# ELEC0447 Analysis of Electric Power and Energy Systems

This is an introductory course on power systems analysis given at the Master's level at ULiège.

We will use eCampus for notifications, homework submissions, questions, etc. 

Prerequisites: 
 - Notions of electrical circuits analysis (https://github.com/bcornelusse/livre_circuits_electriques_ELEC0053/)
 - Notions of (complex) calculus
 - Notions of scientific computing (we will use Python)

Instructors: 
 - Bertrand Cornélusse
 - Antonin Colot

# Lectures (2024-2025) - tentative schedule, subject to change.

| Date | Lecture | Topics |
| --- | --- | --- |
| September 19 | 1 | [Course organization and introduction](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture1_intro.md) ([pdf file](pdf/lecture1_intro.pdf)) |
|              |   | [Sinusoïdal steady-state analysis](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture1_SSSA.md) ([pdf file](pdf/lecture1_SSSA.pdf))|
|              |   | [List of exercises on sinusoïdal steady-state analysis](pdf/ELEC0447-TP1.pdf) |
| September 26 | 2 | [3-phase systems, per unit normalization](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture2_3ph_pu.md) ([pdf file](pdf/lecture2_3ph_pu.pdf)) |
|              |   | Test on sinusoïdal steady-state analysis. Do it on your own, and submit it on Gradescope. |
| October  3   | 3 | [The transmission line and introduction to the power flow analysis](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture3_tl_pf1.md) ([pdf file](pdf/lecture3_tl_pf1.pdf))|
|              |   | [Exercises on 3-phase systems, per unit normalization](pdf/ELEC0447-TP2.pdf) |
| October 10   | 4 | [Power flow analysis - solution methods](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture3_tl_pf1.md#28) ([pdf file](pdf/lecture3_tl_pf1.pdf))|
|              |   | [Exercises on transmission lines](pdf/ELEC0447-TP3.pdf)||
| October 17   | 5 | [The transformer and its inclusion in the power flow analysis](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture4.md) ([pdf](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/lecture4.pdf)) |
|              |   | Assignment 1: Implement power flow analysis on a 4-bus test system [Case 0 solved during the practice session](pdf/CASE0.pdf) |
| October 24   | 6 | [The synchronous generator and the inclusion of generator limits in the power flow analysis](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture5.md) ([pdf](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/lecture5.pdf))|
|              |   | [HVDC and its inclusion in the power flow analysis](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture6.md) ([pdf](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/lecture6.pdf)) |
|              |   | [Exercises on transformers](pdf/ELEC0447-TP4.pdf) |
|              |   | [Assignment 2: add a transformer and generator limits in power flow analysis on a 4-bus test system](pdf/statement0_solved_pf2.pdf) |
| November 7   |  7 |   [Voltage regulation](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture7_aclt.md) ([pdf](pdf/lecture7_aclt.pdf))  |
|              |   | [PandaPower project (part 1) zip](PandapowerProject/2023_pandapower_project.zip) & [VS code & Python notebook tutorial](https://shorturl.at/kpuzE)|
| November 14  | 8 |  [Control of interconnected power systems and economic dispatch](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture9_frequency_control_2023_bcr.md) ([pdf](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/lecture9_frequency_control_2023_bcr.pdf)) |
|              |   | [Exercises on synchronous machines](pdf/ELEC0447-TP5.pdf) & Q&A session Pandapower project pt. I|
| November 21  | 9 |  [Transient stability](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=Lecture9_aclt.md) ([pdf](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/lecture9_aclt.pdf)) |
|              |   | [Exercises on voltage (in)stability](pdf/ELEC0447-TP6.pdf) & Q&A session Pandapower project pt. I and pt. II |
| November 28  | 10 | Visit of Elia's national dispatch center (organizational details on ecampus) |
| December 5   | 11 | Seminar by Dr. Gilles Chaspierre, Elia Grid International. |
|              |    | Seminar by Daniel Mitcan, CTO of Ampacimon. |
|              |    | [Exercises on primary frequency control](pdf/ELEC0447-TP8.pdf) & Q&A session Pandapower project pt. II|
| December 12  | 12 | Oral presentation of PandaPower project results by students. |
| December 19  | 13 | Q&A if needed |
| January      |  | Oral exam,  [list of questions](pdf/20231212_ELEC0447_exam_questions.pdf) |


# talk-template

This a fork of the talk template https://github.com/glouppe/talk-template from Gilles Louppe, that uses [remark](https://github.com/gnab/remark) for rendering slides from markdown, [KaTeX](https://github.com/Khan/KaTeX) for typesetting TeX equations, and some customised CSS.

## Instructions for editing

- Clone this repository and move in this repository
- Start an HTTP server to serve the slides:
```
python -m http.server 8001
```
- Edit `lectureX.md` for making your slides.
- Use [decktape](https://github.com/astefanutti/decktape) for exporting slides to PDF:

  - download and install *node.js* (a recent version)
  - install decktape: 

    npm install -g decktape

 
  - ensure an http server is running, e.g. on localhost at port 8001, from the directory where the sources are

    python -m http.server 8001 

  - run decktape: 

    decktape http://0.0.0.0:8001/?p=lecture7.md pdf/lecture7.pdf




## Markup language

Slides are written in Markdown. See the remark [documentation](https://github.com/gnab/remark/wiki/Markdown) for further details regarding the supported features.

This template also comes with grid-like positioning CSS classes (see `assets/grid.css`) and other custom CSS classes (see `assets/style.css`)

## Integration with GitHub pages

Slides can be readily integrated with [GitHub pages](https://pages.github.com/) by hosting the files in a GitHub repositery and enabling Pages in the Settings tab.

See e.g. [https://glouppe.github.io/talk-template](https://glouppe.github.io/talk-template). 
