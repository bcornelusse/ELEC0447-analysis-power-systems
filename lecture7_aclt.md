class: middle, center, title-slide
count: false

# Analysis of electric power and energy systems

Lecture 7: Voltage regulation and voltage instability

<br><br>

Antonin Colot<br>
[antonin.colot@uliege.be](mailto:antonin.colot@uliege.be)

---

# Overview

- Concept of stability
  - General concept
  - In power systems
- Why do we need stability?
- Voltage instability and voltage collapse 
  - Impact of power flows on voltages
  - Concept of nose curve
  - Examples of voltage instabilities
- (Some) counter-measures
  - Network Reinforcement
  - Voltage regulation
- Impact of renewable energy resources (RES)
  - Reverse power flows in distribution systems
  - Duck Curve
- What did we learn?

---

# Concept of stability
## General concept

 - Multiple definitions for different classes of stability
 - One of them is: 

<div class="warning" style='padding:0.01em; background-color:#F4FFFF; color:#20707E'>
<span>
<p style='margin-top:0.1em; margin-left:1em ; margin-bottom:0.1em; text-align:center'>
<b> If a system has the property that it will get back into the equilibrium state again after moving away from its equilibrium state, then it is stable. [1] </b>
</p></span>
</div>

 <p align="center">
 <img src=figures_aclt/ConceptOfStability.png width="450" height="200" />
 </p>

.footnote[[1] Keviczky, László, et al. "Stability of linear control systems." Control Engineering (2019): 197-239.]

---

## In power systems 

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

.footnote[[2] Hatziargyriou, Nikos, et al. "Definition and classification of power system stability–revisited & extended." IEEE Transactions on Power Systems 36.4 (2020): 3271-3281.]

---

# Why do we need stability?


## Key points

 - We often take electricity as a simple commodity.
 - But the electric power system is one of the most complex and largest man-made system.
 - The chances of system failures are very high taking into account the impact of external factors and rapid changes in system's state.
 - However, power systems are very reliable (operated 24h/24h 7d/7d and only few hours of power outages per year!).
 - But when instabilities occur, it can lead to black-outs with huge financial and societal consequences.

---

## Tokyo 1987

 - Unexpected load increase and presence of constant power devices (air conditioners) led to a voltage collapse.

<p align="center">
<img src=figures_aclt/TokyoCollapse.png width="300" height="350" />
</p>

<div class="warning" style='padding:0.01em; background-color:#F4FFFF; color:#20707E'>
<span>
<p style='margin-top:0.1em; margin-left:1em ; margin-bottom:0.1em; text-align:center'>
<b> 8 GW lost </b> and <b>2.8M customers impacted</b>
</p></span>
</div>
.footnote[[3] T. Ohno and S. Imai, "The 1987 Tokyo Blackout," 2006 IEEE PES Power Systems Conference and Exposition, Atlanta, GA, USA, 2006, pp. 314-318, doi: 10.1109/PSCE.2006.296325.

[4] A. Kurita and T. Sakurai, "The power system failure on July 23, 1987 in Tokyo," Proceedings of the 27th IEEE Conference on Decision and Control, Austin, TX, USA, 1988, pp. 2093-2097 vol.3, doi: 10.1109/CDC.1988.194703.]  

---

## Canada/Northeast USA 2003

 - Initial problem: not enough reactive power reserve. Hot weather and large consumption led to transmission lines overloading and eventually sagging into trees, further deteriorating the initial problem.
 - A cascading event caused the tripping of hundreds of lines and generating units.

<p align="center">
<img src=figures_aclt/USABlackOut.png width="280" height="320" />
</p>

<div class="warning" style='padding:0.01em; background-color:#F4FFFF; color:#20707E'>
<span>
<p style='margin-top:0.1em; margin-left:1em ; margin-bottom:0.1em; text-align:center'>
<b> 63 GW lost </b> and <b> 50M customers impacted </b> and <b> Estimated cost above $5 Billion </b>
</p></span>
</div>

