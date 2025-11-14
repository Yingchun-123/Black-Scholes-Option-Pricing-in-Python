# Log-space Crank–Nicolson FDM with Scharfetter–Gummel (exponential fitting) for convection–diffusion.
import math
import numpy as np
from option import Option


def Bfunc(Pe):
    # B(Pe) = Pe / (exp(Pe) - 1), with series for small Pe
    if abs(Pe) < 1e-6:
        # series: 1 - Pe/2 + Pe^2/12 - Pe^4/720 ...
        p2 = Pe*Pe
        return 1.0 - 0.5*Pe + p2/12.0 - p2*p2/720.0
    else:
        return Pe / (math.exp(Pe) - 1.0)

def fdm_price(opt: Option, N=400, M=800):
    S0, K, r, sigma, T = float(opt.S0), float(opt.K), float(opt.r), float(opt.sigma), float(opt.T)
    is_put = opt.payoff(0.0) > 1e-12

    # Domain in S and x=ln S
    volR = sigma * math.sqrt(T)
    Smin = max(1e-12, S0 * math.exp(-4.0 * volR))
    Smax = max(4.0 * K, S0 * math.exp(4.0 * volR))
    xL, xR = math.log(Smin), math.log(Smax)

    nodes = N + 1
    x = np.linspace(xL, xR, nodes)
    hx = (xR - xL) / N
    S = np.exp(x)

    # Coefficients
    D = 0.5 * sigma * sigma      # diffusion alpha
    beta = r - 0.5 * sigma*sigma # convection

    # Time step rule (CN stable, but refine for accuracy)
    dt_diff = 0.45 * (hx*hx) / max(D, 1e-16)
    dt_conv = 0.80 * hx / (abs(beta) + 1e-12)
    dt_cap  = min(dt_diff, dt_conv)
    M_needed = int(math.ceil(T / max(dt_cap, 1e-12)))
    M = max(M, M_needed, 6*N)      # at least 6N
    M = min(M, 20000)
    dt = T / M

    # Build L_cd (SG) coefficients on internal nodes i=1..N-1
    Pe = beta * hx / max(D, 1e-16)
    Bp = Bfunc(Pe)     # B(+Pe)
    Bm = Bfunc(-Pe)    # B(-Pe) = Pe/(1 - exp(-Pe))
    coef = D / (hx*hx)
    a_lo = coef * Bp           # coupling to i-1
    a_up = coef * Bm           # coupling to i+1
    # arrays for each internal row: constant here due to uniform coefficients
    n_in = N - 1
    L_lo = np.full(n_in, a_lo)
    L_up = np.full(n_in, a_up)
    L_diag = - (a_lo + a_up) - r

    # Crank–Nicolson matrices
    Ldiag = np.full(n_in, 1.0 - 0.5*dt*L_diag)
    Lup   = np.full(n_in-1, -0.5*dt*L_up[0])
    Llo   = np.full(n_in-1, -0.5*dt*L_lo[0])

    Bdiag = np.full(n_in, 1.0 + 0.5*dt*L_diag)
    Bup   = np.full(n_in-1,  0.5*dt*L_up[0])
    Blo   = np.full(n_in-1,  0.5*dt*L_lo[0])

    # boundary couplings (first/last interior rows)
    # RHS uses Blo_boundary = 0.5*dt * a_lo (left), Bup_boundary = 0.5*dt * a_up (right)
    Blo_bdry = 0.5*dt * a_lo
    Bup_bdry = 0.5*dt * a_up
    # LHS to move: Llo_boundary = -0.5*dt * a_lo, Lup_boundary = -0.5*dt * a_up
    Llo_bdry = -0.5*dt * a_lo
    Lup_bdry = -0.5*dt * a_up

    # Terminal condition v(T, x) = payoff(S)
    U = np.maximum(K - S, 0.0) if is_put else np.maximum(S - K, 0.0)
    U_in = U[1:-1].copy()

    # Boundary functions in time
    SL, SR = S[0], S[-1]
    def VL_at(t):
        return K*math.exp(-r*(T - t)) if is_put else 0.0
    def VR_at(t):
        return 0.0 if is_put else (SR - K*math.exp(-r*(T - t)))

    # Time stepping
    for n in range(M):
        t_next = T - n*dt
        t_curr = T - (n+1)*dt

        # RHS multiplication for internal vector (constant-coeff tridiag)
        rhs = np.empty_like(U_in)
        # first internal
        rhs[0] = Bdiag[0]*U_in[0] + Bup[0]*U_in[1]
        # middle
        if n_in > 2:
            rhs[1:-1] = Blo[:-1]*U_in[:-2] + Bdiag[1:-1]*U_in[1:-1] + Bup[1:]*U_in[2:]
        # last internal
        if n_in > 1:
            rhs[-1] = Blo[-1]*U_in[-2] + Bdiag[-1]*U_in[-1]

        # add boundary contributions
        rhs[0]  += Blo_bdry * VL_at(t_next)
        rhs[-1] += Bup_bdry * VR_at(t_next)

        # move current-level boundary to RHS
        rhs[0]  -= Llo_bdry * VL_at(t_curr)
        rhs[-1] -= Lup_bdry * VR_at(t_curr)

        # Solve tridiagonal
        # Thomas algorithm:
        n_sys = n_in
        a = Llo.copy()
        b = Ldiag.copy()
        c = Lup.copy()
        d = rhs.copy()
        # forward
        for i in range(1, n_sys):
            w = a[i-1] / b[i-1]
            b[i] -= w * c[i-1]
            d[i] -= w * d[i-1]
        x = np.empty(n_sys, dtype=float)
        x[-1] = d[-1] / b[-1]
        for i in range(n_sys-2, -1, -1):
            x[i] = (d[i] - c[i]*x[i+1]) / b[i]

        U_in = x

    # Reconstruct U0 and interpolate at S0
    U0 = np.empty_like(S)
    U0[0]  = VL_at(0.0)
    U0[-1] = VR_at(0.0)
    U0[1:-1] = U_in

    if S0 <= SL:  price = U0[0]
    elif S0 >= SR: price = U0[-1]
    else:
        i = np.searchsorted(S, S0) - 1; i = max(0, min(i, len(S)-2))
        w = (S0 - S[i])/(S[i+1] - S[i])
        price = (1-w)*U0[i] + w*U0[i+1]

    return float(price)

