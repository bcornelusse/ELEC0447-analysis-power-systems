#!/usr/bin/env python3
"""
Generate randomized, equalized, and project-decoupled interactive HTML quizzes for:
1. Frequency Control & Distributed Slack
2. Voltage Stability & Reactive Power Management
3. Rotor Angle Stability & Grid Strength
4. HVDC Transmission & Modern Grid Reinforcements
"""

import json
import re

with open('Lectures/SynchronousGenerator/quiz_generators.html', 'r', encoding='utf-8') as f:
    template = f.read()

start_q = template.find('const questions = [')
end_q = template.find('];', start_q) + 2

prefix_tmpl = template[:start_q]
suffix_tmpl = template[end_q:]

# Helper function to place correct answer at a designated index and order feedbacks accordingly
def build_question(qid, title, category, prompt, correct_item, distractor_items, target_idx):
    """
    correct_item: (option_text, feedback_text)
    distractor_items: list of 3 (option_text, feedback_text)
    target_idx: int in [0, 1, 2, 3] where the correct answer should be placed
    """
    assert len(distractor_items) == 3
    assert 0 <= target_idx <= 3

    options = []
    feedbacks = []

    d_iter = iter(distractor_items)
    for i in range(4):
        if i == target_idx:
            options.append(correct_item[0])
            feedbacks.append(correct_item[1])
        else:
            d_opt, d_fb = next(d_iter)
            options.append(d_opt)
            feedbacks.append(d_fb)

    return {
        "id": qid,
        "title": title,
        "category": category,
        "question": prompt,
        "options": options,
        "correct": target_idx,
        "explanation": correct_item[2],
        "distractor_feedbacks": feedbacks
    }


# =========================================================================
# QUIZ 1: FREQUENCY CONTROL & DISTRIBUTED SLACK
# =========================================================================
fc_q1 = build_question(
    qid="Q01",
    title="Q01: Kinetic Energy and Rate of Change of Frequency (RoCoF)",
    category="Power Balance & Kinetic Energy",
    prompt="In a 50 Hz power system with aggregate nominal apparent power $S_N = 10\\text{ GW}$ and equivalent inertia constant $H = 4.0\\text{ s}$, an unexpected generation outage creates an immediate active power imbalance of $\\Delta P = -500\\text{ MW}$. What is the initial Rate of Change of Frequency ($\\text{RoCoF} = df/dt$) at $t = 0^+$, before any governor action takes place?",
    correct_item=(
        "$\\frac{df}{dt} = \\frac{f_N \\Delta P}{2 H S_N} = -0.3125\\text{ Hz/s}$, derived directly from the aggregate rotor swing equation.",
        "Correct! $\\frac{df}{dt} = \\frac{f_N \\Delta P}{2 H S_N} = \\frac{50 \\times (-500\\text{ MW})}{2 \\times 4.0\\text{ s} \\times 10000\\text{ MW}} = -0.3125\\text{ Hz/s}$.",
        "Immediately after an active power imbalance $\\Delta P = P_m - P_e = -500\\text{ MW}$, the power deficit is supplied entirely by the stored kinetic energy of rotating synchronous masses: $\\frac{dE_k}{dt} \\approx \\frac{2 H S_N}{f_N} \\frac{df}{dt} = \\Delta P$. Solving for RoCoF yields: $\\frac{df}{dt} = \\frac{f_N \\Delta P}{2 H S_N} = \\frac{50 \\times (-500\\text{ MW})}{2 \\times 4.0\\text{ s} \\times 10000\\text{ MW}} = -0.3125\\text{ Hz/s}$."
    ),
    distractor_items=[
        (
            "$\\frac{df}{dt} = \\frac{f_N \\Delta P}{H S_N} = -0.6250\\text{ Hz/s}$, assuming the kinetic energy is released over the mechanical starting time $T_a = H$.",
            "Incorrect. This formula omits the factor of 2 in the kinetic energy derivative ($E_k = H S_N (f/f_N)^2$), overestimating RoCoF by a factor of two."
        ),
        (
            "$\\frac{df}{dt} = \\frac{2 H \\Delta P}{f_N S_N} = -0.0008\\text{ Hz/s}$, representing the per-unit power imbalance scaled by twice the inertia constant.",
            "Incorrect. This inverts the ratio between frequency and inertia, yielding an unphysically negligible frequency decay rate."
        ),
        (
            "$\\frac{df}{dt} = \\frac{\\Delta P}{2 H f_N} = -0.0250\\text{ Hz/s}$, evaluating the dimensional angular deceleration without the nominal capacity $S_N$.",
            "Incorrect. The system MVA base $S_N$ cannot be omitted; without it, the expression is dimensionally inconsistent."
        )
    ],
    target_idx=1  # Correct is B
)

fc_q2 = build_question(
    qid="Q02",
    title="Q02: Speed Droop and Individual Generator Power Response",
    category="Primary Frequency Control & Droop",
    prompt="A synchronous generator with nominal capacity $P_N = 400\\text{ MW}$ operates with a speed governor droop of $\\sigma = 4\\%$ ($0.04$). Following a severe system event, the grid frequency stabilizes at $49.80\\text{ Hz}$ ($\\Delta f = -0.20\\text{ Hz}$ from nominal $f_N = 50\\text{ Hz}$). Assuming the unit does not hit its maximum valve limit, what is its primary mechanical power increase $\\Delta P_m$?",
    correct_item=(
        "$\\Delta P_m = - \\frac{P_N}{\\sigma} \\frac{\\Delta f}{f_N} = +40.0\\text{ MW}$, corresponding to an increase of $10\\%$ of its nominal unit rating.",
        "Correct! $\\Delta P_m = - \\frac{P_N}{\\sigma} \\frac{\\Delta f}{f_N} = - \\frac{400\\text{ MW}}{0.04} \\times \\left( \\frac{-0.20\\text{ Hz}}{50\\text{ Hz}} \\right) = +40.0\\text{ MW}$.",
        "Governor droop is defined as $\\sigma = \\left| \\frac{\\Delta f / f_N}{\\Delta P_m / P_N} \\right|$. Solving for active power variation yields $\\Delta P_m = - \\frac{P_N}{\\sigma} \\frac{\\Delta f}{f_N} = - \\frac{400\\text{ MW}}{0.04} \\times \\left( \\frac{-0.20\\text{ Hz}}{50\\text{ Hz}} \\right) = - 10000 \\times (-0.004) = +40.0\\text{ MW}$. The unit increases output by $10\\%$ of its nominal rating."
    ),
    distractor_items=[
        (
            "$\\Delta P_m = - \\sigma P_N \\frac{\\Delta f}{f_N} = +0.064\\text{ MW}$, corresponding to multiplying the relative frequency error directly by droop.",
            "Incorrect. Droop $\\sigma$ represents the inverse slope of the governor power-frequency characteristic; power change divides by $\\sigma$ rather than multiplying by it."
        ),
        (
            "$\\Delta P_m = - P_N \\left( \\frac{\\Delta f}{f_N} \\right) = +1.60\\text{ MW}$, evaluating the unit response without accounting for governor droop amplification.",
            "Incorrect. This computes the raw per-unit frequency error on nominal capacity ($400 \\times 0.004 = 1.6\\text{ MW}$), ignoring the speed governor gain ($1/\\sigma = 25$)."
        ),
        (
            "$\\Delta P_m = - \\frac{P_N}{\\sigma} \\frac{f_N}{\\Delta f} = +250.0\\text{ MW}$, inverting the ratio between nominal frequency and steady-state frequency error.",
            "Incorrect. The frequency error ratio is $\\Delta f / f_N = -0.2/50 = -0.004$, not $f_N / \\Delta f$."
        )
    ],
    target_idx=0  # Correct is A
)