.footnote[[5] Nice videos https://www.youtube.com/watch?v=nd3teNgUq8E, https://www.youtube.com/watch?v=KciAzYfXNwU]

---

## Europe 2004

 - Disconnection of a transmission line in Germany for the transport of a ship approved by the local TSO.
 - The local TSO approved to advance the disconnection later that day, but the commercial flows remained unchanged.
 - Some lines were critically loaded because of the line disconnection and a fast increase of load consumption led to a cascading event.
 - European interconnected network has been split into 3 islands.

<p align="center">
<img src=figures_aclt/EuropeBlackOut.png width="280" height="200" />
</p>

<div class="warning" style='padding:0.01em; background-color:#F4FFFF; color:#20707E'>
<span>
<p style='margin-top:0.1em; margin-left:1em ; margin-bottom:0.1em; text-align:center'>
<b> 14.5 GW lost </b> and <b> 15M customers impacted </b>
</p></span>
</div> 

.footnote[[6] Chunyan Li, Yuanzhang Sun and Xiangyi Chen, "Analysis of the blackout in Europe on November 4, 2006," 2007 International Power Engineering Conference (IPEC 2007), Singapore, 2007, pp. 939-944.
[7] Illustrative video https://www.youtube.com/watch?v=A30DdnsICuw] 
 
---

## Brazil 2023

 - We still don't know the root causes!

<div class="warning" style='padding:0.01em; background-color:#F4FFFF; color:#20707E'>
<span>
<p style='margin-top:0.1em; margin-left:1em ; margin-bottom:0.1em; text-align:center'>
<b> 19 GW lost </b>
</p></span>
</div> 

***

 - Every time a black-out happened, lessons have been learned, and new rules have been put in place.
 - Nonetheless, due to the system complexity, new complex phenomena occur that power system engineers try to understand.
 - In the following, we'll dive into the mechanisms of voltage instability. 

---

# Voltage instability and voltage collapse

## Impact of power flows on voltages 

Consider a simple radial system.

<p align="center">
<img src=figures_aclt/RadialSystem.png width="700" height="150" />
</p>

Assuming no transmission-line losses:

$$S_S = P_S + jQ_S = V_S e^{j \delta_S} \left(\frac{V_S e^{-j \delta_S} - V_R e^{-j \delta_R}}{X}\right) e^{j\frac{\pi}{2}}$$

$$S_R = P_R + jQ_R = V_R e^{j \delta_R} \left(\frac{V_S e^{-j \delta_S} - V_R e^{-j \delta_R}}{X}\right) e^{j\frac{\pi}{2}}$$

---

If we define $\delta = \delta_S-\delta_R$, we have:

$$P_R = P_S = \frac{V_S V_R}{X_L}\sin \delta$$

$$Q_{R} = \frac{V_S V_R \cos \delta}{X_L} - \frac{V^2_R}{X_L}$$

$$Q_{S} = \frac{V_S^2}{X_L} - \frac{V_S V_R \cos \delta}{X_L}$$

<b> Question:</b> What is the sign of $Q_S$ if $V_S>V_R$. What about $Q_R$?

***

From the expression of $Q_{R}$, dividing both sides by $\frac{V_R^2}{X_L}$, we get:

$$\frac{V_R}{V_S} = \cos \delta \left(\frac{1}{1+\frac{Q_R}{V^2_R/X_L}}\right)$$

Assuming $P>>0$ and $V_R \approx V_S \approx 1$, it leads to $\delta >> 0 \rightarrow \cos \delta << 1$.

<b> Question:</b> What would be the sign of $Q_R$ to keep $\frac{V_R}{V_S}\approx 1$?

---

Consider the following radial system, and the associated phasor diagram for which we consider $V_R = 1 e^{j0}, V_S = 1 e^{j\delta}$.

<p align="center">
<img src=figures_aclt/RadialSystem2.png width="600" height="200" />
</p>

Considering Kirchoff's Laws, one has:
$$\bar{V}_S = \bar{V}_R + j X_L \bar{I} \Rightarrow \bar{I} =  \frac{e^{j \delta}-1}{j X_L} = \frac{2 \sin(\delta/2)}{X_L} e^{j(\delta/2)}$$

As $\bar{I}$ is leading $\bar{V}_R$, $Q_R = |\bar{V}_R| |\bar{I}| \sin(-\delta/2)$ is negative. $Q_S$ is positive and one can write:

$$Q_S = -Q_R$$

<b>The larger $\delta \rightarrow P_{s \rightarrow r}$, the larger $Q_R$ and $Q_S$ to maintain $V_R = V_S = 1$</b>

---

<b> Question:</b> Where does the reactive power go?

 - Total reactive power loss: 
$$Q_S-(-Q_S) = 2 Q_S$$
 - Line current: 
$$\bar{I} = \frac{2 \sin(\delta/2)}{X_L} e^{j(\delta/2)}$$
 - Reactive power consumed by the line: 
$$X_L |\bar{I}|^2 = \frac{4}{X_L} \sin(\delta/2)^2 = 2 Q_S$$

---

## Key points


 - For HV systems, we usually assume: 
 $P_{s \rightarrow r} \propto (\delta_s - \delta_r)$
 - And $Q_{s \rightarrow r} \propto (V_s-V_r)$

 - Lines are mostly inductive so they consume reactive power.

 - Therefore, voltage control is done locally to avoid transferring reactive power over long distances.

---

## Concept of nose curve

Consider again the following simple radial system.

<p align="center">
<img src=figures_aclt/RadialSystem.png width="700" height="150" />
</p>

Consider $Q_R = 0 \Rightarrow \frac{V_S V_R \cos \delta}{X_L} - \frac{V^2_R}{X_L} = 0 \Rightarrow V_S \cos \delta = V_R$

We know $P_R = \frac{V_SV_R}{X_L}\sin \delta$, substituing the previous results in the expression of $P_R$ gives:
$$P_R = \frac{V_S^2}{X_L}\sin \delta \cos \delta = \frac{V_S^2}{2 X_L}\sin (2\delta)$$

We can determine the maximum transmissible power by setting the partial derivative to 0:

$$\frac{\partial P_R}{\partial \delta}(\delta^{max}) = \frac{V_S^2}{X_L}\cos (2\delta^{max}) = 0 \Rightarrow \delta^{max} = \frac{\pi}{4}$$

---

Replacing $\delta$ by $\delta^*$ in the equation of $P_R$, we have:

$$P_{R}^{max} = \frac{V_S^2}{2 X_L}$$ 

and 

$$V_R \approx 0.7 V_S$$

<b> Question:</b> How can we increase the maximum transmissible power through a line?

***

One can derive a relationship such that $\frac{V_R}{V_S} = f(\frac{P_R X_L}{V_S^2})$. Consider $y = \frac{V_R}{V_S}$ and $x = \frac{P_R X_L}{V_S^2}$, one has (trust me):

$$y = \sqrt{\frac{1}{2}\pm \sqrt{\frac{1}{4}-x^2}}$$

We verify that $y$ has a unique solution when $x = \frac{1}{2} \Rightarrow P_R = \frac{V_S^2}{2 X_L}$, which is the nose of the curve. There is no solution for $P_R > \frac{V_S^2}{2 X_L}$ and two solutions for $P_R < \frac{V_S^2}{2 X_L}$.

---

Let us consider different load characteristics:
$$P_{constant} \Rightarrow P_R = C_P \Rightarrow x = c_P$$

$$I_{constant} \Rightarrow \frac{P_R}{V_R} = C_I \Rightarrow y = c_I x$$

$$Z_{constant} \Rightarrow \frac{P_R}{V^2_R} = C_Z \Rightarrow y = c_Z \sqrt{x}$$

The operating point is where the load characteristic crosses the <e> PV curve </e>.
<p align="center">
<img src=figures_aclt/NoseCurve.png width="350" height="260" />
</p>
<b> Question:</b> Where does that shape come from?

---

$$P_R = V_R I \cos{\phi} = \frac{V_SV_R}{X_L}\sin \delta$$

Let us consider $\cos{\phi} = 1$ (unity power factor), and $X_L=1$ as well as $V_S=1$.

$$I = \frac{V_S}{X_L}\sin \delta = \sin \delta$$

$$Q_S = \frac{V_S^2}{X_L} - \frac{V_S V_R \cos \delta}{X_L} = 1-V_R \cos \delta$$

Since $Q_R = 0$, you know that $Q_S = X_L I^2 = I^2 \Rightarrow \frac{-I^2+1}{\cos \delta} = V_R$. 

Consider the Taylor expansion of $\sin \delta \approx \delta$ and $\cos \delta \approx 1-\frac{\delta^2}{2}$ for $\delta \approx 0$, we have 

$$V_R \approx \frac{(1-I^2)}{(1-I^2)+I^2/2}$$

---

<p align="center">
<img src=figures_aclt/NoseCurveApprox.png width="550" height="280" />
</p>

Since $I=\sin \delta \leq 1$, which implies that $(1-I^2) \geq 0$ and therefore $V_R$ decreases when $I$ increases. But after a given value of $I$, $V_R$ decreases faster than $I$ increases. Since $P_R = V_R I \cos{\phi}$, there is a maximum power transmissible.  

It does so because the line is inductive, and thus consumes reactive power. The larger the current, the larger the reactive power consumed by the line, which pulls the voltage down.

<b> Question:</b> Is that everything we need to know about nose curves?

---

<b> NO </b>

When you consider $\cos \phi \neq 1$ (the load consumes or produces reactive power), you get more complex nose curves [8].

<p align="center">
<img src=figures_aclt/TrueNoseCurve.png width="350" height="280" />
</p>

The ideas previously developed still stand, except that now the load can:
- <em> improve </em> the voltage profile by providing reactive power and thus compensating the reactive power consumed by the line, 
- or <em> worsen </em> it by further consuming reactive power.

.footnote[[8] Van Cutsem, T., & Vournas, C. (2007). Voltage stability of electric power systems. Springer Science & Business Media.]

---

## Key points

- There's a maximum transmissible power ($P_{R}^{max} = \frac{V_S^2}{2 X_L}$ for load with $\cos \phi = 1$).
- Inductive character of the line which consumes reactive power (influence of $X_L$)

<em> How to increase $P_{R}^{max}$?</em>

  - By increasing the source voltage $V_S$,
  - By decreasing $X_L$ (adding lines in parallel),
  - By producing reactive power at the load side to compensate for the reactive power consumed by the line. 

---

## Examples of voltage instabilities

<em> Long-term instabilities </em>

On-load tap changers (OLTCs) change the turn ratio of the transformers feeding the distribution systems to keep the voltages on the secondary side as close as possible to a given setpoint. 

Let us consider the following circuit, where the primary side of the transformer is the high voltage network, and the secondary side is the low/medium voltage network. 

The load on the secondary side is represented by a constant conductance $G$, consuming active power. 

The voltage on the primary side is controlled by a synchronous generator. $V_g$ is kept constant as long as the reactive power limits of the generator are not reached.

<p align="center">
<img src=figures_aclt/OLTC.png width="380" height="170" />
</p>
 
---

We assume an ideal transformer: $\frac{V}{V_2} = r$, $\frac{I_2}{I} = r$. 

The load characteristic seen from the primary side becomes $P_G = G\left(\frac{V}{r}\right)^2$, with $P_G$ the power consumed by the conductance $G$. 

Now, imagine one wants to keep $V_2 = V_2^o$, if $V \searrow  \Rightarrow r \searrow$. Indirectly, by decreasing $r$, the OLTC tries to restore the load (since it increases $V_2$ and $P_G = G V_2^2 = G\left(\frac{V}{r}\right)^2$).

Two different scenarii:

1) $\frac{V}{r}$ converges towards $V_2^o$, the load is restored.

2) $\frac{V}{r}$ never converges towards $V_2^o$ and $V$ collapses.

