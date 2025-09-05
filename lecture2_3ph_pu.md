class: middle, center, title-slide
count: false


---
### Case 2: **Neutral Broken**

When the neutral breaks, the three resistors form a system without a direct connection to the neutral point. The current through each resistor still needs to sum to zero because the current has no return path through the neutral. This changes the voltage distribution across the resistors.


---

#### Voltages:

  Here, $ V\_{nN'} $ is an unknown voltage offset at the floating point $ N' $ (the shifted neutral). Using KCL, you solve for this voltage by ensuring the sum of the currents at $ N' $ is zero:
  $$
  \frac{V\_{aN'}}{R\_a} + \frac{V\_{bN'}}{R\_b} + \frac{V\_{cN'}}{R\_c} = 0
  $$
  Solving this system gives you the new voltages across the resistors.

---

#### Currents:

- The currents in each phase are then given by:
  $$
  I\_a = \frac{V\_{aN'}}{R\_a}, \quad I\_b = \frac{V\_{bN'}}{R\_b}, \quad I\_c = \frac{V\_{cN'}}{R\_c}
  $$
  
  Since the neutral is broken, the sum of these currents must equal zero:
  $$
  I\_a + I\_b + I\_c = 0
  $$

#### Powers:

- The power consumed in each phase is:
  $$
  P\_a = V\_{aN'} I\_a = \frac{(V\_{aN'})^2}{R\_a}, \quad P\_b = \frac{(V\_{bN'})^2}{R\_b}, \quad P\_c = \frac{(V\_{cN'})^2}{R\_c}
  $$
  
- Total power consumed:
  $$
  P\_{\text{total}} = P\_a + P\_b + P\_c
  $$

---

### Observations:

- When the neutral is connected, the voltages across the resistors are straightforwardly determined by the phase-to-neutral voltages.
- When the neutral is broken, the voltage distribution becomes more complex, and the voltages across the resistors are no longer the same as the phase-to-neutral voltages. The total current in the system remains zero, and the power distribution can also change depending on the values of the resistors.


[A numerical example here.](https://colab.research.google.com/drive/1pXH21c8g9Hv3h94pb81OtuFVQfauG63T?usp=sharing)

---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/HqZtptHnC2I" frameborder="0" allowfullscreen></iframe>

Why not 6 or 12?

---

## Useful formulas: from star to delta connection (and back)

.center.width-60[![](figures/star_delta.png)]

.grid[
.kol-1-2[$$ \begin{aligned}
Z\_a &= \frac{Z\_{ab}Z\_{ca}}{Z\_{ab} + Z\_{bc} + Z\_{ca}} \\\\
Z\_b &= \frac{Z\_{bc}Z\_{ab}}{Z\_{ab} + Z\_{bc} + Z\_{ca}} \\\\
Z\_c &= \frac{Z\_{ca}Z\_{bc}}{Z\_{ab} + Z\_{bc} + Z\_{ca}}
\end{aligned}$$]
.kol-1-2[$$ \begin{aligned}
Z\_{ab} &= \frac{Z\_{a}Z\_{b}+Z\_{b}Z\_{c}+Z\_{c}Z\_{a}}{Z\_{c}} \\\\
Z\_{bc} &= \frac{Z\_{a}Z\_{b}+Z\_{b}Z\_{c}+Z\_{c}Z\_{a}}{Z\_{a}} \\\\
Z\_{ca} &= \frac{Z\_{a}Z\_{b}+Z\_{b}Z\_{c}+Z\_{c}Z\_{a}}{Z\_{b}}
\end{aligned}$$]
]

What happens in a balanced system?

---

## Per-phase analysis

In a **balanced** system, analyses can be simplified by reprensenting only one phase

 - this is straighforward if there are no couplings between phases
 .center.width-80[![](figures/per-phase.png)]
 - in case there is a coupling, and that for instance the voltage drop $\bar{V}\_{aA}$ along a line presenting an impedance $Z\_{self}$ traversed by a current $\bar{I}\_{a}$ is also function of the currents in the other phases:
$$\bar{V}\_{aA} = Z\_{self} \bar{I}\_{a} + Z\_{mutual} \bar{I}\_{b} + Z\_{mutual} \bar{I}\_{c}$$
then the per-phase equivalent impedance (for phase $a$) is $$Z\_{aA} = Z\_{self} - Z\_{mutual}$$
since $\bar{I}\_{a} + \bar{I}\_{b} + \bar{I}\_{c} = 0$


---

## One-line diagram

.center.width-80[![](figures/one-line.png)]

---


class: middle
# The "per unit" representation

---

## The per unit representation is a way to normalize data

It is used extensively in power systems. 
It has several advantages:

 - Values (e.g. device parameters) stay in a narrow range (whatever their "size")
 - Voltages tend to have values close to 1, which eases comparison
 - With appropriate "normalization ratios", (ideal) transformers disappear
 - Normalization facilitates numerical computation (no huge numbers, no tiny numbers)

---

## Working in per unit in 5 steps

 1. Chose 3* "fundamental" base values: 
  - $V_B$ for the voltage [kV]
  - $S_B$ for the power [MVA]
  - $t_B$ for the time [s], or $\omega_B$ for the angular frequency [rad/s]
 2. Derive other needed base values from physical laws, e.g. 
  - the base current: $I_B = S_B/V_B$ [A]
  - the base impedance: $Z_B = V_B^2/S_B$ [$\Omega$]
 3. Normalize input data: divide parameters by their base value
 4. Make your computations
 5. (If necessary) Apply the inverse transformation

--

Data in per unit is by definition dimensionless; pay attention to base value units w.r.t. to physical value units!

(*) When there are transformers, one base voltage per voltage level is preferrable

---

## Example 

It is known that the internal reactance of a synchronous machine lies typically in the range $[1.5, 2.5] \ pu$ (on the machine base)

- A machine with the characteristics $(20 \ kV, 300 \ MVA)$ has a reactance of $2.667 \ \Omega$. Is this a normal value?
 - (Here we do not need a base value for time)
 - the base impedance is $Z_B = 20^2/300 = 1.333 \ \Omega$
 - hence the value of the reactance in per unit is $2.667/1.333 = 2 \ pu$
 - this is a quite normal value!
- Same question for a machine with the characteristics $(15 \ kV, 30 \ MVA)$
 - The base impedance is now $Z_B=15^2/30 = 7.5 \ \Omega$
 - the value of the reactance in per unit is $2.667/7.5 = 0.356 \ pu$
 - hence an abnormal small value!

.footnote[From ELEC0014]

---

## Per unit in three-phase systems

Let the base power $S\_B$ be the three-phase power, and $U\_b=\sqrt{3}V\_B$ be the line to line voltage base.

The (single-phase) base current is $$I\_B = \frac{S\_B}{3V\_B} = \frac{S\_B}{\sqrt{3}U\_B}$$

The base impedance is $$Z\_B = \frac{V\_B}{I\_B} = \frac{3V^2\_B}{S\_B} = \frac{U\_B^2}{S\_B}$$

In a single phase equivalent representation, the power values in per unit can be multiplied by $S\_b$ to get the total three-phase power.

---

# References

- Mohan, Ned. Electric power systems: a first course. John Wiley & Sons, 2012.
- Course notes of ELEC0014 by Pr. Thierry Van Cutsem.

---

class: end-slide, center
count: false

The end.
