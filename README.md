# ELEC0447: Analysis of Electric Power and Energy Systems

This repository contains the course materials for **ELEC0447 Analysis of Electric Power and Energy Systems**, an introductory Master's-level course taught at the University of Liège (ULiège), Faculty of Applied Sciences.

We use **eCampus** for announcements, discussion, homework submissions, and lecture recordings.

## Instructors

- **Bertrand Cornélusse** (Course Responsible)
- **Francesco Moglia**

## Prerequisites

- **Electrical circuit analysis**: e.g., [Circuits Électriques (ELEC0053)](https://github.com/bcornelusse/livre_circuits_electriques_ELEC0053/)
- **Complex calculus and linear algebra**
- **Scientific computing in Python** (used in exercise sessions and course projects; familiarization with [pandapower](https://www.pandapower.org/) is recommended)

## Course Schedule (2026–2027)

> **Note:** Complete problem statements and detailed step-by-step solutions for all practical sessions (TP1 to TP6) are gathered in the **[Exercise Manual (PDF)](Exercises/ELEC0447_exercise_manual.pdf)** (LaTeX sources in [`Exercises/`](Exercises/)).

| Date | Lecture | Topics & Materials |
|:---|:---:|:---|
| September 17 | 1 | [Course organization and introduction](Lectures/Introduction/main.pdf) |
| | | [Sinusoidal steady-state analysis](Lectures/SSSA/main.pdf) |
| | | [Exercises on sinusoidal steady-state analysis (TP1)](Exercises/ELEC0447_exercise_manual.pdf#page=3) (Section 1) |
| September 24 | 2 | [3-phase systems, per unit normalization](Lectures/ThreePhaseAndPu/main.pdf) |
| | | [Exercises on 3-phase systems, per unit normalization (TP2)](Exercises/ELEC0447_exercise_manual.pdf#page=7) (Section 2) |
| October 1 | 3 | [The transmission line](Lectures/TransmissionLine/main.pdf) — **[Interactive Quiz](https://people.montefiore.uliege.be/cornelusse/ELEC0447/quiz_transmission_lines.html)** ([local](Lectures/TransmissionLine/quiz_transmission_lines.html)) |
| | | [Introduction to the power flow analysis](Lectures/IntroPowerFlow/main.pdf) — **[Interactive Quiz](https://people.montefiore.uliege.be/cornelusse/ELEC0447/quiz_power_flow.html)** ([local](Lectures/IntroPowerFlow/quiz_power_flow.html)) |
| | | [Exercises on transmission lines (TP3)](Exercises/ELEC0447_exercise_manual.pdf#page=14) (Section 3) |
| | | [Project 1: Two-feeder distribution network analysis with PandaPower](Projects/Project_1/ELEC0447_project1_2026.pdf) and [Data](Projects/Project_1/ELEC0447_project_1_2026_network.xlsx) |
| October 8 | 4 | [The transformer and its inclusion in the power flow analysis](Lectures/TransfomerAndPF/main.pdf) — **[Interactive Quiz](https://people.montefiore.uliege.be/cornelusse/ELEC0447/quiz_transformers.html)** ([local](Lectures/TransfomerAndPF/quiz_transformers.html)) |
| | | [Exercises on transformers (TP4)](Exercises/ELEC0447_exercise_manual.pdf#page=20) (Section 4) |
| October 15 | 5 | [The synchronous generator and the inclusion of generator limits in the power flow analysis](Lectures/SynchronousGenerator/main.pdf) |
| | | [Exercises on synchronous machines (TP5)](Exercises/ELEC0447_exercise_manual.pdf#page=26) (Section 5) |
| | | Q&A: Project 1 |
| October 22 | — | *No lecture — team is at IEEE PES ISGT Europe 2026 in Budapest* |
| October 29 | — | *No lecture — Autumn break* |
| November 5 | 6 | **Project 1 assessment** (presence is mandatory) |
| November 12 | 7 | [HVDC and its inclusion in the power flow analysis](Lectures/HVDC/main.pdf) |
| | | Project 2 statement: Transmission network analysis with PandaPower *(see on eCampus)* |
| November 19 | 8 | [Introduction to stability and control problems](Lectures/intro_stability/intro_stability.pdf) *(video on eCampus)* |
| | | [Frequency control](Lectures/frequency_control/main.pdf) |
| November 26 | 9 | [Voltage regulation](Lectures/voltage_stability/voltage_stability.pdf) *(video on eCampus)* |
| | | [Exercises on voltage (in)stability (TP6)](Exercises/ELEC0447_exercise_manual.pdf#page=31) (Section 6) |
| December 3 | 10 | [Transient stability](Lectures/transient/main.pdf) *(video on eCampus)* |
| December 10 | 11 | **Visit to Elia's national dispatch center** (presence is mandatory) |
| December 17 | 12 | **Project 2 assessment** (presence is mandatory) |
| January | — | Oral exam — [List of questions](Evaluation/ELEC0447_exam_questions.pdf) |

### Interactive Self-Assessment Quizzes

Web-based practice quizzes with step-by-step navigation, KaTeX math rendering, immediate feedback with detailed pedagogical analyses, and centralized grade submission:

- ⚡ **Transmission Lines & Line Rating**: **[Online Quiz](https://people.montefiore.uliege.be/cornelusse/ELEC0447/quiz_transmission_lines.html)** | [Source HTML](Lectures/TransmissionLine/quiz_transmission_lines.html)
  - *Topics*: Conductor physics & skin effect, surge impedance loading (SIL), lumped $\pi$ model validity, catenary sag & ground clearances, Static vs. Dynamic Line Rating (SLR/DLR).
- 🔄 **Power Flow Analysis**: **[Online Quiz](https://people.montefiore.uliege.be/cornelusse/ELEC0447/quiz_power_flow.html)** | [Source HTML](Lectures/IntroPowerFlow/quiz_power_flow.html)
  - *Topics*: Bus classification (PQ, PV, Slack), nodal admittance matrix $\mathbf{Y}_{\text{bus}}$, Newton-Raphson quadratic convergence & sparsity, generator reactive limits ($Q_{\min}/Q_{\max}$), Fast Decoupled and DC linear power flow, and grid overload remediation.
- ⚙️ **Transformers & Per-Unit Power Flow**: **[Online Quiz](https://people.montefiore.uliege.be/cornelusse/ELEC0447/quiz_transformers.html)** | [Source HTML](Lectures/TransfomerAndPF/quiz_transformers.html)
  - *Topics*: IEC nameplate test data ($v_k\%, v_{kr}\%$), per-unit referral invariance, vector groups (Dyn11), auto-transformer core sizing ($k_{\text{size}}$), On-Load Tap Changers (OLTC), Phase-Shifting Transformers (PST quadrature boost), and two-port $\mathbf{Y}_{\text{bus}}$ matrix stamping.

> **Configuring Centralized Google Sheet Submissions:**  
> All quizzes submit to a single Google Apps Script endpoint. To collect student responses into your Google Sheet, follow the quick 2-minute setup instructions in [`Lectures/google_apps_script.js`](Lectures/google_apps_script.js) and update the `GOOGLE_SCRIPT_URL` constant. Submissions will automatically log to a master tab and to dedicated tabs per quiz.

### Extra Module: Usual Transforms in Power Systems (Self-Study / Reference)

> **Note for students:** This self-study module covers essential coordinate transformations and network decompositions used across power system analysis, converter control, and protection. It will not be covered during live lectures, but it will be referred to from time to time throughout the course. Students are encouraged to review these materials to build intuition.

- **Lecture Slides**: **[Usual Transforms in Power Systems (PDF)](Lectures/transforms/main.pdf)** (LaTeX sources in [`Lectures/transforms/`](Lectures/transforms/))
- **Interactive Notebook**: [`Lectures/transforms/transforms.ipynb`](Lectures/transforms/transforms.ipynb)
- **Python Module**: [`Lectures/transforms/transforms.py`](Lectures/transforms/transforms.py)

#### Topics Covered:
1. **Motivation**: Overcoming electromagnetic phase coupling, time-varying machine inductances, network asymmetries, and high dimensionalities.
2. **Fortescue Symmetrical Components ($012$)**: Direct, inverse, and zero sequence decomposition; sequence networks and decoupling; sequence impedances ($Z_1, Z_2, Z_0$); unsymmetrical fault calculation (SLG, L-L); and protection relays (ANSI 46, 50N/51N).
3. **Clarke Transform ($\alpha\beta0$)**: 3-phase to 2-axis stationary orthogonal frame; amplitude vs. power invariance; space vector circular trajectories under balanced conditions and elliptical trajectories under unbalances; Space Vector PWM (SVPWM).
4. **Park Transform ($dq0$) & Grid Synchronization**: Transforming AC sinusoids into constant DC steady-state quantities; decoupled active and reactive vector control ($P \propto i_d, Q \propto -i_q$); appearance of the $2\omega$ (100 Hz) unbalance ripple; and Synchronous Reference Frame PLL (SRF-PLL).
5. **Cross-Domain Bridges**: Explicit mappings connecting Fortescue sequence phasors, Clarke space vector orbits, and Park rotating DC/ripple components.
6. **Kron Network Reduction**: Mathematical elimination of passive (zero-injection) buses via the Schur complement ($\mathbf{Y}_{\text{Kron}} = \mathbf{Y}_{GG} - \mathbf{Y}_{GL}\mathbf{Y}_{LL}^{-1}\mathbf{Y}_{LG}$) for transient stability simulation and dynamic equivalents.
7. **Full-Cycle Discrete Fourier Transform (DFT)**: Fundamental frequency phasor extraction from sampled waveforms, with complete integer harmonic and DC offset rejection for digital distance protection and PMUs.

## Repository Structure

- [`Lectures/`](Lectures/): LaTeX Beamer slide decks for all lectures, the self-study module on transforms ([`Lectures/transforms/`](Lectures/transforms/)), and the compilation script [`compile_all.sh`](Lectures/compile_all.sh).
- [`Exercises/`](Exercises/): Complete exercise manual containing problem statements and step-by-step solutions for TP1 through TP6, authored in modular LaTeX (`ELEC0447_exercise_manual.tex`, `tp1_phasor_analysis.tex` to `tp6_voltage_stability.tex`) and the compiled document [`ELEC0447_exercise_manual.pdf`](Exercises/ELEC0447_exercise_manual.pdf).
- [`pdf/`](pdf/): Project descriptions, data sheets, and past exam questions.
- [`notebooks/`](notebooks/): Python and Jupyter notebooks for tutorials, power flow algorithms (Newton–Raphson, DC power flow), and [pandapower](https://www.pandapower.org/) examples.
- [`PandapowerProject/`](PandapowerProject/): Assignment material and LaTeX sources for projects.

## Compiling the Exercise Manual

The complete exercise manual in `Exercises/` can be compiled using `pdflatex`:

```bash
cd Exercises
pdflatex ELEC0447_exercise_manual.tex
pdflatex ELEC0447_exercise_manual.tex   # Run a second time to update table of contents
```

## Compiling LaTeX Lecture Slides

The Beamer lecture slides located in `Lectures/` can be compiled using the compilation script [`Lectures/compile_all.sh`](Lectures/compile_all.sh):

```bash
cd Lectures

# Compile all slide decks
./compile_all.sh

# Or compile specific decks only (supports deck names or aliases like sssa, lecture5, syncgen)
./compile_all.sh SSSA SynchronousGenerator Introduction

# Compile and clean auxiliary files (.aux, .log, .toc, etc.)
./compile_all.sh -c
```

The script automatically detects `latexmk` or falls back to `pdflatex`, running the required passes and bibliographies (`bibtex` / `biber`).

