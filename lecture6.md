class: middle, center, title-slide
count: false

# Analysis of electric power and energy systems

Lecture 5: High Voltage DC transmission

<br><br>

Bertrand Cornélusse<br>
[bertrand.cornelusse@uliege.be](mailto:bertrand.cornelusse@uliege.be)


---

# What will we learn today?

- Why HVDC systems are used and how they are implemented (focus on LCC)
- How to insert a point-to-point HVDC line in a power flow analysis

You will be able to do exercises *TODO*.

---

class: middle

# HVDC systems

---

## Introduction

intro.pdf

Comparison of CSC(LCC) vs. VSC and focus on LCC.

---

## Components of an LCC HVDC link

around 10 slides from chap1.pdf describing the big picture and the role of components


---

## Thyristor valves

Summary of chap2.pdf

---

## Operation of the LCC line

Almost all of chap3.pdf



---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/WVI8Z7p_rdY" frameborder="0" allowfullscreen></iframe>

6-pulse rectifier

---

## Control

A summary of chap4.pdf, aligned with Ned Mohan's book.

---

## Interaction between AC and DC

Elements of Chap6.pdf as a transition with pf analysis

---

class: middle

# HVDC in the power flow analysis

---

Discuss the simple implementation in panda power.

Discuss the implementation of Bondhala - 2011 - Power Flow Studies of an AC-DC Transmission System

Braunagel, Kraft, Whysong - 1976 - Inclusion of DC converter and transmission equations directly in a newton power flow.

---

# References

- Mohan, Ned. Electric power systems: a first course. John Wiley & Sons, 2012.
- [Course notes of ELEC0445](https://people.montefiore.uliege.be/vct/courses.html) by Pr. Thierry Van Cutsem and al.
- L. Thurner, A. Scheidler, F. Schäfer et al, pandapower - an Open Source Python Tool for Convenient Modeling, Analysis and Optimization of Electric Power Systems, in IEEE Transactions on Power Systems, vol. 33, no. 6, pp. 6510-6521, Nov. 2018.

---

class: end-slide, center
count: false

The end.
