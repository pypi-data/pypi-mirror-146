# The Merton Model

## Introduction
The Merton model was first developed by economist Robert Merton in 1974. The model makes a claim about default probabilities based on the capital structure of the firm. It models the value of equity as a call option on the total assets of the underlying firm. If assets are below the call option’s strike price at time $T$, the firm defaults, the value of equity goes to zero, and the remaining value of the firm is divided equally among debt holders. 

The model has some limitations. The version of the model we considered makes the Black-Scholes assumptions, which are generally accepted to be false. Furthermore, it does not address the possibility of a bankruptcy before time $T$.

We used several resources. Of particular utility was a Society of Actuaries article entitled "Structural Credit Risk Modeling: Merton and Beyond" by Wang, "Options, Futures, and Other Derivatives" 9th ed. by Hull, and Journal of Banking & Finance article "Credit spreads with dynamic debt" by Das and Kim.

## Black-Scholes Assumptions and Formula
In addition to the frame-work of the Merton model, we adopted the Black-Scholes assumptions but with the underlying asset being the total assets of the firm. These assumptions are the following.
	* A constant continuously compounded risk-free rate r.
	* The assets of the firm follow geometric Brownian motion. In particular, if the total assets of the firm at time $t$ are equal to $A_t$, then the assets satisfy the stochastic differential equation
$$
dA_t=r A_t  dt+ σ_A  A_t  dW_t
$$
where $W_t$ denotes Brownian motion under the risk-neutral probability measure $Q$.
	* The coefficient in the diffusion term σ_A is constant.
	* Portfolios can be instantaneously rebalanced.
	* There are no transaction costs or taxes. That includes transaction costs on short positions.
	* There are no arbitrage opportunities. That is, returns in excess of the risk-free rate are proportional to the risk associated with the position. 
Under these assumptions, we can use the popular Black-Scholes call option formula to model the value of the firm’s equity $E_t$:
$$
E_t= A_t N(d_1)-Ke^{-r(T-t)} N(d_2),
$$
where
$$
d_1=  \frac{\log(A_t/K)+ (r+ \sigma_A^2/2)(T-t)}{\sigma_A \sqrt{T-t}}\quad\text{and}\quad $d_2=d_1- \sigma_A\sqrt{T-t}.
$$

## Parameter Selection
The formulas in the previous section raise questions regarding parameter selection. How would one estimate the diffusion coefficient $\sigma_A$ and strike price $K$ as well as select the length of the time window? This section aims to address those questions.
The value of $\sigma_A$ is unobservable and we must derive this value from other traded assets. The diffusion coefficient of equity $\sigma_E$ is also unobservable, but there is a great deal of theory behind $\sigma_E$ and an implied value can be extracted from market data. Then, under the assumption that the value of equity $E_t$ also follows Brownian motion,
$$ 
\sigma_E E_t- \sigma_A A_t N(d_1) = 0.
$$
Within the Python code, we used fsolve to find $\sigma_A$. In the cases were the solver does not converge, we assume
$$
A_t =E_t+L_t\quad\text{and}\quad N(d_1) = 0.8.
$$
The value of $L_t$ is the present value of the cash flows from liabilities. It is calculated using a put option as described in the next section, but within this put option assume the volatility of the underlying is $\sigma_E$ instead of $\sigma_A$; this overestimates the volatility of the underlying which decreases the value of $L_t$. Using all of these assumptions, we find
$$
\sigma_A=  \frac{E_t}{0.8(E_t+L_t)}\sigma_E.
$$
The value of $\sigma_A$ is most likely smaller than what is implied from our calculations.

Regarding the time window, we supposed $t = 0 and $T = 1$. This choice is somewhat arbitrary. However, modeling default over a shorter window is more likely to produce reliable results. This is because a firm’s balance sheet provides less and less information about its future capital structure the further and further away the present we conduct our analysis. 

