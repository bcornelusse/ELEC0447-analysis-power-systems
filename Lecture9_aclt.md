class: middle, center, title-slide
count: false

# Analysis of electric power and energy systems

Lecture 9: Transient Stability

<br><br>

Antonin Colot<br>
[antonin.colot@uliege.be](mailto:antonin.colot@uliege.be)

---

# Overview

- Classification power system stability (Reminder)
- Principle of transient stability
- Swing equation
- Practical Example
- Dynamic Security Assessment
- Nowadays

---

# Classification power system stability (Reminder)

 - Proposed definition:

<div class="warning" style='padding:0.01em; background-color:#F4FFFF; color:#20707E'>
<span>
<p style='margin-top:0.1em; margin-left:1em ; margin-bottom:0.1em; text-align:center'>
<b> Power system stability is the ability of an electric power system, for a given initial operating condition, to regain a state of operating equilibrium after being subjected to a physical disturbance, with most system variables bounded so that practically the entire system remains intact. [2] </b>
</p></span>
</div> 


<p align="center">
<img src=figures_aclt/ClassificationStability.gif width="650" height="250" />
</p>

.footnote[[1] Hatziargyriou, Nikos, et al. "Definition and classification of power system stability–revisited & extended." IEEE Transactions on Power Systems 36.4 (2020): 3271-3281.]

---

# Principle of transient stability

<p align="center">
<img src=figures_aclt/Principle_TS.png width="650" height="150" />
</p>

 - Consider a generator bus connected through a transformer to a infinite bus system ($\bar{V}_B = V_B$ is an ideal voltage source).
 - The mechanical power delivered through the shaft is $P_m$. 
 - The electrical power delivered to the grid is denoted $P_e$.
 - In steady-state, the synchronous machine is modelled as a constant voltage source 
 $E'\ e^{j\delta}$ behind its transient reactance $X'_d$.
 - Finally, $X_{tr}$ is the leackage reactance of the transformer.

---

## Reminder

Consider a simple radial system.

<p align="center">
<img src=figures_aclt/RadialSystem.png width="500" height="100" />
</p>

Assuming no transmission-line losses:

$$S_S = P_S + jQ_S = V_S e^{j \delta_S} \left(\frac{V_S e^{-j \delta_S} - V_R e^{-j \delta_R}}{X}\right) e^{j\frac{\pi}{2}}$$

If we define $\delta = \delta_S-\delta_R$, we have:

$$P_R = P_S = \frac{V_S V_R}{X_L}\sin \delta$$

$$Q_{R} = \frac{V_S V_R \cos \delta}{X_L} - \frac{V^2_R}{X_L}$$

$$Q_{S} = \frac{V_S^2}{X_L} - \frac{V_S V_R \cos \delta}{X_L}$$

---

The electrical power $P_e$ is expressed as follows:

$$P\_e = \frac{E' V\_B}{X\_{tr}+X'\_d + X\_L/2} \sin(\delta)$$

At equilibrium, $P_e = P_m$. For given reactances and voltage sources, one has:

$$\delta\_{eq} = \arcsin\left(P\_m \frac{X\_{tr}+X'\_d + X\_L/2}{E' V\_B}\right)$$

<p align="center">
<img src=figures_aclt/delta_P_m.png width="350" height="260" />
</p>

When we increase $P\_{m}$, the electrical angle at equlibrium also increases. The maximum value is reached for $\delta_{eq} = \frac{\pi}{2}$.

---

There exist <b> TWO </b> equilibrium points for $P_m \in [0,10)$. Only <b> ONE </b> for $P_m = 10$, and <b> NONE </b> for $P_m>10$. 

<b> Question: </b> What happens if $P_m>10$?

----

<p align="center">
<img src=figures_aclt/Angle_MechanicAnalogy.png width="300" height="180" />
</p>

