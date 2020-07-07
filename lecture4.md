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
- electrically isolate parts of a circuit
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

---

The excitation current, sum of the currents in $R\_{core}$ and $X\_m$, is often neglected, leading to a simpler non-ideal model, and the series impedances can be transferred from one side to the other:

.grid[
.kol-1-2[.center.width-90[![](figures/non-ideal-transformer-2.png)]]
.kol-1-2[
with $$Z\_p = R\_1 + X\_{leakage, 1}$$ and $$Z\_s = R\_2 + X\_{leakage, 2}$$]]

---

## Eddy currents

-> Laminated magnetic cores

One of the core losses (or iron losses).

---

## Copper losses 

---

## Non-ideal model

---

## Transfer of impedance through the ideal transformer

$n^2$ from $1$ to $n$

---

## Per unit representation

---

## Example 6.1

---

## Efficiency

---

## Tap changers

---

## Auto-transformers

---

## Phase shift in delta-star transformers

---

## Power flow regulation by phase shifting


---

## Three-winding transformers

---

## Three-phase transformers

Three single phase tfos vs on three-phase 


---

class: middle

# Transformers in the power flow analysis


---

## The generic transmission line

Adapt from VCT's slides on power flow

---

# References

- Mohan, Ned. Electric power systems: a first course. John Wiley & Sons, 2012.
- Course notes of ELEC0014 by Pr. Thierry Van Cutsem.
- L. Thurner, A. Scheidler, F. Schäfer et al, pandapower - an Open Source Python Tool for Convenient Modeling, Analysis and Optimization of Electric Power Systems, in IEEE Transactions on Power Systems, vol. 33, no. 6, pp. 6510-6521, Nov. 2018.

---

class: end-slide, center
count: false

The end.
