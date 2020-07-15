class: middle, center, title-slide
count: false

# Analysis of electric power and energy systems

Lecture 6: Synchronous generators

<br><br>

Bertrand Cornélusse<br>
[bertrand.cornelusse@uliege.be](mailto:bertrand.cornelusse@uliege.be)


---

# What will we learn today?

- What are synchronous generators
- How we can model them for our analyses
- How to include generator limits in power flow computation.

You will be able to do exercises **TODO**


---

class: middle

# Principle

---

## Synchronous machines

Synchronous machines produce the major part of the electric energy
 - range from a few kVA to a few hundred MVA 
 - the biggest are rated 1500 MVA

They play other important roles:
 - they impose the frequency of sinusoidal voltages and currents
 - they provide an “energy buffer” (through the kinetic energy stored in their rotating masses)
 - they can produce or consume reactive power (needed to regulate voltage).

---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/8XF-11MQGQ0?list=PLuUdFsbOK_8qVROrfl2M2WSV2xAz-ABVU" frameborder="0" allowfullscreen></iframe>

Magnetic field created by the stator

---

## Magnetic field created by the stator

several slides from transp-g-1.pdf


---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/tiKH48EMgKE?list=PLuUdFsbOK_8qVROrfl2M2WSV2xAz-ABVU" frameborder="0"  allowfullscreen></iframe>

Magnetic field created by the rotor

---

## Magnetic field created by the rotor

several slides from transp-g-1.pdf

---

## The two types of synchronous machines

several slides from transp-g-1.pdf

---

class: middle

# Model

---

## Per phase equivalent circuit

Start from this, transp-g-2.pdf slide 11/23

Then top down approach to show how to obtain  $X$, $R\_a$, $\delta$, ...

---

## Power balance

Try to give intuition, 

---

## power balance of stator

$p\_{r\rightarrow s} = 3 P + p\_{Js}$

Mechanical power converted in electrical power + Joule losses of the stator

---

## power balance of rotor

Mechanical power + field current.

- In steady state, the power entering the field winding is dissipated in Joule losses !
 - magnetizes the rotor
- all mechanical power transfered to the stator

---

## Capability curves

Slide 20/23

Explanation of limits.

--- 

## Power output, stability, and loss of synchronism


From ned Mohan section 9.4

Also transp-g-2.pdf slide 19/23

--- 

## Adjusting reactive power 

Intuitive explanations of sections 9.5, overexcitation, under excitation.

From ned Mohan section 9.5

A word about synchronous condesers

--- 



---

class: middle

# Synchronous generators in the power flow analysis

---

## TODO

---

# References

- Mohan, Ned. Electric power systems: a first course. John Wiley & Sons, 2012.
- [Course notes of ELEC0014](https://people.montefiore.uliege.be/vct/courses.html) by Pr. Thierry Van Cutsem.
- L. Thurner, A. Scheidler, F. Schäfer et al, pandapower - an Open Source Python Tool for Convenient Modeling, Analysis and Optimization of Electric Power Systems, in IEEE Transactions on Power Systems, vol. 33, no. 6, pp. 6510-6521, Nov. 2018.

---

class: end-slide, center
count: false

The end.
