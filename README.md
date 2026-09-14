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
| October 1 | 3 | [The transmission line](Lectures/TransmissionLine/main.pdf) |
| | | [Introduction to the power flow analysis](Lectures/IntroPowerFlow/main.pdf) |
| | | [Exercises on transmission lines (TP3)](Exercises/ELEC0447_exercise_manual.pdf#page=14) (Section 3) |
| | | [Project 1: Two-feeder distribution network analysis with PandaPower](pdf/ELEC0447_project_1_2025.pdf) and [Data](pdf/ELEC0447_project_1_2025_network.xlsx) |
| October 8 | 4 | [The transformer and its inclusion in the power flow analysis](Lectures/TransfomerAndPF/main.pdf) |
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
| December 10 | 11 | (TBC) Visit to Elia's national dispatch center *(organizational details on eCampus)* |
| December 17 | 12 | **Project 2 assessment** (presence is mandatory) |
| January | — | Oral exam — [List of theoretical questions](pdf/20231212_ELEC0447_exam_questions.pdf) |

## Repository Structure

- [`Lectures/`](Lectures/): LaTeX Beamer slide decks for all lectures and the compilation script [`compile_all.sh`](Lectures/compile_all.sh).
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