fc_q3 = build_question(
    qid="Q03",
    title="Q03: System Quasi-Steady-State Frequency Deviation",
    category="Primary Frequency Control & Droop",
    prompt="A power system with negligible load damping ($D \\approx 0$) experiences an unexpected active power loss $\\Delta P_{\\text{lost}}$. If all online generating units possess power-frequency governor stiffnesses $K_{p,i} = P_{N,i} / \\sigma_i$ (in MW/Hz or MW/pu), what governing formula dictates the quasi-steady-state frequency deviation $\\Delta f$ before secondary control intervenes?",
    correct_item=(
        "$\\Delta f = - \\frac{\\Delta P_{\\text{lost}}}{\\sum_i K_{p,i} + D}$, meaning frequency drop is inversely proportional to total system regulating stiffness.",
        "Correct! In quasi-steady state, $\\Delta f = - \\frac{\\Delta P_{\\text{lost}}}{\\sum_i K_{p,i} + D}$. The frequency drop is inversely proportional to system primary regulating stiffness.",
        "In primary frequency control, governors use proportional droop control. The aggregate power response is $\\sum_i \\Delta P_i = - (\\sum_i K_{p,i}) \\frac{\\Delta f}{f_N}$. Equating this to the power imbalance $\\Delta P_{\\text{lost}}$ yields the quasi-steady-state frequency deviation: $\\Delta f = - \\frac{\\Delta P_{\\text{lost}}}{\\sum_i K_{p,i} + D}$. Frequency stabilization requires a permanent offset (proportional droop), which secondary control subsequently restores."
    ),
    distractor_items=[
        (
            "$\\Delta f = - \\frac{\\Delta P_{\\text{lost}} \\cdot f_N}{\\sum_i 2 H_i S_{N,i}}$, assuming steady-state frequency is dictated entirely by aggregate machine inertia.",
            "Incorrect. Machine inertia determines initial RoCoF during the transient ($t < 1\\text{--}2\\text{ s}$), but drops out in quasi-steady-state once $df/dt = 0$."
        ),
        (
            "$\\Delta f = - \\frac{\\sum_i K_{p,i}}{\\Delta P_{\\text{lost}} + D}$, implying that greater governor stiffness results in a larger steady-state frequency drop.",
            "Incorrect. Frequency deviation is inversely proportional to system stiffness; stiffer systems experience smaller frequency deviations."
        ),
        (
            "$\\Delta f = - \\frac{\\Delta P_{\\text{lost}} \\cdot \\max_i \\sigma_i}{\\sum_i P_{N,i}}$, determined solely by the single generator with the highest governor droop setting.",
            "Incorrect. All synchronized generators with active governors contribute simultaneously in parallel, weighted by their individual stiffness $K_{p,i} = P_{N,i}/\\sigma_i$."
        )
    ],
    target_idx=2  # Correct is C
)

fc_q4 = build_question(
    qid="Q04",
    title="Q04: Distributed Slack Power Flow vs Single Slack Modeling",
    category="Distributed Slack Modeling",
    prompt="When modeling an unexpected generator tripping event in steady-state AC power flow simulation, why is a distributed slack formulation physically and numerically superior to a conventional single-slack bus calculation?",
    correct_item=(
        "A single slack bus forces one generator to absorb 100% of the active power imbalance and loss variations, whereas distributed slack allocates redispatch across all governors proportional to $w_i = \\frac{S_{N,i}/\\sigma_i}{\\sum_j S_{N,j}/\\sigma_j}$.",
        "Correct! Single slack concentrates the entire disturbance onto one machine; distributed slack shares power across all governors proportional to their MW capacity and droop, accurately reflecting physical grid response.",
        "In classic single-slack power flow, a solitary reference bus absorbs all system power imbalances ($\\Delta P_{\\text{lost}} + \\Delta P_{\\text{losses}}$). This creates unrealistically severe line loadings and voltage depressions adjacent to the slack bus. In reality, primary frequency response distributes the imbalance across the entire generator fleet according to governor droop: $w_i = \\frac{S_{N,i}/\\sigma_i}{\\sum_j S_{N,j}/\\sigma_j}$. Setting <code>distributed_slack=True</code> accurately mirrors this physical multi-machine redispatch."
    ),
    distractor_items=[
        (
            "A single slack bus causes the nodal admittance matrix to lose rank ($\\text{rank}(\\mathbf{Y}_{\\text{bus}}) < N - 1$), whereas distributed slack maintains matrix invertibility by converting all PQ load buses into PV voltage-controlled buses.",
            "Incorrect. Single-slack power flow preserves matrix invertibility and converges fine mathematically, but yields physically unrealistic line flows and localized branch overloads."
        ),
        (
            "A single slack bus neglects transmission line series resistances ($R_{ij} = 0$), whereas distributed slack re-establishes ohmic branch losses by dynamically scaling line conductances $G_{ij}$ with frequency deviations.",
            "Incorrect. Full AC power flow includes line resistance $R$ in both single-slack and distributed-slack modes; distributed slack redistributes active power, not line conductances."
        ),
        (
            "A single slack bus forces the Newton-Raphson Jacobian matrix to be non-invertible ($\\det \\mathbf{J} = 0$), whereas distributed slack avoids the Jacobian entirely by solving a decoupled sequence of linear DC equations.",
            "Incorrect. Distributed slack executes a full non-linear AC Newton-Raphson power flow with an augmented Jacobian matrix; it is not a DC approximation."
        )
    ],
    target_idx=3  # Correct is D
)

fc_q5 = build_question(
    qid="Q05",
    title="Q05: Role and Control Law of Secondary Frequency Control (AGC)",
    category="Secondary Control (AGC)",
    prompt="While primary frequency control stabilizes the grid within $2\\text{--}30\\text{ seconds}$, why is Secondary Frequency Control (Automatic Generation Control / aFRR, acting over $30\\text{ s to }15\\text{ minutes}$) necessary, and what is its control law?",
    correct_item=(
        "Primary control leaves a quasi-steady-state error $\\Delta f \\neq 0$ and unbalances cross-border exchanges; secondary control drives $\\text{ACE} = \\Delta P_{\\text{tie}} + K \\Delta f$ to zero using integral action.",
        "Correct! Secondary control integrates Area Control Error ($\\text{ACE} = \\Delta P_{\\text{tie}} + K \\Delta f$), eliminating residual frequency error and restoring scheduled tie-line flows.",
        "Primary control is a proportional control: it arrests frequency decay but leaves a residual steady-state frequency error $\\Delta f$ and causes unintended power exchanges across cross-border tie-lines. Secondary control (AGC/aFRR) employs a centralized integral controller per control zone that monitors Area Control Error ($\\text{ACE} = \\Delta P_{\\text{tie}} + K_r \\Delta f$). By integrating ACE, it brings both $\\Delta f$ back to $0$ ($50.00\\text{ Hz}$) and tie-line flows back to scheduled contract values, liberating primary reserves for the next disturbance."
    ),
    distractor_items=[
        (
            "Primary control cannot modify generator exciter voltages; secondary control adjusts Automatic Voltage Regulators (AVR) according to $\\Delta V = K_v \\Delta Q$ to eliminate rotor pole slipping.",
            "Incorrect. Excitation voltage and field current control fall under Automatic Voltage Regulators (AVR) for voltage control, not secondary frequency control."
        ),
        (
            "Primary control destabilizes turbine rotor angles; secondary control executes Under-Frequency Load Shedding (UFLS) according to $\\Delta P_{\\text{shed}} = K_f (f_{\\text{trip}} - f)$ to prevent total blackout.",
            "Incorrect. Emergency load shedding below $49.0\\text{ Hz}$ is Under-Frequency Load Shedding (UFLS), a defense plan of last resort, not secondary AGC regulation."
        ),
        (
            "Primary control operates exclusively on day-ahead markets; secondary control runs quadratic optimal power flow according to $\\min \\sum C_i(P_i)$ to re-dispatch generators based on fuel prices.",
            "Incorrect. Economic day-ahead scheduling is tertiary control / market redispatch, operating on hourly horizons rather than automated minute-by-minute AGC."
        )
    ],
    target_idx=1  # Correct is B
)