---

Imagine a disturbance leading to a decrease in the maximum transmissible power.

<p align="center">
<img src=figures_aclt/PVcurvestable.png width="350" height="280" />
<img src=figures_aclt/PVcurveunstable.png width="350" height="280" />
</p>

1) Left figure shows $P_G$ is recovered after two tap changes.

2) Right figure shows $P_G$ is never recovered, and the voltage collapses.

Scenario 2) is a typical case of <b> Long-term Voltage Stability </b>.

The disturbance can be the tripping of a line (as it is the case here), which leads to $X_L \nearrow$ or hitting the reactive power limits of a generator ($V_S$ is no longer maintained).

---

<em> Short-term instabilities </em>

Consider an induction motor. The torque-speed curve is given below. 

<p align="center">
<img src=figures_aclt/Motorstalling.png width="300" height="210" />
</p>

$T_L$ is the mechanical torque. $C$ curves correspond to different electromechanical torques depending on the slip $s=\frac{\omega_s - \omega_r}{\omega_s}$. 

The initial curve is $C_0^-$ and the machine operates on operating point $S_0$. If the voltage drops, the new curve becomes $C_0^+$. 

The motor speed $\omega_r$ is reduced (thus $s$ increases), and we reach a new operating point $S_1$. This increase in $s$ leads to an increase in motor current and the further decrease in voltage and electrical torque. If the rate of decreasing voltage is slower than that of increasing slip, the voltage settles down.

