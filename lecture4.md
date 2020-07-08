


class: middle, center, title-slide
count: false

# Analysis of electric power and energy systems

Lecture 4: Transformers, power flow analysis part 2

<br><br>

Bertrand Cornélusse<br>
[bertrand.cornelusse@uliege.be](mailto:bertrand.cornelusse@uliege.be)


---

# What will we learn today?

- The power transformer
- The next part of power flow analysis: how to include transformers, and transformers with tap changers

You will be able to do exercises ... from the Ned Mohan's book.

---

class: middle

# The transformer

---

A (single phase) transformer is made of two magnetically coupled coils. An ideal transformer is a two-port represented as 

.grid[
.kol-1-2[.width-80[![](figures/ideal_transformer.png)]]
.kol-1-2[
with
$$u\_2  = n u\_1$$ 
$$i\_2  = -\frac{1}{n}i\_1$$
]]


In power systems, transformers are mainly used to transmit power over long distances by changing the voltage level, thus decreasing the current for a given power level.

Voltage is changed around 5 times between generation and load.

It is also used to 
 
- measure currents and voltages
- electrically isolate parts of a circuit (not the auto-transformer we will see)
- match impedances

---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/vh_aCAHThTQ" frameborder="0" allowfullscreen></iframe>

---

## Non-ideal model

.center.width-90[![](figures/non-ideal-transformer.png)]

The ideal model is complemented by elements 
- $X\_m$ that models the magnetizing inductance
- $X\_{leakage, i}$ that models the flux not captured by the core on side $i$
- $R\_{core}$ that models eddy current and hysteresis losses, i.e. losses in the iron core
- $R\_{1}$ and $R\_{2}$ that model (coil) copper losses

Parameters are either given in the datasheet or obtained by open-circuit and short-cirtuit tests.

Laminated core to decrease losses.

---

The excitation current, sum of the currents in $R\_{core}$ and $X\_m$, is often neglected, leading to a simpler non-ideal model, and the series impedances can be transferred from one side to the other:

.grid[
.kol-1-2[.center.width-90[![](figures/non-ideal-transformer-2.png)]]
.kol-1-2[
with $$Z\_p = R\_1 + jX\_{leakage, 1}$$ and $$Z\_s = R\_2 + jX\_{leakage, 2}$$]]

---

## Per unit representation

Let's consider the rated voltages and currents on both sides of the (ideal) transformer as base values. As $$V\_{s, base} = n V\_{p, base} $$ and $$ I\_{p, base} = n V\_{s, base},$$
the *MVA base is the same on both sides*, and thus
$$Z\_{s, base} = n^2 Z\_{p, base}$$

Hence, *in per unit, the transformer can be replaced by a single impedance* equal to 
$$Z\_{tr} = \frac{Z\_{p}}{Z\_{p, base}}+\frac{Z\_{s}}{Z\_{s, base}}.$$

---

Thus we have also that $$\begin{aligned}Z\_{tr} &= \frac{Z\_{p}+ Z\_s/n^2}{Z\_{p, base}} \\\\ &= \frac{n^2 Z\_{p} + Z\_s}{Z\_{s, base}}\end{aligned}$$
i.e. the impedance if the same whether we see it from the primary or the secondary side, although the voltage bases differ.

Also, if the three-phase transformer is *wye-delta* connected, a *30° phase shift* must be applied (more on this later).

---

## Example 6.1

Consider the one-line diagram 

.width-90[![](figures/example-6-1.svg)]

with 
 - a 200 km line with $R = 0.029 \Omega/km$, $X=0.326 \Omega/km$, neglected shunt impedances
 - two ransformers with a leakage reactance of $0.2 pu$ in the (500 kV, 1000 MVA) base, and losses neglected.

*What is the equivalent model in a (345 kV, 100 MVA) base?*

---

### In the (500 kV, 1000 MVA) base:

- $Z\_{line, pu} = 200 \times (0.029 + j 0.326) / (500^2/1000) = 0.0232 + j 0.2608 pu$

- hence the total impedance between buses 1 and 2 is $$Z\_{12} = 0.0232 + j 0.2608  + 2 * j 0.2pu =  0.0232 + j 0.6608 pu $$

---

### In the (345 kV, 100 MVA) base:

- the pu value of the impedance is the same in the (*500* kV, 1000 MVA) and (**345** kV, 1000 MVA) bases

- if we now change the MVA base to 100 MVA, 
 $$Z\_{12} = 0.0232 + j 0.6608  \times (100/1000) pu =  0.00232 + j 0.06608 pu$$ since the base impedance is proportional to the inverse of the MVA base.

---

## Efficiency

The efficiency expressed in % is 
$$100 \times \frac{P\_{output}}{P\_{input}} = 100 \times \left(1 - \frac{P\_{losses}}{P\_{input}}\right) $$

- maximal when copper losses = iron losses (cancel derivative of efficiency w.r.t current) 
- Around 99.5 % in large power transformers at full load.

---

## Tap changers

- Some transformers are equipped with a system allowing to change the $1:n$ ratio
- The ability to change the tap under load is called load tap changer (LTC) or on-load tap changer (OLTC)
- This is mainly used for voltage control.
- It is usually implemented using auto-transformers.
- We will see later on how to include this in the power flow analysis.

---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/R_NxRDXOEFk" frameborder="0"  allowfullscreen></iframe>

---

## Auto-transformers

The two windings (of the same phase) are connected in series, without galvanic insulation. They are commonly used when the ratio is limited.

Advantages: 
- Physically smaller
- less costly (less copper)
- higher efficiency
- easy to implement tap changes
- "solid" earth grounding

Disadvantages:
- no electrical insulation
- higher short circuit current
- full voltage at secondary if it breaks (in case of a step down)

---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/lltVwhoPvh0" frameborder="0"  allowfullscreen></iframe>


---

## Phase shift in delta-star transformers

The star part has $n$ times the number of turns of the delta part (primary side).

Let's reason on phase $a$,
- Voltage $\bar{V}\_{a,s}$ is on the same core as $\bar{V}\_{AC,p} = \sqrt{3}\bar{V}\_{a,p} \angle{-30^\circ}$ where $\bar{V}\_{a,p}$ is the (virtual) phase-neutral voltage on the primary side.
- Hence 
$$\bar{V}\_{a,s} = n\sqrt{3} \bar{V}\_{a,p} \angle{-30^\circ}$$

We gain a $\sqrt{3}$ in the amplification, but a lagging phase shift of 30°.

The same reasoning olds for phases $b$ and $c$.


---

## Power flow regulation by phase shifting

We have seen in previous courses that active power flows are dictated by the voltage magnitudes but also the sine of the angle difference between buses.

See [https://en.wikipedia.org/wiki/Quadrature_booster](Wikipedia)

---

## Three-winding transformers

---

## Three-phase transformers

Three single phase tfos vs on three-phase 


---

class: middle

# Transformers in the power flow analysis


---

## Representing taps and phase shifts

Section 6.11

---

## The generic transmission line

Adapt from VCT's slides on power flow

---

# References

- Mohan, Ned. Electric power systems: a first course. John Wiley & Sons, 2012. Chapter 6.
- Weedy, Birron Mathew, et al. Electric power systems. John Wiley & Sons, 2012. Section 3.8.
- Course notes of ELEC0014 by Pr. Thierry Van Cutsem.


---

class: end-slide, center
count: false

The end.