Our choice of strike price $K$ was less clear. Denote the current and noncurrent liabilities of the firm by $CL$ and $NCL$, respectively. Then we considered
$$
K =  \frac{1}{2}CL + \frac{1}{2}NCL,\quad K = CL + \frac{1}{2} NCL,\quad\text{and}\quad K =  \frac{3}{2} CL+  \frac{1}{2} NCL.
$$
Since we are considering models where $T = 1$, current liabilities, i.e. liabilities that are due in one year or less, are highly relevant. Furthermore, due to the time value of money, the coefficient in front of CL seems as though it ought to be at least 1. As a result, within the current iteration of the code, we have 
$$
K = CL + \frac{1}{2} NCL.
$$

## Further Formulas
Using the Black-Scholes frame-work, the risk neutral probability of default is
$$
P^Q(A_T < K)=N(-d_2).
$$
As stated previously, we could have
$$
A_{t_1} < K\quad\text{but} A_T > K
$$
for $t\leq t \leq t_1 \leq T$. This would trigger a default not accounted for within our calculations. 

Let us derive the value of liabilities $L_t$.  Due to the assumptions of the model, we suppose $L_T = K$ as long as the firm does not default. If we purchase the liabilities for price $L_t$ and a put option with strike price $K$, then we obtain $K$ at time $T$ with no risk. If the time $t$ value of the put option is $P_t$, then no arbitrage pricing implies
$$
L_t + P_t=Ke^{-r(T-t)}.
$$
It follows that
$$
L_t = K e^{-r(T-t)}-P_t.
$$

We can obtain a formula for the spread $s$ over the risk-free rate. Since
$$
L_t=K e^{-r(T-t)}-P_t,
$$
and we would discount $K$ at a rate of $r + s$ to obtain $L_t$. It follows that
$$
K e^{-(r+s)(T-t)}= K e^{-r(T-t)}-P_t. 
$$
Hence, the continuously compounded spread is
$$
s= -\frac{1}{T-t}\log\left(1 - \frac{P_t}{K}e^{r(T-t)}\right).
$$

## Functions

get_d(V, T, K, r, sigma_V)

V: Value of the firm.
T: Time until maturity.
K: Strike price; related to the firm's debt level.
r: Risk-free rate.
sigma_V: Firm volatility.


distance(V, T, K, r, sigma_V) 

The Merton model distance to default. Corresponds to $d_2$ in the Black-Scholes framework.


prob_default(V, T, K, r, sigma_V)

The probability of default using the Merton model. Corresponds to $N(-d_2)$ in the Black-Scholes framework.


call(V, T, K, r, sigma_V)

Value of a call option under the Black-Scholes framework. Corresponds to the value of equity under the Merton model. Formula on page 604 of "Options, Futures, and Other Derivatives" 9th ed. by Hull.

put(V, T, K, r, sigma_V, phi = 1)

Value of a put option under the Black-Scholes framework. Corresponds to value of insurance required to make debt risk free. Formula on page 604 of "Options, Futures, and Other Derivatives" 9th ed. by Hull.
    
V: Value of the firm.
T: Time until maturity.
K: Strike price; related to the firm's debt level.
r: Risk-free rate.
sigma_V: Firm volatility. 
phi: Fraction of firm's value retained in the case of default.


put_ui(V, T, K, H, r, sigma_V, phi = 1)

Value of an up-and-in put option under the Black-Scholes framework. Formula on page 605 of "Options, Futures, and Other Derivatives" 9th ed. by Hull.
    
V: Value of the firm.
T: Time until maturity.
K: Strike price; related to the firm's debt level.
H: Value of the firm which activates the up-and-in option.
r: Risk-free rate.
sigma_V: Firm volatility. 
phi: Fraction of firm's value retained in the case of default.


put_uo(V, T, K, H, r, sigma_V, phi = 1)

Value of an up-and-out put option under the Black-Scholes framework. Formula on page 605 of "Options, Futures, and Other Derivatives" 9th ed. by Hull.
    
V: Value of the firm.
T: Time until maturity.
K: Strike price; related to the firm's debt level.
H: Value of the firm which deactivates the up-and-out option.
r: Risk-free rate.
sigma_V: Firm volatility. 
phi: Fraction of firm's value retained in the case of default.


prob_default_mc(V, T, K, r, sigma_V, trails = 10000, steps = floor(12 * T + 1))