---

If now the voltage drops faster, and the new curve becomes $C_2$, the motor speed is reduced until it completely stops (since there is no intersection between $C_2$ and $T_L$). The induction motor acts as a large inductance, drawing reactive power.  

This is considered as a <b> Short-term Voltage Instability </b> as this phenomenon is much quicker than what we have with OLTCs (it takes several seconds to change tap positions). OLTCs are not able to restore the voltage.

<p align="center">
<img src=figures_aclt/InductionMotorVoltage.png width="350" height="280" />
</p>

.footnote[[9] F. Karbalaei, M. Kalantar, A. Kazemi,
Diagnosis of voltage collapse due to induction motor stalling using static analysis,
Energy Conversion and Management,
Volume 49, Issue 2,
2008,
Pages 151-156,
ISSN 0196-8904]

---

# (Some) counter-measures
## Network Reinforcement

We saw that the main issues for voltage problems are:
 - Large values of $X_L$
 - Not enough reactive power compensation

To mitigate voltage problems, one solution is to reinforce the network by adding new lines and capacitor banks, static var compensators or synchronous condensers.

---

## Voltage regulation

The second solution is to use the reactive power reserve already available. 

In transmission system, we have synchronous machines. They can provide or consume reactive power. 

<p align="center">
<img src=figures_aclt/SG_EMF.png width="600" height="230" />
</p>

