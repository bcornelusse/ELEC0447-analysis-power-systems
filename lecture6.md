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

-   stator (or *armature*) = motionless, separated from the rotor by a
    small air gap

-   subjected to varying magnetic flux ⇒ built up of thin laminations to
    decrease *eddy (or Foucault)* currents

-   equipped with three windings, distributed 120 degrees apart in
    space.

 
Magnetic field created by a direct current flowing in one of the stator
windings:

.center.width-50[![](figures/stator_field.jpg)]

---

The magnetic field lines cross the air gap radially.



The amplitude $B(\varphi)$ of the magnetic flux density at point P :

-   is a periodic function of $\varphi$ with period $2\pi$

-   this function has a “staircase” shape

-   is made as close as possible to a sinusoid, by properly distributing
    the conductors along the air gap.

 

Layout of the three phases (each winding represented by a single turn for clarity):

.center.width-30[![](figures/layout_phases.jpg)]


---

Total flux density created by the three phases at point P corresponding to angle $\varphi$:

$$B\_{3 \\phi}(\\varphi) = k i\_a \\cos \\varphi + k i\_b \\cos(\\varphi - \\frac{2
\\pi}{3}) + k i\_c \\cos(\\varphi - \\frac{4 \\pi}{3})$$

If three-phase alternating currents are flowing in the windings:

$$B\_{3 \\phi}(\\varphi) = \frac{3 \sqrt{2} k I}{2}  \cos(\omega t + \psi - \varphi)$$

The three-phase alternating currents all together produce the same
magnetic field as a magnet (or a coil carrying a direct current)
rotating at the angular speed $\omega$

 - North pole of magnet ≡ maximum of $B(\varphi)$
 - South pole of magnet ≡ minimum of $B(\varphi)$


---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/tiKH48EMgKE?list=PLuUdFsbOK_8qVROrfl2M2WSV2xAz-ABVU" frameborder="0"  allowfullscreen></iframe>

Magnetic field created by the rotor

---

## Magnetic field created by the rotor

-   rotor = rotating part, separated from the rotor by the air gap

-   carries a winding in which a direct current flows, in steady-state
    operation