# =========================================================================
# QUIZ 2: VOLTAGE STABILITY & REACTIVE POWER MANAGEMENT
# =========================================================================
vs_q1 = build_question(
    qid="Q01",
    title="Q01: Mathematical Origin of the P-V Nose Point and Solver Divergence",
    category="P-V Nose Curves & Maximum Power",
    prompt="When tracing the receiving-end voltage $V_R$ as active power demand $P$ increases, the curve reaches a maximum transmissible power $P_{\\max}$ (the nose of the $P$-$V$ curve). Why does a standard Newton-Raphson power flow solver diverge if power demand is increased beyond $P_{\\max}$?",
    correct_item=(
        "At the nose point, the power flow Jacobian matrix becomes singular ($\\det \\mathbf{J} = 0$, $dP/dV = 0$); beyond this saddle-node bifurcation point, no real-valued steady-state voltage solution exists.",
        "Correct! The nose point is a saddle-node bifurcation where $\\det \\mathbf{J} = 0$ and $dP/dV = 0$. Beyond $P_{\\max}$, no real power flow solution exists.",
        "The nose point represents a saddle-node bifurcation. As power demand reaches $P_{\\max}$, the high-voltage (stable) and low-voltage (unstable) solutions coalesce. At this point, $\\frac{dP}{dV} = 0$, causing the power flow Jacobian matrix $\\mathbf{J} = \\begin{bmatrix} \\frac{\\partial P}{\\partial \\theta} & \\frac{\\partial P}{\\partial V} \\\\ \\frac{\\partial Q}{\\partial \\theta} & \\frac{\\partial Q}{\\partial V} \\end{bmatrix}$ to become singular ($\\det \\mathbf{J} = 0$). Beyond $P_{\\max}$, the mathematical equations have only complex roots; no physical steady-state operating point exists, triggering solver divergence."
    ),
    distractor_items=[
        (
            "At the nose point, transmission line current reaches $I = \\infty$, causing the series branch impedance matrix to become non-invertible due to infinite resistive dissipation ($I^2 R \\to \\infty$).",
            "Incorrect. Line current remains finite at the nose point; divergence is caused by Jacobian singularity and the absence of real algebraic roots, not infinite physical current."
        ),
        (
            "At the nose point, the voltage phase angle reaches $\\delta = 180^\\circ$, causing active power flow $P = \\frac{V_1 V_2}{X} \\sin\\delta$ to reverse sign and creating persistent numerical limit cycles.",
            "Incorrect. The voltage angle at the nose point is typically in the range of $30^\\circ\\text{--}45^\\circ$, far below $180^\\circ$."
        ),
        (
            "At the nose point, reactive power demand satisfies $Q = V^2 B_c$, triggering an exact numerical resonance with shunt capacitance that generates division-by-zero errors in the solver.",
            "Incorrect. Shunt capacitance provides voltage support; divergence occurs when load exceeds network transfer capability, causing Jacobian singularity."
        )
    ],
    target_idx=2  # Correct is C
)

vs_q2 = build_question(
    qid="Q02",
    title="Q02: Influence of Load Power Factor on Voltage Stability",
    category="Power Factor & Reactive Drops",
    prompt="Consider a transmission corridor feeding a load bus. How does shifting the load power factor from unity ($\\cos\\phi = 1.0$) to lagging ($\\cos\\phi = 0.95$ inductive) alter the $P$-$V$ nose curve and the maximum transferable power $P_{\\max}$?",
    correct_item=(
        "Lagging power factor draws inductive current that causes large reactive voltage drops ($\\Delta V \\approx X Q / V$) across line reactances, drastically shrinking $P_{\\max}$ and raising the critical collapse voltage.",
        "Correct! Inductive current creates heavy reactive voltage drops across transmission line reactances ($X Q / V$), severely curtailing $P_{\\max}$.",
        "High-voltage transmission lines are predominantly inductive ($X \\gg R$). Drawing lagging (inductive) current creates severe voltage drops $\\Delta V \\approx \\frac{R P + X Q}{V} \\approx \\frac{X Q}{V}$. When a load consumes inductive reactive power alongside active power ($Q = P \\tan\\phi > 0$), reactive losses $I^2 X$ compound, causing receiving voltage to decline much faster with active power. As a result, the maximum transferable active power $P_{\\max}$ drops substantially, and the critical voltage $V_{\\text{crit}}$ at the collapse point shifts higher."
    ),
    distractor_items=[
        (
            "Lagging power factor increases $P_{\\max}$ because inductive current compensates line shunt charging ($Q_{\\text{load}} = \\omega C V^2$), holding transmission voltage flat up to twice nominal loading.",
            "Incorrect. Ferranti rise occurs on lightly loaded lines due to shunt capacitance, whereas inductive load current aggravates line reactive consumption and accelerates collapse."
        ),
        (
            "The active power limit $P_{\\max}$ remains completely unchanged because active power transfer $P$ is mathematically decoupled from reactive power $Q$ in high-voltage grids ($\\partial P / \\partial Q = 0$).",
            "Incorrect. Active and reactive power flows are tightly coupled through line series reactances and node voltage magnitudes; lagging power factor significantly contracts $P_{\\max}$."
        ),
        (
            "Lagging power factor shifts the receiving voltage to $V_R = V_S \\cos\\delta$, eliminating the lower unstable branch of the nose curve and transforming the bifurcation into an unconditional linear limit.",
            "Incorrect. The two solutions (upper stable and lower unstable) persist under lagging power factor, but the bifurcation point occurs at a lower $P_{\\max}$."
        )
    ],
    target_idx=0  # Correct is A
)

vs_q3 = build_question(
    qid="Q03",
    title="Q03: Impact of Generator Reactive Power Limits ($Q_{\\max}$)",
    category="Generator Limits (Q-lims)",
    prompt="When analyzing transmission voltage stability under increasing system load, what physical and numerical change occurs when a nearby synchronous generator reaches its rotor excitation current limit ($Q = Q_{\\max}$)?",
    correct_item=(
        "The generator bus converts from PV to PQ with $Q$ clamped at $Q_{\\max}$; losing local terminal voltage regulation creates a sharp downward break in the $P$-$V$ curve and drastically brings forward voltage collapse.",
        "Correct! Hitting $Q_{\\max}$ converts the bus from PV to PQ; losing voltage control creates a sharp downward kink in the $P$-$V$ curve and brings forward collapse.",
        "Synchronous generators normally operate as PV buses, adjusting rotor excitation current via Automatic Voltage Regulators (AVR) to maintain constant terminal voltage ($V = V_{\\text{set}}$). When reactive demand forces field or armature current to its thermal ceiling ($Q = Q_{\\max}$), excitation can no longer increase. In power flow, the bus switches to a PQ bus with fixed reactive injection $Q_{\\max}$ and free voltage $V$. The grid loses local voltage control, transferring reactive burden to more distant machines and drastically shrinking the voltage stability margin."
    ),
    distractor_items=[
        (
            "The generator bus converts from PV to Slack with voltage angle clamped at $\\theta = 0^\\circ$; absorbing unlimited active power from the transmission grid to stabilize stator winding temperatures.",
            "Incorrect. Reaching reactive limits converts a PV bus into a PQ bus; it does not turn the machine into an infinite slack bus."
        ),
        (
            "The generator excitation protection trips the unit offline within 10 milliseconds, instantaneously dropping active power output ($P = 0$) and causing an immediate transient angle collapse.",
            "Incorrect. Physical generators do not trip merely upon reaching Mvar excitation limits; the Over-Excitation Limiter (OEL) simply clamps excitation to prevent thermal damage."
        ),
        (
            "The generator automatic voltage regulator switches to frequency droop control, dynamically doubling active power generation ($P = 2 P_0$) to compensate for the reactive power shortfall.",
            "Incorrect. Voltage regulators control excitation (reactive power), while turbine governors control active power; reaching $Q_{\\max}$ does not alter turbine active setpoints."
        )
    ],
    target_idx=1  # Correct is B
)