Probability of default if possible for some values of t prior to maturity. Default occurs if the value of the firm is below K at time Δt, 2Δt, ..., or T = steps · Δt.
If T is measured in years, steps = floor(12 * T + 1) corresponds to possibility of default at each monthly payment. Probability obtained using Monte Carlo simulation.
    
V: Value of the firm.
T: Time until maturity.
K: Strike price; related to the firm's debt level.
r: Risk-free rate.
sigma_V: Firm volatility. 
trails: Monte Carlo simulations used to obtain approximation; antithetic values also considered.
steps: Number of times the firm can default within each simulation.


spread(V, T, K, r, sigma_V, phi = 1)

CDS spread given default only possible at T. Uses the Black-Scholes framework. Value tends to be below market CDS spreads.
    
V: Value of the firm.
T: Time until maturity.
K: Strike price; related to the firm's debt level.
r: Risk-free rate.
sigma_V: Firm volatility. 
phi: Fraction of firm's value retained in the case of default.


spread_mc(V, T, K, r, sigma_V, phi = 1, trails = 10000, steps = floor(12 * T + 1))

CDS spread if default possible for some values of t prior to maturity. Default occurs if the value of the firm is below K at time Δt, 2Δt, ..., or T = steps · Δt. If T is measured in years, steps floor(12 * T + 1) corresponds to monthly payments. In the case of default, partial payment assumed to be made at time T. Probability obtained using Monte Carlo simulation.
    
V: Value of the firm.
T: Time until maturity.
K: Strike price; related to the firm's debt level.
r: Risk-free rate.
sigma_V: Firm volatility. 
phi: Fraction of firm's value retained in the case of default.
trails: Monte Carlo simulations used to obtain approximation; antithetic values also considered.
steps: Number of times the firm can default within each simulation.


spread_das(V, T, K_1, K_2, H, r, sigma_V, phi = 1)

CDS spread if default possible only at time T, but firm increases debt if its value goes above barrior. Inspired by the Journal of Banking & Finance article "Credit spreads with dynamic debt" by Das and Kim.
    
V: Value of the firm.
T: Time until maturity.
K_1: Strike price if firm does not increase its debt level.
K_2: Strike price if firm increases its debt level.
H: Value of the firm which triggers it to increase its debt level from K_1 to K_2.
r: Risk-free rate.
sigma_V: Firm volatility. 
phi: Fraction of firm's value retained in the case of default.


obj(sigma_V, sigma_E, V, T, K, r)

Objective function to be minimized. Used to obtain the volatility of the firm's value.
    
sigma_V: Firm volatility.
sigma_E: Equity volatility.
V: Value of the firm.
T: Time until maturity.
K: Strike price; related to the firm's debt level.
r: Risk-free rate.


get_sigma_V(sigma_E, V, T, K, r)

Obtain the volatility of the firm's value. Uses the Black-Scholes framework and fsolve.
    
sigma_E: Equity volatility.
V: Value of the firm.
T: Time until maturity.
K: Strike price; related to the firm's debt level.
r: Risk-free rate.


get_K(CL, NCL, T = 1, r = 0)

If the value of the firm drops below K at maturity, then the firm is considered to be in default under the Merton model. Formula overweights current liabilities because they must be paid within the year or one business cycle.
    
CL: Current liabilities.
NCL: Noncurrent liabilities
T: Time until maturity.
r: Risk-free rate.

## References
Wang, Yu. “Structural Credit Risk Modeling: Merton and Beyond.” Society of Actuaries, June 2009, Structural Credit Risk Modeling: Merton and Beyond (soa.org). Accessed June 2021.
“Default Probability by Using the Merton Model for Structural Credit Risk.” MathWorks, Default Probability by Using the Merton Model for Structural Credit Risk - MATLAB & Simulink (mathworks.com). Accessed June 2021.
Sundaresan, Suresh. “A Review of Merton’s Model of the Firm’s Capital Structure with its Wide Applications.” Columbia Business School, Merton_review_cap_structure.pdf (columbia.edu). Accessed June 2021. 
Hull, John. "Options, Futures, and Other Derivatives" 9th ed. 
Das, S. and Kim. Journal of Banking & Finance article "Credit spreads with dynamic debt"
