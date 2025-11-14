# Black–Scholes Option Pricing in Python
##vido demo<https://youtu.be/GRf9wRx2GD4>
#### by Yingchun Song, Tettnang Germany
#### Solving BS PDE via 3 Methods

---

#### 📘 Description

This project is a **complete implementation of a European option pricer** based on the **Black–Scholes model**.
It aims to demonstrate analytical, stochastic, and numerical approaches to solving the same financial problem—determining the fair price of a call or put option at a given time.

Specifically, the program prices European-style options using **three independent methods**:

1. **Closed-form analytical solution** — the exact Black–Scholes formula.
2. **Monte Carlo simulation** — a stochastic estimation by simulating many potential future asset prices.
3. **Finite Difference Method (FDM)** — a numerical solution to the Black–Scholes partial differential equation using a Crank–Nicolson scheme with Scharfetter–Gummel stabilization.



The project is written entirely in **Python**, follows CS50’s final project structure, and includes complete unit tests using `pytest`.

```
## 🧱 Project Structure

project.py            # main entry point and API functions
test_project.py       # Compare the results of the three algorithms
option.py             # Option, Call, and Put classes
closed_form_price.py  # analytical Black–Scholes pricing
mc_price.py           # Monte Carlo pricing
fdm_price.py          # Finite Difference Method pricing
test_closed_form.py   # test the function closed_form_price and monotonicity
test_mc_price.py      # test the function mc_price and monotonicity
test_fdm_price.py     # test the function fdm_price and monotonicity
requirements.txt      # required dependencies
```

## 🚀 How to Run

###  Run the interactive program
```bash
python project.py
```
Then enter:
- Spot price `S0`
- Strike price `K`
- Risk-free interest rate `r`
- Volatility `sigma`
- Time to maturity `T`

### 3. Run tests
```bash
pytest -q
```

---

## 🧩 Core Functions

```python
price_closed_form(Call, is_call=True)
price_mc(Call, n=200_000, seed=42)
price_fdm(Call, N=400, M=800)
```

---

## 🧮 Example Output

| Method | Call | Put |
|--------|------:|----:|
| Closed-form | 10.4506 | 5.5735 |
| Monte Carlo | ≈10.47 | ≈5.58 |
| FDM | 10.4512 | 5.5756 |

---

## ⚙️ Requirements

```
numpy
pytest
```

---

**Last updated:** October 2025