vs_q4 = build_question(
    qid="Q04",
    title="Q04: Shunt Capacitor Placement for Voltage Support",
    category="Shunt Compensation & Controls",
    prompt="To prevent voltage collapse and expand the permissible active power transfer margin along a heavily loaded transmission corridor, why is placing a shunt capacitor bank at the receiving load substation vastly more effective than placing it further upstream near the sending generation bus?",
    correct_item=(
        "Transmitting reactive power across inductive lines incurs high reactive losses ($\\Delta Q = I^2 X$) and large voltage drops; local compensation supplies $Q$ at the load, offloading upstream corridors and maximizing $P_{\\max}$.",
        "Correct! Supplying reactive power locally at the load bus relieves upstream transmission lines of reactive current, minimizing $I^2 X$ drops and maximizing stability margins.",
        "Reactive power transport over transmission lines consumes reactive power itself ($\\Delta Q_{\\text{loss}} = I^2 X$). Supplying reactive power from upstream requires transmitting high reactive currents across bottleneck lines, depressing voltage along the entire corridor. Installing shunt capacitors directly at the receiving load bus provides reactive compensation locally, eliminating the reactive current component flowing through upstream branches. This offloads transmission lines, reduces active and reactive losses, and provides maximum elevation of the $P$-$V$ nose curve."
    ),
    distractor_items=[
        (
            "Upstream placement near the sending bus causes capacitor dielectric breakdown under elevated generator electromotive force ($E_{af} > 1.2\\text{ pu}$), forcing protection relays to isolate the capacitor bank.",
            "Incorrect. Capacitor banks are rated for the nominal bus voltage at their installation substation; location choice is governed by network power flow physics, not dielectric breakdown."
        ),
        (
            "Shunt capacitors installed at receiving buses consume active power ($P = V^2 G$), directly damping electromechanical power oscillations between sending and receiving substations.",
            "Incorrect. Shunt capacitors are purely reactive components ($Q = V^2 B_c$); they do not consume significant active power nor act as electromechanical dampers."
        ),
        (
            "Upstream capacitor placement reverses the polarity of transformer leakage reactance ($X_t < 0$), causing uncontrollable overvoltages across downstream distribution networks.",
            "Incorrect. Shunt capacitors connect in parallel to ground; they do not alter the series leakage inductive reactance of transformers."
        )
    ],
    target_idx=3  # Correct is D
)

vs_q5 = build_question(
    qid="Q05",
    title="Q05: Under-Load Tap Changers (OLTC) and Voltage Collapse",
    category="Shunt Compensation & Controls",
    prompt="How can automatic Under-Load Tap Changers (OLTC) on transmission-to-distribution transformers inadvertently trigger or accelerate a system-wide voltage collapse during depressed grid conditions?",
    correct_item=(
        "When transmission voltage sags, OLTCs boost secondary turns to restore distribution voltage; for voltage-sensitive loads, restoring load voltage restores power draw, pulling even higher current through the struggling transmission network.",
        "Correct! Restoring secondary distribution voltages prevents natural load relief, demanding high currents from the stressed transmission grid and accelerating collapse.",
        "This phenomenon is known as 'tap changer reverse action' or load restoration. When transmission voltage drops, OLTCs automatically adjust tap ratios to keep distribution bus voltage near $1.0\\text{ pu}$. However, restoring distribution voltage causes voltage-dependent loads (thermostatic, motor, and constant impedance loads) to draw their full nominal power. This forces the transmission network to supply higher currents through its inductive reactances, deepening transmission voltage drops and pushing the grid over the nose of the $P$-$V$ curve."
    ),
    distractor_items=[
        (
            "When transmission voltage sags, OLTC tap changers automatically invert the phase angle between primary and secondary windings by $180^\\circ$, converting inductive loads into negative resistance generators.",
            "Incorrect. Standard OLTCs modify voltage magnitude (in-phase ratio taps); they do not invert phase angle by $180^\\circ$."
        ),
        (
            "When transmission voltage sags, OLTC transition resistors remain permanently in-circuit, dissipating megawatts of active power as heat and causing thermal overload of the substation busbars.",
            "Incorrect. Transition resistors are switched in for only a few milliseconds during tap transitions; they do not cause transmission voltage collapse."
        ),
        (
            "When transmission voltage sags, OLTC controllers lock all downstream distribution capacitor banks into a disconnected state, preventing reactive power injection during emergency low-voltage conditions.",
            "Incorrect. Tap changers regulate transformer turns ratio; they do not send remote disconnect commands to independent distribution capacitor banks."
        )
    ],
    target_idx=0  # Correct is A
)


# =========================================================================
# QUIZ 3: ROTOR ANGLE STABILITY & GRID STRENGTH
# =========================================================================
ts_q1 = build_question(
    qid="Q01",
    title="Q01: Synchronous Generator Subtransient Currents ($X''_d$)",
    category="Subtransient Currents & IEC 60909",
    prompt="During the subtransient period ($t \\approx 10\\text{--}40\\text{ ms}$) following a bolted three-phase short-circuit, why do synchronous machines feed massive fault currents ($5\\text{ to }7 \\times I_n$) into the transmission network?",
    correct_item=(
        "Flux linkages trapped in closed rotor field and damper circuits cannot change discontinuously ($d\\psi/dt \\approx 0$), forcing the machine to act as a low-impedance voltage source behind $X''_d \\ll X_d$ and feeding $I''_k \\approx (5\\text{--}7) I_n$.",
        "Correct! Conservation of rotor flux linkages inside damper and field circuits forces the machine to react via its low subtransient reactance $X''_d \\ll X_d$.",
        "According to the principle of constant flux linkages, the magnetic flux enclosed by closed rotor circuits (field winding and amortisseur damper bars) cannot jump discontinuously upon a sudden terminal short circuit. To oppose flux changes, induced eddy and damper currents shield the rotor body, restricting magnetic flux paths to high-reluctance leakage paths. The machine exhibits a very low apparent reactance, the subtransient reactance $X''_d$, resulting in initial symmetrical fault currents $I''_k = E'' / X''_d \\approx (5\\text{--}7) I_n$."
    ),
    distractor_items=[
        (
            "Stator winding copper undergoes transient superconductivity under high current density, reducing phase resistance to $R_a = 0$ and allowing fault currents to reach $I''_k \\approx 50 \\times I_n$.",
            "Incorrect. Machine winding copper retains normal electrical resistance; subtransient current magnitude is bounded by the subtransient inductive leakage reactance $X''_d$."
        ),
        (
            "Turbine speed governors open steam valves to 100% within the subtransient timeframe ($t < 20\\text{ ms}$), driving mechanical input power to $P_m = 5 P_n$ and multiplying electrical current output.",
            "Incorrect. Mechanical governors have time constants on the order of seconds; they cannot respond within the subtransient electromagnetic window ($10\\text{--}40\\text{ ms}$)."
        ),
        (
            "Generator step-up transformers saturate magnetically, reducing core relative permeability to $\\mu_r \\approx 1$ and converting three-phase transformers into ideal air-core inductors with zero impedance.",
            "Incorrect. Core saturation occurs under certain voltage transients, but subtransient fault current magnitude is fundamentally dictated by machine internal rotor flux conservation and leakage reactances."
        )
    ],
    target_idx=1  # Correct is B
)