In synchronous machines, the rotor rotates at the same angular speed as the magnetic field produced by the stator. If we denote $\omega_m$ the rotor angular speed and $\omega_s = 2\pi f_s$ the synchronous speed, then $\omega_m = \omega_s$. 

The field produced by the rotor and the stator tend to align. If they are not aligned, an electromechanical torque is produced. This misalignment is represented by the electrical angle. A greater angle induces a larger torque. <b> BUT </b> if the angle is too large, the machine loses synchronism and the torque becomes 0.

.footnote[[2] Lectures given by Prof. Thierry Van Cutsem https://thierryvancutsem.github.io/home/courses.html]

---

Consider this equation:

$$P\_e = \frac{E' V\_B}{X\_{tr}+X'\_d + X\_L/2} \sin(\delta)$$

with $E' = 1.1$, $V\_B = 1$, $X\_{tr} = 0.8$, $X'\_d = 0.4$ and various values of $X\_L = [0.5,1,3]$. 

<p align="center">
<img src=figures_aclt/P-delta.png width="350" height="260" />
</p>

---

Let us consider the following sequence of actions:
 1. Pre-fault conditions; the impedance between generators and the infinite bus system is $j 0.5$ pu.
 2. During-fault conditions; one line is short-circuited, the impedance becomes $j 3$ pu.
 3. Post-fault conditions; the short-circuit is cleared by disconnecting a line, the impedance becomes $j 1$ pu.

For the system to be stable, the system has to stabilize at $\delta = \delta_2$ after the fault occured. 

<em> We will now look at how the system moves from the equilibrium point $\delta_1$ to equilibrium point $\delta_2$ </em>

---
# Swing equation

Let us define the following quantities; $J_m$ is the moment-of-inertia of the rotational system, $T_m$ is the mechanical torque, $T_e$ is the electrical torque, $\omega_m$ is the rotor speed and $\delta_m$ the rotor angle (in mechanical radians). Using Newton's Second Law, one has:
$$J_m\frac{d^2\delta_m}{dt^2} = T_m-T_e$$

Multiplying both sides by $\omega_m$ (the rotor speed), one has:
$$\omega_m J_m \frac{d^2\delta_m}{dt^2} = P_m-P_e$$

We then define 
$$H\_{gen} = \frac{\frac{1}{2}J\_m \\omega\_{syn,m}^2}{S\_{rated,gen}} = \left\[\frac{kg \\cdot m^2 \\times 1/s^2}{kg \cdot m^2/s^3}\right\] = \left\[s\right\]$$

where $\\omega\_{syn,m}$ is the synchronous speed (in mechanical radians/s), $S\_{rated,gen}$ the nominal rated size of the generator.
$H\_{gen}$ is defined in seconds, and takes a value in a range of 3-11s for turbo-alternators, and in a 1-2s range for hydro generators.

---

One can write the swing equation by substituing $J\_m$ by $H\_{gen}$:

$$\left(\frac{\\omega\_{m}}{\\omega\_{syn,m}^2}\right)2 H\_{gen} \frac{d^2\\delta\_m}{dt^2} = P\_{m,gen,pu} - P\_{e,gen,pu}$$
where $P\_m$ and $P\_e$ are in per-unit of the generator MVA base. One can also write the equation in the system base $S\_{system}$:

$$\left(\frac{\\omega\_m}{\\omega\_{syn,m}^2}\right)2 H \frac{d^2\\delta\_m}{dt^2} = P\_{m,pu} - P\_{e,pu}$$
with 

$$H = H\_{gen} \left(\frac{S\_{rated,gen}}{S\_{system}}\right)$$

Finally, we make the reasonable assumption that $\\omega\_{m} \approx \\omega\_{syn,m}$, and we express everything in terms of electrical radians.

$$\left(\frac{2H}{\\omega\_{syn}}\right) \frac{d^2\\delta}{dt^2} = P\_{m,pu} - P\_{e,pu}$$

.footnote[[3] Mohan, N. (2012). Electric power systems: a first course. John Wiley & Sons.]

---

<b> What can we say about the swing equation? </b>

- If the mechanical power provided at the shaft $P\_m$ is greater than the electrical power transferred to the network $P\_e$, the machine accelerates $\frac{d^2\\delta}{dt^2} = \frac{d\\Delta\\omega}{dt} > 0$, where $\\Delta\\omega$ is the deviation from the synchronous speed $\\omega\_{syn}$.
- It decelerates if the electrical power is greater than the mechanical power. 
- The acceleration is proportional to the machine inertia $H$ = time it takes for the machine to reach its nominal speed if the mechanical power provided at the shaft is $S\_{system}$. 

<b> What is the inertia of PV panels? </b>

---

## Transient stability using Equal-Area Criterion

<b> Swing equation: </b>
$$\left(\frac{2H}{\\omega\_{syn}}\right) \frac{d^2\\delta}{dt^2} = P\_{m,pu} - P\_{e,pu}$$

Rearranging the terms and multiplying both sides by $d\\delta/dt$:
$$2\frac{d\\delta}{dt}\frac{d^2\\delta}{dt^2} = \frac{\\omega\_{syn}}{H}\left(P\_{m,pu}-P\_{e,pu}\right)\frac{d\\delta}{dt}$$

Applying change of variables $\\delta = \\theta$, and integrating both sides between $\\delta\_0$ and an arbitrary angle $\\delta$:
$$\int\_{\\delta\_0}^{\\delta} \left(2\frac{d\\theta}{dt}\frac{d^2\\theta}{dt^2}\right) dt = \frac{\\omega\_{syn}}{H}\int\_{\\delta\_0}^{\\delta} \left(P\_{m,pu}-P\_{e,pu}\right)d\\theta$$

Assume $\\delta\_0$ being an equilibrium point, <i> i.e. </i> $d\\delta/dt\|\_{\\delta = \\delta\_0} = 0$, we have:
$$\left(\frac{d\\delta}{dt}\right)^2 = \frac{\\omega\_{syn}}{H}\int\_{\\delta\_0}^{\\delta} \left(P\_{m,pu}-P\_{e,pu}\right) d\\theta$$

---

The left term $\left(\frac{d\\delta}{dt}\right)^2 = \\Delta\\omega^2$ represents the kinetic energy of the machine at an arbitrary angle $\\delta^*$ (with respect to the synchronous speed $\\omega\_{syn}$) $\rightarrow$ rotational kinetic energy: $\frac{1}{2} J \\omega^2$ with $J$ the moment-of-inertia and $\omega$ the angular speed. 

As long as $P\_{m,pu} > P\_{e,pu}$, the machine gains kinetic energy and accelerates. For the system to stabilize, it must exist an angle $\\delta\_{m}$ at which the kinetic energy becomes 0, and thus:
$$\int\_{\\delta\_0}^{\\delta} \left(P\_{m,pu}-P\_{e,pu}\right) d\\theta = 0$$

Let us consider the following system; at time $t$ and angle $\\delta\_0$, a short-circuit occurs and is cleared at time $t+t\_{cl}$ and angle $\\delta\_{cl}$ by tripping the line.

<p align="center">
<img src=figures_aclt/TransientStabilityEAC.png width="650" height="200" />
</p>

---

For a stable system, we highlighted that:

$$\int\_{\\delta\_0}^{\\delta} \left(P\_{m,pu}-P\_{e,pu}\right) d\\theta = 0$$

For our little example, one can write the same condition:

$$\\underbrace{\int\_{\\delta\_0}^{\\delta\_{cl}} \left(P\_{m,pu}-P\_{e,fault,pu}\right) d\\theta}\_{\\text{Area A}} - \\underbrace{\int\_{\\delta\_{cl}}^{\\delta\_{m}} \left(P\_{e,post-fault,pu}-P\_{m,pu}\right) d\\theta}\_{\\text{Area B}} = 0$$

During the first part (Area A), the machine accelerates. After the fault (Area B), the machine decelerates and the net acceleration becomes 0. At angle $\\delta\_{m}$, there is still a mismatch between the electrical power and the mechanical power, thus the machine swings back (from $\delta\_{m}$ to $\delta\_{2}$).

<p align="center">
<img src=figures_aclt/SwingsBack.png width="400" height="180" />
</p>

---

Without any damping (kinetic energy losses), the system oscillates indefinitely between angle $\\delta\_2$ and $\\delta\_m$.

<p align="center">
<img src=figures_aclt/RotorOscillation.png width="400" height="280" />
</p>

However, in a real system, the damping would cause the machine to settle down at an angle $\\delta\_1$ (new equilibrium point).

Synchronous machines have <i> damper windings </i>. In perfect steady state, the magnetic fields produced by both the stator and the rotor are fixed relative to the rotor so there is no current in the dampers. On the other hand, if the rotor moves with respect to the magnetic field, the current induced in the dampers create a damping torque according to Lenz's law.

---
## Critical Clearing Angle

Let us come back to our definition of stability for our little system:

$$\\underbrace{\int\_{\\delta\_0}^{\\delta\_{cl}} \left(P\_{m,pu}-P\_{e,fault,pu}\right) d\\theta}\_{\\text{Area A}} - \\underbrace{\int\_{\\delta\_{cl}}^{\\delta\_{m}} \left(P\_{e,post-fault,pu}-P\_{m,pu}\right) d\\theta}\_{\\text{Area B}} = 0$$

<b> What are the conditions to ensure there exists $\\delta\_{cl}$ such that Area A = Area B?</b>

We introduce the concept of critical clearing angle $\\delta\_{cct}$. Past this point, Area A will always be greater than Area B, such that the system cannot stabilize. We associate the critical clearing time $CCT$ to the critical clearing angle, <i> i.e. </i> the maximum time allowed to clear the fault before the system gets unstable. 

---

<b> Visual representation </b>

<p align="center">
<img src=figures_aclt/CCT_example.png width="400" height="200" />
</p>

<b> Mathematical formulation </b>

$$\\underbrace{\int\_{\\delta\_0}^{\\delta\_{cct}} \left(P\_{m,pu}-P\_{e,fault,pu}\right) d\\theta}\_{\\text{Area A}} - \\underbrace{\int\_{\\delta\_{cct}}^{\\delta\_{max}} \left(P\_{e,post-fault,pu}-P\_{m,pu}\right) d\\theta}\_{\\text{Area B}} = 0$$

One has to determine the angle $\\delta\_{max}$ such that $P\_{e,post-fault} = P\_{m}$, and the angle $\\delta\_{0}$ such that $P\_{e,pre-fault} = P\_{m}$. Then solving this equation gives $\\delta\_{cct}$. Finally, using the <b> swing equation </b>, one can determine the critical clearing time $CCT$, <i> i.e. </i> the time needed to reach the angle $\\delta\_{cct}$.

---
# Practical Example

Let us consider the following system:
<p align="center">
<img src=figures_aclt/InitialSystem.png width="700" height="220" />
</p>

and the following data:
$$X\_d' = 0.3, X\_{tr} = 0.5, X\_{l} = 1, X\_{21} = 0.5, X\_{22} = \frac{1}{6}, X\_{23} = \frac{1}{3}$$ 
and
$$\bar{E}\_{t} = 1e^{j \pi/6}, \bar{E}\_{B} = 1e^{j0}$$

---
## Equivalent 
We can derive the following equivalent:
<p align="center">
<img src=figures_aclt/InitialSystemEq.png width="700" height="220" />
</p>

where 
$$X\_T = X\_{tr} + X\_{d}' + \frac{X\_{l}\left(X\_{21}+X\_{22}+X\_{23}\right)}{X\_{21}+X\_{22}+X\_{23}+X\_{l}} = 1.3$$

The power transfer from the machine to the infinite-bus system takes the following form:
$$P = \frac{E' E\_{B}}{X\_{T}} \sin \\delta$$

---
## Find $\bar{E}'$, $P\_e$ and $P\_m$
 1. Current from $\\bar{E}\_{t}$ to $\\bar{E}\_{B}$
 $$\\bar{I}\_{t\\rightarrow B} = \frac{\\bar{E}\_{t}-\\bar{E}\_{B}}{jX\_{T} - jX\_{d}'}$$ 
 2. $\bar{I}\_{t\\rightarrow B}$ is the same as the one from $\\bar{E'}$ to $\\bar{E}\_{t}$
 $$\bar{E}' = j X\_{d}' \bar{I}\_{t\\rightarrow B} + \bar{E}\_{t} = 1.05095 e^{j 38.2057/180}$$
 3. Find $P\_e$
 $$P\_e = \frac{1.05095\ 1\ \sin(38.2057/180)}{1.3} = 0.5$$
 4. Initially, the system is at equilibrium.
 $$P\_m = P\_e = 0.5$$

In the following, we will compute the maximum power outputs for three different conditions: Pre-fault, During-Fault and Post-Fault. It will allow us to determine the 3 different $P-\delta$ curves.

---
## Pre-fault condition

----

<b> We compute the maximum power output while assuming $E'$ does not change. </b>

<em> If the transient stability study lasts a second or less, it is reasonable to consider, as a first-order approximation, that the exciter of the synchronous machine cannot respond in such short amount of time. Hence, $E'$ does not change</em>

----

Maximum power output:

$$\hat{P}\_{e,bf} = \frac{E'E\_{B}}{X\_{T}} = 0.808$$

---
## During-fault condition

A short-circuit occurs between lines $22$ and $23$. The circuit topology changes and is depicted below. 

<p align="center">
<img src=figures_aclt/DuringFault.png width="600" height="380" />
</p>

---

We can derive the following Thevenin's equivalent

<p align="center">
<img src=figures_aclt/TheveninEquiv.png width="400" height="160" />
</p>

where 

$$\bar{E}\_{th} = \bar{E'} \frac{X\_{21} + X\_{22}}{X\_{d}+X\_{tr} + X\_{21} + X\_{22}} = 0.478 e^{j 38.206/180}$$
and 
$$X\_{th} = \frac{1}{\frac{1}{X\_d' + X\_{tr}}+\frac{1}{X\_{21}+X\_{22}}} = 0.364$$

and then get the maximum power output:
$$\hat{P}\_{e,df} = \frac{E\_{th}E\_{B}}{X\_{th} + X\_{l}} = 0.35$$

---
## Post-fault condition

The line $2$ is tripped to clear the short-circuit.

The impedance of the path connecting the machine to the infinite-bus system becomes $X\_d' + X\_{tr} + X\_{l} = 1.8$. 

The maximum power output is:
$$\hat{P}\_{e,pf} = \frac{E'E\_{B}}{X\_d' + X\_{tr} + X\_{l}} = 0.584$$ 

---

The final $P-\\delta$ curves are shown here under:

<p align="center">
<img src=figures_aclt/P-delta-example.png width="500" height="380" />
</p>

with 

$$\\delta\_1 = \arcsin \left(\frac{P\_m}{\hat{P}\_{e,bf}}\right) = 0.667, \\delta\_2 = \arcsin \left(\frac{P\_m}{\hat{P}\_{e,pf}}\right) = 1.028, \\delta\_{max} = 2.114$$

---
## Critical clearing angle $\\delta\_{cct}$

$$\\underbrace{\int\_{\\delta\_0}^{\\delta\_{cct}} \left(P\_{m,pu}-P\_{e,fault,pu}\right) d\\theta}\_{\\text{Area A}} = \\underbrace{\int\_{\\delta\_{cct}}^{\\delta\_{max}} \left(P\_{e,post-fault,pu}-P\_{m,pu}\right) d\\theta}\_{\\text{Area B}}$$

<b> Area A </b>
$$
\\begin{aligned}
\int\_{\\delta\_{0}}^{\\delta\_{cct}} \left(P\_{m,pu}-P\_{e,fault,pu}\right) d\\theta &= P\_{m,pu} \left(\\delta\_{cct} - \\delta\_{0}\right) - \int\_{\\delta\_{0}}^{\\delta\_{cct}} \\hat{P}\_{e,df} \\sin \\theta d\\theta \\\
&=P\_{m,pu} \left(\\delta\_{cct} - \\delta\_{0}\right) + \\hat{P}\_{e,df} \left(\\cos \\delta\_{cct} -\\cos \\delta\_{0}\right) \\\ 
\\end{aligned}
$$

<b> Area B </b>
$$
\\begin{aligned}
\int\_{\\delta\_{cct}}^{\\delta\_{max}} \left(P\_{e,pf,pu}-P\_{m,pu}\right) d\\theta &= P\_{m,pu} \left(\\delta\_{cct} - \\delta\_{max}\right) - \int\_{\\delta\_{cct}}^{\\delta\_{max}} \\hat{P}\_{e,pf} \\sin \\theta d\\theta \\\
&=P\_{m,pu} \left(\\delta\_{cct} - \\delta\_{max}\right) + \\hat{P}\_{e,pf} \left(\\cos \\delta\_{cct} -\\cos \\delta\_{max}\right) \\\ 
\\end{aligned}
$$

---

<b> Equal-area criterion </b>

$$
\\begin{aligned}
\text{Area A} &= \text{Area B}\\\
P\_{m,pu} \left(\\delta\_{max} - \\delta\_{0}\right) + \\hat{P}\_{e,df} \left(\\cos \\delta\_{cct} -\\cos \\delta\_{0}\right) &= \\hat{P}\_{e,pf} \left(\\cos \\delta\_{cct} -\\cos \\delta\_{max}\right) \\\
\\end{aligned}
$$

We can find out the critical clearing angle.

$$
\\cos \\delta\_{cct} = \frac{P\_{m,pu} \left(\\delta\_{0} - \\delta\_{max}\right) + \\hat{P}\_{e,df} \\cos \\delta\_{0} - \\hat{P}\_{e,pf} \\cos \\delta\_{max}}{\\hat{P}\_{e,df} - \\hat{P}\_{e,pf}} 
$$

---

<p align="center">
<img src=figures_aclt/P-delta-example-cct.png width="500" height="380" />
</p>

The purple star corresponds to $\\delta\_{cct} = 0.8938$, and the dashed purple line shows the evolution of the angle $\\delta$. Even without damping, the system stabilizes at $\delta = \delta\_{max}$ since the kinetic energy reaches 0 at that point ($\Delta \omega^2 = 0$)

---
## Estimation of the critical clearing time $CCT$

In order to find the critical clearing time, one would need to solve the swing equation:

$$\left(\frac{2H}{\\omega\_{syn}}\right) \frac{d^2\\delta(t)}{dt^2} = P\_{m,pu} - P\_{e,pu}(\\delta(t))$$

where $P\_{e,pu}(\\delta(t))$ is a non-linear function depending on $\\delta$; $P\_{e,pu}(\\delta(t)) = K(t) \sin (\\delta(t))$, and with $K$ changing non-continuously with time. We would need to solve a non-linear differential equation, which is not an easy task!

Thus, let us assume that the acceleration $\frac{d^2\\delta(t)}{dt^2}$ is constant over time. We have:

$$\\delta\_{cct} = \\delta\_1 + \Delta \omega\_0\  CCT +a \frac{CCT^2}{2}$$
where $a$ is the constant acceleration and $\Delta \omega\_0$ the initial speed assumed to be 0.
Let us assume two cases:
 1. We pick the maximum acceleration for angles in $[\\delta\_1,\\delta\_{cct}]$.
 2. We pick the minimum acceleration for angles in $[\\delta\_1,\\delta\_{cct}]$.

---

From the following figure

<p align="center">
<img src=figures_aclt/P-delta-example-cct.png width="400" height="280" />
</p>

it is clear that the acceleration is maximum for $\\delta = \\delta\_1$, and minimum for $\\delta = \\delta\_{cct}$ for $\\delta \in [\\delta\_1,\\delta\_{cct}]$ (larger power mismatch when $\\delta = \\delta\_1$ and smaller for $\\delta = \\delta\_{cct}$).

We have:
$$a\_{min} = \frac{\\omega\_{syn}}{2H}\left(P\_{m,pu} - \hat{P}\_{e,df}\sin \\delta\_{cct}\right)$$
$$a\_{max} = \frac{\\omega\_{syn}}{2H}\left(P\_{m,pu} - \hat{P}\_{e,df}\sin \\delta\_{1}\right)$$

---

With $H = 4.5$s, we can derive a lower and an upper bound for the critical clearing time $CCT$.

$$CCT\_{max} = \sqrt{\frac{2\left(\\delta\_{cct}-\\delta\_{1}\right)}{a\_{min}}} = \sqrt{\frac{2\left(0.8938-0.667\right)}{7.93}} = 239 \text{ms}$$

$$CCT\_{min} = \sqrt{\frac{2\left(\\delta\_{cct}-\\delta\_{1}\right)}{a\_{min}}} = \sqrt{\frac{2\left(0.8938-0.667\right)}{9.89}} = 214 \text{ms}$$

If the actual clearing time is denoted $t^*$, we can conclude that:

1. If $t^*>CCT\_{max}$, the system is unsafe!
2. If $t^*<CCT\_{min}$, the system is safe!
3. If $CCT\_{min}<t^*<CCT\_{max}$, we have no guarantee if the system is safe or not.

---
## Extension on dynamics

<b> Swing equations with damping coefficient </b>

$$\frac{d\Delta \omega(t)}{dt} = \frac{1}{2H}\left(P\_m - P\_{e,max}(t) \sin (\delta(t)) - D \Delta \omega(t) \right)$$
$$\frac{d\delta(t)}{dt} = \omega\_0 \Delta \omega(t)$$

Euler discretization
$$\Delta \omega\_{t+1} = (1-\tau \frac{D}{2H})\Delta \omega\_{t} + \frac{\tau}{2H}\left(P\_m-P\_{e,max}^{k \tau}\sin (\delta\_{t})\right)$$
$$\delta\_{t+1} = \delta\_{t} + \tau\omega\_0\Delta \omega\_t$$
where $\tau$ is the time step and where we explicitly denote that $P\_{e,max}^{k \\tau}$ is changing over time in a discretize fashion (pre-fault$\rightarrow$during-fault$\rightarrow$post-fault) through the superscript $k \tau$. 

---

<b> Results without damping ($t\_{cl} = 0.214 s \leq CCT$)</b>

<p align="center">
<img src=figures_aclt/P-dynamics.png width="500" height="380" />
</p>

The fault is cleared after 214 ms (lower bound on the clearing time). As expected from previous calculations, the system is safe.   

---

<b> Results with damping ($t\_{cl} = 0.214 \leq CCTs$)</b>

<p align="center">
<img src=figures_aclt/P-dynamics_bis.png width="500" height="380" />
</p>

The fault is cleared after 214 ms (lower bound on the clearing time). As expected from previous calculations, the system is safe. The damping adds energy dissipation, which allows the system to stabilize around $\delta\_2 = 1.028$

---

<b> Results without damping ($t\_{cl} = 0.239 s \geq CCT$)</b>

<p align="center">
<img src=figures_aclt/P-dynamics_failed.png width="500" height="380" />
</p>

The fault is cleared after 239 ms (upper bound on the clearing time). The machine loses synchronism. 

---

<b> Results with damping ($t\_{cl} = 0.239 s \geq CCT$)</b>

<p align="center">
<img src=figures_aclt/P-dynamics_bis_failed.png width="500" height="380" />
</p>

The fault is cleared after 239 ms (upper bound on the clearing time). The system is stable thanks to the damping effect (energy dissipation). 

---

# Dynamic Security Assessment (DSA)

- Based on fast time domain contingency simulations.
- Study main stability issues such that: Voltage, Transient and Small-Signal (not covered throughout this course).
- Start from actual and future operating points.
- Has to be visual for the operators $\rightarrow$ show the type of instability, where it comes from and even possible solutions. 

Main question that DSA should answer: 

<b> Imagine a set of major, yet credible contingencies, can the system resist such events without jeopardizing its integrity?</b>

If yes, then the states are determined secure $\rightarrow$ the system trajectories do not bring the states inside an unsafe set.

---

There are basically two types of analysis: off-line and on-line. 

<b> Off-line analysis </b>

- They are subjected to forecast errors $\rightarrow$ system security cannot be taken for granted. 

- But they can be performed with no constraints on time (performed day-ahead in order to set up a recommended operating schedule)

<b> On-line analysis </b>

- Not prone to forecast errors since they are based on real-time information.

- But need to be fast.

.footnote[[4] Kerin, U., Balaurescu, R., Lazar, F., Krebs, R., & Balasiu, F. (2012, July). Dynamic security assessment in system operation and planning—First experiences. In 2012 IEEE Power and Energy Society General Meeting (pp. 1-6). IEEE.]

---

## Voltage stability assessment

- Mainly static analyses.
- Goal is to ensure a sufficient load power margin.
- List of contingencies: all single-component outages.

<p align="center">
<img src=figureslw/pfonc-sev.png width="500" height="300" />
</p>

.footnote[[5] Lecture of last year presented by Prof. Louis Wehenkel https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture9.md#20]

---

## Transient stability assessment

- We want to avoid that:

<p align="center">
<img src=figures_aclt/P-dynamics_failed.png width="500" height="380" />
</p>

- Simulations with different three-phase short-circuits at various locations.
- And with different clearing schemes!
- Very time consuming computations.

---

# Nowadays

- Integration of large off-shore wind parks, and PV systems without reinforcing the network.
- Large power plants are decommissioned, and conventional generators are no longer accepted in urban areas.
- New units are built far away from load centers.
- Hard to build new lines because of public debates and environmental constraints.

<em> This leads to a weaker electrical system, more prone to stability issues.</em>

There's a need for tools that can quickly perform security assessment to guarantee a secure system. 

---

## Few  examples

- For static analyses, we rely on power flow solvers to estimate the state of the system. 
- With increasing penetration of RES, probabilistic approaches are envisioned to perform risk assessment. 
- But traditional power flow solvers based on Newton-Raphson methods are too slow.
- Usage of AI tools to derive approximate solutions of the power flow equations.

<i> Donon, B., Clément, R., Donnot, B., Marot, A., Guyon, I., & Schoenauer, M. (2020). Neural networks for power flow: Graph neural solver. Electric Power Systems Research, 189, 106547. </i>

<p align="center">
<img src=figures_aclt/GNS.png width="340" height="220" />
</p>

---

## Few examples (cont'd)

- For dynamic analyses, we study the time-evolution of a power system trajectory (e.g. internal angle in transient stability)

- It requires solving the differential-algebraic equations for multiple scenarios (different short-circuit locations, different clearing schemes).

- Usage of reachability analysis techniques: gives the reach set, i.e., the set that contains all possible system trajectories. 

<i> Chen, Y. C., & Dominguez-Garcia, A. D. (2012). A method to study the effect of renewable resource variability on power system dynamics. IEEE Transactions on Power Systems, 27(4), 1978-1989. </i>

<p align="center">
<img src=figures_aclt/ReachAn.png width="600" height="240" />
</p>

---
class: end-slide, center
count: false

The end.