-   referred to as *field* winding (in French: enroulement d'excitation)

 

Magnetic field created by this direct current (field winding represented by a single turn for clarity)
:

.center.width-50[![](figures/rotor_field.jpg)]

---

## Interaction between magnetic fields and electromechanical conversion

-   In a synchronous machine, in steady state, the rotor rotates at the
    same angular speed $\omega$ as the magnetic field produced by the stator
-   thus, the stator and rotor magnetic fields are fixed with respect to
    each other
-   both fields tend to align in the manner of two magnets
-   if one pulls apart those two magnets, an electromagnetic torque
    appears.

Mechanical analogy:

.center.width-50[![](figures/interaction_fields.jpg)]

.center[generator operation <-> motor operation]

There exists a max value of the electromagnetic torque $T\_e$ $\; \rightarrow \;$ loss of synchronism

---

class: middle, center 

# The two types of synchronous machines

---

## Machines with multiple pairs of poles

Some turbines operate at a lower speed, but AC voltages and currents at the stator must keep the same period $T=\\frac{1}{f}$

.grid[
.kol-1-2[
-   the rotor carries $p$ pairs of poles
-   during a period $T$, the rotor makes only $\frac{1}{p}$ of a whole revolution
-   the stator carries $p$ sets of (a, b, c) windings
-   one winding spans an angle of $\frac{\pi}{p}$  radians
-   during a period $T$, each stator winding is still swept by one North and one South pole of rotor.
]
.kol-1-2[
.center.width-60[![](figures/several_poles.jpg)]
.center[example: $p=2$ ]
]]


---

## Machines with multiple pairs of poles (...)

Speed: $\\displaystyle \\frac{3000}{p}$ rev/min at 50 Hz

The various windings relative to a given phase are connected (in series
or parallel) to end up with a three-phase machine.

**Caution**: $p$ sometimes denotes the number of poles, sometimes the number of pairs of poles.

---

## Round-rotor generators (or turbo-alternators)

.center.width-80[![](figures/round_rotor.png)]

Driven by steam or gas turbines, which rotate at high speed

-   $p=1$ (conventional thermal units)   or   $p=2$ (nuclear units)

-   cylindrical rotor made up of solid steel forging

-   diameter  << length (centrifugal force !)

-   field winding made up of conductors distributed on the rotor, in
    milled slots

-   even if the generator efficiency is around 99 %, the heat produced
    by Joule losses has to be evacuated !  Large generators are cooled by hydrogen (heat evacuation 7 times
    better than air) or water (12 times better) flowing in the hollow
    stator conductors.
---

## Salient-pole generators

.center.width-70[![](figures/salient_poles.png)]


-   Driven by hydraulic turbines (or diesel engines), which rotate at
    low speed

-   $p$ is much higher (at least 4)  ⇒  it is more convenient to have
    field windings concentrated and placed on the poles

-   diameter  >>  length (to have space for the many poles)

-   rotor is laminated (poles easier to construct)

-   generators usually cooled by the flow of air around the rotor.

---


## Damper windings (or amortisseurs)

-   round-rotor machines: copper/brass bars placed in the same slots at
    the field winding, and interconnected to form a damper cage (similar
    to the squirrel cage of an induction motor)

-   salient-pole machines: copper/brass rods embedded in the poles and
    connected at their ends to rings or segments.

Why?

-   in perfect steady state: the magnetic fields produced by both the
    stator and the rotor are fixed relative to the rotor ⇒ no current
    induced in dampers

-   after a disturbance: the rotor moves with respect to stator magnetic
    field  
    ⇒ currents are induced in the dampers…  
    ... which, according to Lenz’s law, create a *damping torque* helping
    the rotor to align on the stator magnetic field.

 

Remark: in round-rotor generators: the solid rotor offers a path for eddy currents,
which produce an effect similar to those of dampers.

---

class: middle

# Model

---

## Induced emf in the stator windings

There are two sources that induce an *emf* (electromotive force) in the stator windings. 

 - the effect of the rotor's induced field ($\bar{E}\_{af}$)
 - the effect of the current flowing in the stator itself, called the armature reaction ($- j X\_s \bar{I}\_a$).

By superimposing them, we get the resulting emf.

We assume there is no magnetic saturation.

---

## Per phase equivalent circuit (for phase $a$)

.center.width-50[![](figures/generator_model.svg)]
- $R\_s$ is the resistance of a phase
- the *synchronous reactance* $X\_s$ characterizes the *steady-state operation* of the machine (magnetizing + leakage reactances)
- $\delta$, the phase shift between the internal emf $\bar{E}\_{af}$ and the terminal voltage $\bar{V}\_a$,  is called the *internal angle* or *load angle* of the machine.

.footnote[See [sourse notes of ELEC0431](https://people.montefiore.uliege.be/geuzaine/ELEC0431/3_Synchronous.pdf) for more details.]

We thus have 
$$\bar{V}\_a = \bar{E}\_{af} - R\_s \bar{I}\_a - j X\_s \bar{I}\_a$$

---
## Phasor diagram representation

.center.width-70[![](figures/generator_diagram.svg)]

---

## Remark: models for other types of analysis

So far we are mostly interested in steady-state.

But note that depending on the type of analysis carried out, the model used should be adapted: 
- *Subtransient condition* (e.g. just after a short circuit fault): $X''\_s << X\_s$
- *transient state* (after the subtransient condition, before steady state):  $X'\_s < X\_s$ but $X'\_s < X''\_s$

The field induced emf has to be adapted as well depending on the type of analysis.

---

class: middle, center

# Properties of the model

---

## Power output, stability, and loss of synchronism

From ned Mohan section 9.4

Also transp-g-2.pdf slide 19/23

---

## Adjusting reactive power 

By controlling the field current, it is possible to control the induced emf and the reactive power delivered.

Intuitive explanations of sections 9.5, overexcitation, under excitation.

From ned Mohan section 9.5

A word about synchronous condesers

---

## Power balance

*From VCT*

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

class: middle

# Synchronous generators in the power flow analysis

---

## TODO

---

# References
- [Course notes of ELEC0014](https://people.montefiore.uliege.be/vct/courses.html) by Pr. Thierry Van Cutsem.
- Mohan, Ned. Electric power systems: a first course. John Wiley & Sons, 2012.
- L. Thurner, A. Scheidler, F. Schäfer et al, pandapower - an Open Source Python Tool for Convenient Modeling, Analysis and Optimization of Electric Power Systems, in IEEE Transactions on Power Systems, vol. 33, no. 6, pp. 6510-6521, Nov. 2018.

---

class: end-slide, center
count: false

The end.