ts_q2 = build_question(
    qid="Q02",
    title="Q02: The Equal Area Criterion and Decelerating Margin",
    category="Equal Area Criterion & CCT",
    prompt="According to the Equal Area Criterion (EAC) for a synchronous machine connected to an infinite bus, what is the fundamental condition required for the generator to maintain transient rotor angle stability following a short-circuit fault?",
    correct_item=(
        "The kinetic energy gained during fault acceleration ($\\text{Area A} = \\int_{\\delta_0}^{\\delta_{\\text{cl}}} (P_m - P_{e,f}) d\\delta$) must be fully absorbed by post-fault decelerating capability ($\\text{Area B} = \\int_{\\delta_{\\text{cl}}}^{\\delta_{\\max}} (P_{e,pf} - P_m) d\\delta$), requiring $\\text{Area B} \\ge \\text{Area A}$.",
        "Correct! Transient stability requires that available post-fault decelerating energy (Area B) exceeds the kinetic energy accumulated during the fault (Area A).",
        "Integrating the swing equation $M \\frac{d^2\\delta}{dt^2} = P_m - P_e$ shows that the change in rotor kinetic energy is proportional to the area under the power-angle curve. During the fault, electrical power collapses ($P_{e,f} < P_m$), accumulating accelerating kinetic energy $\\text{Area A} = \\int_{\\delta_0}^{\\delta_{\\text{cl}}} (P_m - P_{e,f}) d\\delta$. After fault clearing, stability requires that the rotor can decelerate back to synchronous speed ($d\\delta/dt = 0$) before reaching the unstable equilibrium point $\\delta_{\\max}$. This requires $\\text{Area B} \\ge \\text{Area A}$."
    ),
    distractor_items=[
        (
            "The total electrical work done during the fault must equal the mechanical energy stored in the rotor shaft ($W_e = \\frac{1}{2} J \\omega_0^2$), requiring the rotor angle to satisfy $\\delta_{\\text{cl}} \\le 45^\\circ$ at all times.",
            "Incorrect. The rotor angle frequently swings well beyond $45^\\circ$ (often up to $100^\\circ\\text{--}130^\\circ$) while remaining fully stable."
        ),
        (
            "The accelerating power at the instant of fault clearing must exactly equal the post-fault damping power ($P_m - P_{e,f} = D \\omega_0$), ensuring that rotor angular acceleration immediately becomes zero.",
            "Incorrect. At clearing, electrical power does not equal mechanical power; the rotor is still spinning above synchronous speed and must decelerate across Area B."
        ),
        (
            "The area under the mechanical power line ($P_m \\cdot \\delta_{\\max}$) must exceed the integral of the pre-fault power-angle curve ($\\int_0^{\\pi} \\hat{P}_e \\sin\\delta d\\delta$), preventing rotor pole slipping.",
            "Incorrect. Mechanical energy during the fault causes acceleration; stability is governed by the net balance between accelerating Area A and decelerating Area B."
        )
    ],
    target_idx=3  # Correct is D
)

ts_q3 = build_question(
    qid="Q03",
    title="Q03: Short-Circuit Capacity ($S''_{sc}$) and Critical Clearing Time ($CCT$)",
    category="Equal Area Criterion & CCT",
    prompt="How does an electrically strong grid (high short-circuit level $S''_{sc}$, low Thévenin reactance $X_{th}$) impact the post-fault power-angle curve and the Critical Clearing Time ($CCT$) of a synchronous generator?",
    correct_item=(
        "High short-circuit capacity implies small Thévenin reactance ($X_{th} \\propto 1/S''_{sc}$), which elevates peak post-fault power $\\hat{P}_{e,pf} = \\frac{E' V}{X'_d + X_{th}}$, expanding decelerating Area B and lengthening the $CCT$.",
        "Correct! Higher short-circuit capacity boosts peak post-fault power transfer, enlarging decelerating Area B and lengthening the Critical Clearing Time ($CCT$).",
        "Post-fault electrical power transfer is governed by $\\hat{P}_{e,pf} = \\frac{E' V}{X'_d + X_{th}}$. In a strong grid ($S''_{sc}$ high, $X_{th}$ low), $\\hat{P}_{e,pf}$ is significantly higher. This lifts the post-fault power-angle curve, vastly enlarging the available decelerating Area B: $\\text{Area B} = \\int_{\\delta_{\\text{cl}}}^{\\delta_{\\max}} (\\hat{P}_{e,pf}\\sin\\delta - P_m) d\\delta$. With more decelerating capacity, the system can tolerate a larger accelerating Area A, increasing the critical clearing angle $\\delta_{cct}$ and lengthening the Critical Clearing Time ($CCT$), providing a wider safety margin for protection relays."
    ),
    distractor_items=[
        (
            "High short-circuit capacity increases fault current magnitude ($I''_k \\propto S''_{sc}$), which doubles mechanical acceleration during the fault ($a = P_m/M$) and significantly shortens the $CCT$.",
            "Incorrect. During a bolted three-phase fault, electrical power drops to zero regardless of grid strength, so fault acceleration ($P_m/M$) is identical, while post-fault recovery is much stronger."
        ),
        (
            "High short-circuit capacity locks the generator internal rotor angle to the infinite bus reference ($\\delta(t) = \\delta_0$), eliminating electromechanical oscillations and rendering $CCT$ infinite.",
            "Incorrect. A finite Thévenin reactance always exists; the rotor angle oscillates dynamically governed by the non-linear swing equation."
        ),
        (
            "High short-circuit capacity alters only circuit breaker interrupting duties ($I_b$), having zero physical influence on the electrical power-angle curve or generator rotor dynamics.",
            "Incorrect. Grid strength and Thévenin impedance directly dictate the post-fault synchronizing power transfer curve $\\hat{P}_{e,pf} \\sin\\delta$."
        )
    ],
    target_idx=0  # Correct is A
)

ts_q4 = build_question(
    qid="Q04",
    title="Q04: Small-Signal Synchronizing Torque Coefficient ($K_s$)",
    category="Synchronizing Torque & Small-Signal",
    prompt="The small-signal synchronizing torque coefficient is defined as $K_s = \\left.\\frac{\\partial P_e}{\\partial\\delta}\\right|_{\\delta_0} = \\frac{E' V}{X'_d + X_{th}} \\cos\\delta_0$. What physical failure mode occurs if operating conditions push the rotor angle such that $K_s < 0$?",
    correct_item=(
        "The electromechanical coupling becomes repulsive rather than restoring, yielding a positive real eigenvalue in $M s^2 + K_s = 0$ and causing aperiodic (monotonic) loss of synchronism.",
        "Correct! When $K_s < 0$, the restoring torque inverts, causing the rotor angle to drift monotonically out of synchronism (aperiodic instability).",
        "The synchronizing torque coefficient $K_s$ acts as the torsional spring stiffness of the magnetic coupling connecting the rotor to the AC grid. When $K_s > 0$, any angular displacement $\\Delta\\delta > 0$ produces an electrical counter-torque $\\Delta P_e > 0$ that restores the rotor. If operating conditions exceed steady-state pull-out ($\\delta_0 > 90^\\circ$ for a cylindrical machine), $K_s = \\frac{\\partial P_e}{\\partial\\delta} < 0$. The characteristic equation $M s^2 + K_s = 0$ yields a positive real root ($s = +\\sqrt{|K_s|/M}$), causing non-oscillatory aperiodic rotor runaway."
    ),
    distractor_items=[
        (
            "The generator develops negative electrical resistance ($R_e < 0$), triggering high-frequency sub-synchronous resonance with series compensated transmission lines.",
            "Incorrect. Negative electrical resistance refers to sub-synchronous resonance (SSR) with series compensated lines, not the loss of synchronizing torque ($K_s < 0$)."
        ),
        (
            "The electromechanical oscillation frequency $\\omega_n = \\sqrt{K_s/M}$ becomes purely real and shifts into the acoustic sound spectrum, causing physical stator bar vibration.",
            "Incorrect. When $K_s < 0$, $\\omega_n = \\sqrt{K_s/M}$ becomes imaginary ($s = \\pm \\sqrt{|K_s|/M}$), producing non-oscillatory exponential divergence rather than acoustic sound."
        ),
        (
            "The automatic voltage regulator immediately inverts rotor flux direction, restoring stability by forcing negative field excitation voltage through the brushless exciter.",
            "Incorrect. AVR control cannot restore stability if the operating point is past the steady-state pull-out limit where $dP/d\\delta < 0$."
        )
    ],
    target_idx=2  # Correct is C
)

