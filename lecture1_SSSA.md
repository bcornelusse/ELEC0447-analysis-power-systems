class: middle, center, title-slide
count: false

# ELEC0447 — Analysis of electric power and energy systems

 Sinusoïdal steady-state analysis


<br><br>

Bertrand Cornélusse<br>
[bertrand.cornelusse@uliege.be](mailto:bertrand.cornelusse@uliege.be)

---

# What will we learn today?

- Recap of conventions
- Sinusoidal steady state analysis


You will be able to do exercises 2.1, 2.2, 2.4, 2.5, 2.9, 2.11, 2.12, 2.14, 2.16, 2.17, 2.18, 2.19 and 2.20 from the Ned Mohan's book.

---

class: middle

# Basics and conventions

---

## Power and energy

 - Power measures the rate of use of energy
 - It is expressed in Watt [W]: 1 W = 1 Joule/second
 - In an electric system, $$p(t) = u(t) \times i(t)$$
  - $u(t)$ is the voltage measured in volt [V], the line integral of the electric field between two points.
  - $i(t)$ is the current measured in amps [A]
  - $t$ is the time 
 - To measure energy in power systems, we use units ranging from a kWh (a microgrid) to a TWh (a country)
 - Devices have power ratings ranging from W to GW (although we generally speak in VA for ratings)

---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/S4O5voOCqAQ" frameborder="0" allowfullscreen></iframe>

The cyclist vs the toaster.

---

## Motor convention (or standard reference)

When using the motor convention to direct $u$ w.r.t. $i$, $p(t)$ represents the power **consumed** by a device (here a resistor): 

.center[.width-20[![](figures/motor_conv.png)]]

 - The power consumed can be < 0, = 0, or > 0 depending on the device
 - E.g. for a resistor we always have $p(t) \geq 0$
 - The **opposite** convention is the **generator convention**
 - We will sometimes use a mix of both conventions, based on intuition, so that in general we have few negative numbers: pay attention to the orientations! 

---

## Magnetic fields, etc.

Magnetic fields have a central role to model the behavior of equipment (lines, transformers, generators, etc.).

As this course will not be focused on modeling devices, but rather a system of devices, magnetic effects will often be highly abstracted (an inductance, or a turns ratio).

Let's just recall that 
- a magnetic field is due to charges in movement or magnetized materials
- it is measured in amps/meter (for $H$) or in Tesla (for $B$) when we capture the effect of the material (the $\mu\_0$ coefficient in the air)
- the magnetic flux ($\phi$ in weber) measures the magnetic field crossing a surface
- a time varying magnetic flux induces a voltage (Lenz), this is the fundamental principle behind transformers.

---

class: middle

# Sinusoidal steady state analysis

---

## Sinusoidal signals and phasor representation

Unless otherwise specified, we will always work with sinusoidal signals and in steady state:
$$y(t)= \sqrt{2} Y \cos(\omega t + \phi\_y).$$

$Y$ is the *rms* value of the signal, $\phi\_y$ its phase and $\omega$ its angular frequency.

At a specific frequency $f = \frac{\omega}{2\pi}$, the signal can be represented as a phasor
$$\bar{Y} = Y \angle \phi_y = Y e^{j \phi_y}$$

Phasors allow to work in the frequency domain, which is much more handy for computations.

*How do you get the time expression from the phasor?*

---

class: middle, center

.center[![](figures/Unfasor.gif)]
https://en.wikipedia.org/wiki/Phasor

---

## Impedance

Let $u(t)$ and $i(t)$ be the voltage and current across a one-port, respectively, in sinusoidal steady state and with the motor convention.

 - For a resistor, $u(t) = R i(t)$ hence $\bar{U} = R \bar{I}$
 - For a self, $u(t) = L \frac{di(t)}{dt}$ hence $\bar{U} = j\omega L \bar{I}$
 - For a capacitor, $i(t) = C \frac{du(t)}{dt}$ hence $\bar{I} = j\omega C \bar{U}$

The *impedance*, a complex number, generalizes this notion
$$Z = R + jX \ \ [\Omega]$$ 
such that $\bar{U} = Z \bar{I}$ with 

 - for a resistor, $Z = R$
 - for a self, $Z = jX = j\omega L$
 - for a capacitor, $Z = jX = -j\frac{1}{\omega C}$

---

## Impedance, admittance, etc.

The imaginary part of the impedance, $X$, is called reactance

The admittance $Y$ is the inverse of the impedance, expressed in Siemens:

$$Y = G + jB$$

- $G$ is the conductance
- $B$ is the susceptance

---

class: middle, center, black-slide

<iframe width="600" height="450" src="https://www.youtube.com/embed/zO7RZZW0wSQ" frameborder="0"  allowfullscreen></iframe>

A nice animation.

---

## Complex calculus

$$|Z| = \sqrt{R^2+X^2}$$
$$\angle Z = \arctan \frac{X}{R}$$
$$Z = \frac{\bar{U}}{\bar{I}} = \frac{{U}}{{I}} \angle (\phi\_u - \phi_i)$$


---

## Phasor diagrams

Plot the phasors in the complex plane!

.center.width-50[![](figures/phasor_diagram.png)]

Inductive or capacitive? Which is which?
.grid[
.kol-1-2[.center.width-40[![](figures/phasor_diagram_L.png)]]
.kol-1-2[.center.width-50[![](figures/phasor_diagram_C.png)]]]

---

## The notions of power

The complex power is defined as $$S = \bar{U}\bar{I}^*$$

Let $$\phi = \phi_u - \phi_i$$
then $$S = UI e^{j\phi} = P + jQ$$

- $P = UI \cos\phi$ is the active power, measured in watt
- $Q = UI \sin\phi$ is the reactive power, measured in var
- $\cos\phi$ is the power factor

Reactive power is, in general, undesirable. 

The apparent power is $|S| = UI$, measured in VA

---

## Useful formulas

$$P = RI^2 = \frac{U^2}{R}$$
$$Q = XI^2 = \frac{U^2}{X}$$
$$\tan \phi = \frac{Q}{P}$$
$$\cos \phi = \frac{P}{|S|}$$

The power factor does not tell you whether the system is leading or lagging
 - in an inductive system, $u(t)$ precedes $i(t)$, $i(t)$ is lagging, thus $Q > 0$ (motor convention)
 - in a capacitive system, this is the opposite (leading).


---

## Power factor compensation

.width-40[![](figures/pf_compensation_1.png)]

Produce some $Q$ to cancel out $\phi$.

*Example:* 

A 120V voltage source at 60 Hz that feeds a R-L load $1858.4 + j 1031.4 \ VA $



---

class: end-slide, center
count: false

The end.