In this figure $E_{af}$ is the induced emf, $V_a$ the stator voltage, $I_a$ the stator current and $X_s$ the synchronous reactance. In case (a), there is no reactive power transfer. In case (b), the synchronous machine <b> provides reactive power </b> and in case (c), the machine <b> consumes reactive power </b>.

---

- When the machine is overexcited, it produces reactive power (because of the larger induced emf). 
 
- When it is underexcited, it consumes reactive power. 
  
A regulator is responsible for controlling the excitation current in a synchronous generator. 

<p align="center">
<img src=figures_aclt/AVR.png width="500" height="260" />
</p>

The voltage setpoints $V_0$ are dispatched by the TSO to ensure a safe and reliable grid.

<em>N.B. In MV networks, the only way to regulate voltages is through on-load tap changers, or capacitor banks.</em> 

---

# Impact of renewable energy resources (RES)
## Reverse power flows in distribution systems

 - Distribution networks are radial networks (they are built as meshed networks, but operated radially)
 - Before the venue of distributed energy resources (<i> PV panels, batteries,... </i>), the power was flowing from the substation node, down to the end of the feeders.
 - Increasing penetration of DERs led to reverse power flows. 

<p align="center">
<img src=figures_aclt/VoltageProfile.png width="450" height="230" />
</p>


.footnote[[10] https://prod-energycouncil.energy.slicedtech.com.au/lv-voltage-report]

---

- During hours of high production and low consumption (at midday on a summer day), overvoltages can occur.

- It leads to the disconnection of PV inverters $\Rightarrow$ loss of production.

<p align="center">
<img src=figures_aclt/PVdisconnection.png width="400" height="260" />
</p>

.footnote[[11] https://danthesolarman.com.au/overvoltage-is-impacting-your-solar-systems/]  

---

- In distribution systems, the $X/R < 1$. Active power flows have actually a greater influence on voltage magnitudes than reactive power flows.

- One way to fight overvoltages in distribution networks with high penetration of solar inverters is to do active power curtailment and reactive power compensation.

<p align="center">
<img src=figures_aclt/VoltageCtrl.png width="700" height="300" />
</p>

.footnote[[12] Colot, A., Stegen, T., & Cornélusse, B. (2023, June). Fully distributed real-time voltage control in active distribution networks with large penetration of solar inverters. In 2023 IEEE Belgrade PowerTech (pp. 01-06). IEEE.] 

---

## Duck Curve

- As we further increase the penetration of RES, changes appear in the demand profile (concept of Duck Curve, now becoming Canyon Curve)

- Needs for flexibility to ensure power balance: shut down of flexible production plants when RES start to produce, activate them again when they stop producing

- There exist various solutions to <i> fill the curve </i>: Demand Side Management, Energy Buffers (e.g. batteries), increasing import/export capacities.

<p align="center">
<img src=figures_aclt/duckcurve.png width="400" height="260" />
</p>

.footnote[[13] https://www.powermag.com/epri-head-duck-curve-now-looks-like-a-canyon/]

---

# What did we learn? 

 - In transmission systems, because lines are inductive $X/R >> 1$, reactive power flows impact voltage magnitudes, and active power flows impact voltage angles

 - There is a maximum transmissible power through a line.

 - Different voltage instabilities, caused by slow acting devices like OLTC (Long-term instabilities), or by faster dynamics like stalling of induction motors (Short-term instabilities).

 - To prevent voltage instabilities, one can reinforce the grid by adding new lines or new devices, or enforce voltage regulation (local voltage control tracking voltage setpoints given by the system operator)

 - The increasing penetration of RES creates overvoltage problems in distribution networks and challenges for balancing the system.

---

class: end-slide, center
count: false

The end.