ts_q5 = build_question(
    qid="Q05",
    title="Q05: Short-Circuit Ratio (SCR) and Renewable Converter Stability",
    category="Short-Circuit Ratio & Grid Strength",
    prompt="The Short-Circuit Ratio at a converter Point of Common Coupling is defined as $\\text{SCR} = S''_{sc} / P_{\\text{rated}}$. Why do grid connection points with $\\text{SCR} < 2.0$ ('very weak grids') create severe operational instability for standard grid-following (GFL) inverter-based resources?",
    correct_item=(
        "High grid Thévenin impedance ($Z_{th} \\gg 0$) means converter current injections produce large voltage magnitude and phase swings ($\\Delta V \\approx Z_{th} \\Delta I$), destabilizing Phase-Locked Loop (PLL) synchronization.",
        "Correct! In weak grids ($\\text{SCR} < 2.0$), high Thévenin impedance makes terminal voltage hypersensitive to converter current, destabilizing Phase-Locked Loops (PLLs).",
        "Grid-following (GFL) inverters rely on a Phase-Locked Loop (PLL) to detect grid voltage phase and maintain synchronism. In a weak grid ($S''_{sc}$ low, $X_{th}$ high, $\\text{SCR} < 2.0$), the grid voltage at the point of common coupling (PCC) is highly sensitive to converter active and reactive current injections ($\\Delta V \\approx Z_{th} \\Delta I$). This creates strong non-linear cross-coupling between inverter current control loops, DC-link voltage regulators, and the PLL, leading to voltage oscillations, PLL loss of lock, and converter tripping."
    ),
    distractor_items=[
        (
            "Low short-circuit capacity prevents inverter semiconductor switches from commutating, causing reverse overvoltage breakdown of the IGBT anti-parallel freewheeling diodes.",
            "Incorrect. IGBTs are self-commutating switches; they do not rely on grid voltage for commutation, unlike line-commutated thyristors (LCC)."
        ),
        (
            "In weak grids, the ratio of resistance to reactance satisfies $R/X > 10$, converting transmission lines into purely resistive heating elements that dissipate all converter power output.",
            "Incorrect. High-voltage transmission lines remain predominantly inductive ($X \\gg R$) even in weak grids; the issue is high impedance magnitude ($|Z_{th}|$), not high resistance."
        ),
        (
            "Inverter harmonic filters resonate with the grid Thévenin inductance, permanently clamping converter active power injection to zero regardless of DC-link power availability.",
            "Incorrect. Harmonic resonances can occur, but the fundamental definition of weak grid GFL instability is voltage sensitivity and Phase-Locked Loop loss of synchronization."
        )
    ],
    target_idx=1  # Correct is B
)


# =========================================================================
# QUIZ 4: HVDC TRANSMISSION & ADVANCED GRID REINFORCEMENTS
# =========================================================================
hd_q1 = build_question(
    qid="Q01",
    title="Q01: Line-Commutated (LCC) vs Voltage Source (VSC) Converters",
    category="LCC vs VSC HVDC Technologies",
    prompt="What is a major operational advantage of Voltage Source Converter (VSC-HVDC) technology based on IGBTs over conventional Line-Commutated Converter (LCC-HVDC) technology based on thyristors?",
    correct_item=(
        "VSC-HVDC uses self-commutating IGBTs with high-frequency switching, providing decoupled four-quadrant $(P, Q)$ control without requiring an external AC commutating voltage or bulky reactive filter banks.",
        "Correct! VSC-HVDC allows independent four-quadrant active and reactive power control without requiring an external AC commutating voltage, enabling weak grid and black-start operation.",
        "LCC-HVDC uses line-commutated thyristors that require a strong AC voltage source to turn off (commutation). LCCs always consume reactive power ($Q \\approx 0.5\\text{--}0.6 P$) and risk commutation failure if AC voltage sags. In contrast, VSC-HVDC uses self-commutating switches (IGBTs) with Pulse-Width Modulation (PWM) or Modular Multilevel Converters (MMC). VSC can synthesize an AC voltage waveform independently, providing decoupled four-quadrant $(P, Q)$ control, voltage support to weak AC networks, and black-start capability."
    ),
    distractor_items=[
        (
            "LCC-HVDC uses line-commutated thyristors that synthesize sinusoidal AC voltages from zero, enabling seamless black-start of passive islanded networks without auxiliary diesel generators.",
            "Incorrect. LCC converters cannot black-start a dead grid because thyristors require an existing AC commutating voltage to turn off; black-start is a distinctive capability of VSC."
        ),
        (
            "VSC-HVDC is restricted to low-voltage DC microgrids ($V_{\\text{dc}} < 1.5\\text{ kV}$), whereas LCC-HVDC is the only technology capable of transmitting power through underground cross-linked polyethylene cables.",
            "Incorrect. VSC-HVDC operates at extra-high voltages (e.g. $\\pm 525\\text{ kV}$, several gigawatts) and is the preferred technology for extruded XLPE cables."
        ),
        (
            "LCC-HVDC produces zero harmonic distortion on AC busbars, eliminating the need for AC harmonic filters, whereas VSC-HVDC requires massive 50 Hz series resonant blocking circuits.",
            "Incorrect. LCC produces severe low-order harmonics (11th, 13th, etc.) requiring massive filter/capacitor banks, whereas multilevel VSCs (MMC) produce near-perfect sinusoidal voltages."
        )
    ],
    target_idx=0  # Correct is A
)

hd_q2 = build_question(
    qid="Q02",
    title="Q02: Cable Capacitance and HVDC Break-Even Distance",
    category="Cable Physics & Break-Even Distance",
    prompt="Why is HVDC technology practically mandatory for long subsea cable connections (e.g. $> 50\\text{--}80\\text{ km}$) connecting offshore wind farms to the mainland, whereas HVAC cables become infeasible?",
    correct_item=(
        "Insulated cables exhibit high shunt capacitance ($C_{\\text{cable}} \\gg C_{\\text{line}}$), drawing continuous AC charging current ($I_c = \\omega C V$) that thermally saturates long cables; in DC, $d V/dt = 0$, so steady-state charging current is zero.",
        "Correct! AC cable capacitance draws continuous charging current ($I_c = \\omega C V$) that thermally saturates long cables; DC has zero steady-state capacitive charging current.",
        "Insulated underground and subsea cables have small conductor-to-sheath spacing and high dielectric permittivity, resulting in shunt capacitance $20\\text{ to }40$ times higher than overhead lines. Under alternating voltage, this capacitance draws continuous charging current $I_c = \\omega C V$ along the entire length. For subsea AC cables beyond $50\\text{--}80\\text{ km}$, the charging current consumes $100\\%$ of the cable's thermal ampacity ($I_c \\ge I_{\\max}$), so no active power can be delivered unless intermediate reactive compensation is added (impossible offshore). In DC, $d V/dt = 0$, so steady-state charging current is zero."
    ),
    distractor_items=[
        (
            "AC cables experience intense skin effect that forces current to the center of the conductor, whereas DC current flows exclusively along the outer sheath, reducing effective electrical resistance.",
            "Incorrect. Skin effect forces AC current to the outer surface (not center), and direct current distributes uniformly across the conductor cross-section."
        ),
        (
            "High hydrostatic pressure in subsea environments compresses AC dielectric insulation, shifting grid frequency from 50 Hz to 60 Hz over distances exceeding 50 kilometers.",
            "Incorrect. Water pressure has zero influence on electromagnetic frequency; frequency is governed by the rotational speed of synchronized generators."
        ),
        (
            "DC transmission eliminates ohmic resistive losses ($I^2 R = 0$) along the entire conductor, enabling 100% transmission efficiency across thousands of kilometers of subsea links.",
            "Incorrect. Direct current does incur resistive ohmic losses ($I^2 R$); superconductors eliminate resistance, but conventional copper/aluminum DC cables have finite resistance."
        )
    ],
    target_idx=2  # Correct is C
)

hd_q3 = build_question(
    qid="Q03",
    title="Q03: Modeling Embedded VSC-HVDC in Steady-State AC Power Flow",
    category="HVDC in Steady-State Power Flow",
    prompt="When integrating an embedded point-to-point VSC-HVDC transmission link into an AC power flow simulation, how are the sending (rectifier) and receiving (inverter) converter stations mathematically represented in the network equations?",
    correct_item=(
        "As coupled injection buses where scheduled active power is extracted at the sending bus and injected at the receiving bus (minus converter losses), while each terminal independently provides AC voltage control within $(P, Q)$ capability limits.",
        "Correct! In power flow, embedded DC lines model controlled active power transfer with losses, while each terminal independently provides voltage control within reactive limits.",
        "In steady-state power flow, a point-to-point VSC-HVDC link is modeled as two coupled converter terminals: the sending terminal acts as a load extracting active power $P_{\\text{mw}}$ and regulating voltage $V_{m,\\text{from}}$, while the receiving terminal acts as a generator injecting $(1 - \\text{loss}) P_{\\text{mw}}$ and regulating voltage $V_{m,\\text{to}}$. Each terminal behaves as an independent voltage-controlling (PV) source within its converter $(P, Q)$ capability limits. The internal DC physics (DC voltage and current) is decoupled from the AC power flow equations."
    ),
    distractor_items=[
        (
            "As an equivalent AC $\\pi$-model transmission line whose series reactance $X_{\\text{line}}$ and shunt susceptance $B_{\\text{line}}$ are dynamically adjusted to zero by the Newton-Raphson solver.",
            "Incorrect. DC lines cannot be represented as zero-reactance AC lines; that would produce an ill-conditioned singular admittance matrix with division by zero ($1/X \\to \\infty$)."
        ),
        (
            "As two infinite slack buses that fix voltage angles to $\\theta_{\\text{from}} = 0^\\circ$ and $\\theta_{\\text{to}} = 90^\\circ$, absorbing unlimited active and reactive imbalances to guarantee solver convergence.",
            "Incorrect. Converter terminals have finite capacity and specified active power setpoints; they are not infinite slack buses."
        ),
        (
            "As ideal DC current sources that force the entire interconnected AC network to convert from sinusoidal alternating voltages to constant unipolar direct-current potentials.",
            "Incorrect. Embedded VSC-HVDC links interface with AC grids through converter transformers; the surrounding network remains AC."
        )
    ],
    target_idx=1  # Correct is B
)

hd_q4 = build_question(
    qid="Q04",
    title="Q04: Transmission System Flexibility and the 'Duck Curve'",
    category="Duck Curve & N-1 Grid Reinforcement",
    prompt="In a modern transmission grid with massive distributed and utility-scale solar PV generation, what specific transmission system challenge characterizes the late afternoon / evening period (hours 17–20) of the daily 'duck curve'?",
    correct_item=(
        "Rapid solar generation decline coincides with rising evening peak demand, producing steep upward net-load ramp rates ($dP_{\\text{net}}/dt$) that subject transmission corridors to maximum thermal stress and depressed voltages.",
        "Correct! The collapse of solar generation combined with the evening demand peak produces steep upward ramping and heavy transmission corridor loading.",
        "The 'duck curve' reflects net demand ($D_{\\text{net}} = D_{\\text{gross}} - P_{\\text{solar}} - P_{\\text{wind}}$). At midday, high solar output suppresses net demand and relieves transmission corridors. As sunset approaches, solar drops to zero in 2–3 hours exactly when consumer demand reaches its daily evening peak. This produces an extreme positive ramping requirement ($d P_{\\text{net}} / dt$). Remote conventional and hydro units must ramp up rapidly, reversing power flows and subjecting north-to-south transmission corridors to maximum thermal stress and depressed voltages."
    ),
    distractor_items=[
        (
            "Solar inverters back-feed immense reactive power into high-voltage lines, causing Ferranti voltage surges that exceed statutory equipment insulation ratings ($V > 1.30\\text{ pu}$).",
            "Incorrect. Solar inverters shut down as solar irradiance drops to zero at dusk; the problem is depressed voltage under heavy load rather than overvoltages."
        ),
        (
            "The sudden drop in ambient temperature increases transmission line resistance ($R \\propto T^2$), cutting corridor active power transfer capabilities in half right before nighttime.",
            "Incorrect. Conductor resistance decreases with cooler ambient temperatures ($R = R_0[1 + \\alpha(T - T_0)]$), which slightly increases line thermal capacity rather than cutting it."
        ),
        (
            "Grid-scale solar plants disconnect simultaneously due to loss of grid synchronization, collapsing system inertia to zero and permanently reversing European grid frequency.",
            "Incorrect. Solar plants disconnect cleanly as sunlight fades; inertia is provided by spinning conventional/hydro units and synchronous condensers, and frequency does not reverse."
        )
    ],
    target_idx=3  # Correct is D
)

hd_q5 = build_question(
    qid="Q05",
    title="Q05: $N-1$ Contingency Screening and Controllable Transmission Devices",
    category="Duck Curve & N-1 Grid Reinforcement",
    prompt="During an automated $N-1$ contingency screening of a meshed transmission grid, an unexpected branch outage overloads an adjacent corridor. Why can an embedded VSC-HVDC link or a Phase-Shifting Transformer (PST) resolve this bottleneck more effectively than adding a conventional parallel AC line?",
    correct_item=(
        "Power flow on conventional AC lines is governed passively by Kirchhoff's laws and branch reactances ($P_{ij} \\approx \\Delta\\theta_{ij}/X_{ij}$), whereas VSC-HVDC links and PSTs provide active dispatch control, dynamically redirecting power away from congested bottlenecks.",
        "Correct! VSC-HVDC links and PSTs give operators direct active power flow control, allowing power to be routed around congested bottlenecks during contingencies.",
        "In an AC meshed network, power flow splits inversely proportional to branch series reactances ($P_{ij} \\approx \\frac{\\theta_i - \\theta_j}{X_{ij}}$). Adding a conventional parallel AC line can inadvertently attract even more flow through an already constrained path. In contrast, controllable devices break this passive impedance dependence: a Phase-Shifting Transformer (PST) injects a series quadrature voltage that alters the effective phase angle, while a VSC-HVDC link directly enforces a scheduled active power setpoint $P_{\\text{flow}}$. This allows system operators to dynamically redirect power flows away from overloaded corridors during $N-1$ contingencies."
    ),
    distractor_items=[
        (
            "Conventional parallel AC lines always double total system active power losses ($\\Delta P_{\\text{loss}} \\propto 2 I^2 R$), whereas VSC-HVDC links and PSTs operate with negative internal resistance that recovers lost energy.",
            "Incorrect. All physical transmission devices have positive resistive losses; converters introduce ~1% losses per station, and parallel lines generally reduce total resistance ($R/2$)."
        ),
        (
            "Adding parallel AC lines violates European ENTSO-E grid codes by reducing the electrical distance between substations below the minimum statutory threshold of 10 kilometers.",
            "Incorrect. Building parallel circuits on the same right-of-way or separate towers is standard utility practice; no code prohibits parallel AC circuits."
        ),
        (
            "Embedded VSC-HVDC links and PSTs completely eliminate physical short-circuit currents on all surrounding transmission lines, preventing post-contingency fault propagation.",
            "Incorrect. VSC links can limit their own fault current contribution, but they cannot eliminate physical short circuits on surrounding AC transmission lines."
        )
    ],
    target_idx=0  # Correct is A
)


# Assemble Quizzes
QUIZZES = [
    {
        "filename": "Lectures/frequency_control/quiz_frequency_control.html",
        "title": "ELEC0447 - Frequency Control & Distributed Slack Quiz",
        "h1": "Frequency Control &amp; Distributed Slack Quiz",
        "desc": "Interactive practice quiz testing active power balance, kinetic energy and RoCoF, generator speed droop, quasi-steady-state frequency deviations, distributed slack power flow modeling, and secondary control (AGC).",
        "course": "ELEC0447",
        "quiz_id": "frequency_control",
        "quiz_title": "Frequency Control & Distributed Slack",
        "categories": [
            ("Power Balance & Kinetic Energy", "Power Balance & Kinetic Energy"),
            ("Primary Frequency Control & Droop", "Primary Control & Droop"),
            ("Distributed Slack Modeling", "Distributed Slack Modeling"),
            ("Secondary Control (AGC)", "Secondary Control (AGC)"),
        ],
        "questions": [fc_q1, fc_q2, fc_q3, fc_q4, fc_q5]
    },
    {
        "filename": "Lectures/voltage_stability/quiz_voltage_stability.html",
        "title": "ELEC0447 - Voltage Stability & Reactive Power Quiz",
        "h1": "Voltage Stability &amp; Reactive Power Quiz",
        "desc": "Interactive practice quiz testing maximum power transfer, P-V nose curves, saddle-node bifurcations, power factor effects, generator reactive limits, and shunt compensation.",
        "course": "ELEC0447",
        "quiz_id": "voltage_stability",
        "quiz_title": "Voltage Stability & Reactive Power",
        "categories": [
            ("P-V Nose Curves & Maximum Power", "P-V Curves & Maximum Power"),
            ("Power Factor & Reactive Drops", "Power Factor & Reactive Drops"),
            ("Generator Limits (Q-lims)", "Generator Limits (Q-lims)"),
            ("Shunt Compensation & Controls", "Shunt Compensation & Controls"),
        ],
        "questions": [vs_q1, vs_q2, vs_q3, vs_q4, vs_q5]
    },
    {
        "filename": "Lectures/transient/quiz_transient_stability.html",
        "title": "ELEC0447 - Rotor Angle Stability & Grid Strength Quiz",
        "h1": "Rotor Angle Stability &amp; Grid Strength Quiz",
        "desc": "Interactive practice quiz testing generator subtransient reactance, IEC 60909 short-circuit calculation, Equal Area Criterion (EAC), Critical Clearing Time (CCT), synchronizing torque, and Short-Circuit Ratio (SCR).",
        "course": "ELEC0447",
        "quiz_id": "transient_stability",
        "quiz_title": "Rotor Angle Stability & Grid Strength",
        "categories": [
            ("Subtransient Currents & IEC 60909", "Subtransient Currents & IEC 60909"),
            ("Equal Area Criterion & CCT", "Equal Area Criterion & CCT"),
            ("Synchronizing Torque & Small-Signal", "Synchronizing Torque & Small-Signal"),
            ("Short-Circuit Ratio & Grid Strength", "Short-Circuit Ratio & Grid Strength"),
        ],
        "questions": [ts_q1, ts_q2, ts_q3, ts_q4, ts_q5]
    },
    {
        "filename": "Lectures/HVDC/quiz_hvdc.html",
        "title": "ELEC0447 - HVDC & Grid Reinforcement Quiz",
        "h1": "HVDC &amp; Grid Reinforcement Quiz",
        "desc": "Interactive practice quiz testing LCC vs VSC HVDC technologies, cable capacitance limits and break-even distance, embedded DC line power flow modeling, duck curve ramping, and N-1 security reinforcement.",
        "course": "ELEC0447",
        "quiz_id": "hvdc_transmission",
        "quiz_title": "HVDC & Grid Reinforcement",
        "categories": [
            ("LCC vs VSC HVDC Technologies", "LCC vs VSC Technologies"),
            ("Cable Physics & Break-Even Distance", "Cable Physics & Break-Even"),
            ("HVDC in Steady-State Power Flow", "HVDC in Power Flow"),
            ("Duck Curve & N-1 Grid Reinforcement", "Duck Curve & N-1 Reinforcement"),
        ],
        "questions": [hd_q1, hd_q2, hd_q3, hd_q4, hd_q5]
    }
]

for qz in QUIZZES:
    fn = qz["filename"]
    title = qz["title"]
    h1 = qz["h1"]
    desc = qz["desc"]
    cid = qz["quiz_id"]
    ctitle = qz["quiz_title"]
    cats = qz["categories"]
    questions = qz["questions"]

    prefix = prefix_tmpl
    prefix = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', prefix)
    prefix = re.sub(r'<h1>.*?</h1>', f'<h1>{h1}</h1>', prefix)
    desc_pattern = r'<p class="header-desc">.*?</p>'
    new_desc = f'<p class="header-desc">\n                    {desc}\n                </p>'
    prefix = re.sub(desc_pattern, new_desc, prefix, flags=re.DOTALL)
    
    opt_html = '<option value="all">All Topics (5 questions)</option>\n'
    for val, label in cats:
        opt_html += f'                    <option value="{val}">{label}</option>\n'
    
    select_pattern = r'<select id="topic-select" class="select-filter">.*?</select>'
    new_select = f'<select id="topic-select" class="select-filter">\n                    {opt_html}                </select>'
    prefix = re.sub(select_pattern, new_select, prefix, flags=re.DOTALL)

    prefix = re.sub(r'\(12 questions\)', '(5 questions)', prefix)
    prefix = re.sub(r'Question 1 of 12', 'Question 1 of 5', prefix)
    prefix = re.sub(r'0 / 12', '0 / 5', prefix)

    cfg_pattern = r'const QUIZ_CONFIG = \{.*?\};'
    new_cfg = f'''const QUIZ_CONFIG = {{
            course: "{qz["course"]}",
            quiz_id: "{cid}",
            quiz_title: "{ctitle}"
        }};'''
    prefix = re.sub(cfg_pattern, new_cfg, prefix, flags=re.DOTALL)

    q_json = json.dumps(questions, indent=2)

    suffix = suffix_tmpl
    suffix = re.sub(r'You answered <span id="summary-correct">0</span> out of 12', 'You answered <span id="summary-correct">0</span> out of 5', suffix)

    full_html = prefix + "const questions = " + q_json + ";\n" + suffix

    with open(fn, 'w', encoding='utf-8') as out_f:
        out_f.write(full_html)

    # Check answer distribution
    ans_dist = [q["correct"] for q in questions]
    print(f"✅ Generated: {fn} (Correct answer distribution: {ans_dist})")

print("All quizzes generated successfully!")
