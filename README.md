# ELEC0447 Analysis of Electric Power and Energy Systems

**UNDER CONSTRUCTION**

This is an introductory course on power systems analysis given at Master's level at ULiège.

In 2020-2021, the course is scheduled on Mondays from 8:30AM to 12:30AM in room **1.94**, building B28.

We will use eCampus for notifications, homeworks submissions, questions, etc. 

Prerequisites: 
 - Notions of electrical circuits analysis (https://github.com/bcornelusse/livre_circuits_electriques_ELEC0053/)
 - Notions of (complex) calculus
 - Notions of scientific computing (we will use Python)

Instructors: 
 - Bertrand Cornélusse
 - Louis Wehenkel

# Lectures 

| Date | Topic |
| --- | --- |
| September 14 | Lecture 1: [Course organization and introduction](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture1.md) ([pdf](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/lecture1.pdf))|
| September 21 | Lecture 2: [3-phase systems](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture2.md) ([pdf](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/lecture2.pdf)) <br> Practice session: [Python installation instructions](pdf/python_install.pdf), [list of exercises](pdf/ELEC0447_TP1-2.pdf)|
| September 28 | Lecture 3: [The transmission line, and introduction to the power flow analysis](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture3.md) ([pdf](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/lecture3.pdf))<br> Homework: write a power flow in python (apply to the case of the slides). |
| October 5 | Lecture 4: [The transformer and its inclusion in the power flow analysis.](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture4.md) <br> Homework: add a transformer to the power flow problem. |
| October 12 | Lecture 5: [HVDC and its inclusion in the power flow analysis](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture5.md) <br> Homework: add a HVDC line to the power flow analysis. |
| October 19 | Lecture 6: [The synchronous generator and the inclusion of generator limits in the power flow analysis](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture6.md) <br> Homework: add generator limits to the power flow analysis.|
| October 26 | Lecture 7: [Voltage regulation](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture7.md) <br> Homework: .|
| November 9 | Lecture 8: [Transient stability](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture8.md) <br> Homework: .|
| November 16 | Lecture 9: [Frequency control](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture9.md) <br> Homework: .|
| November 23 | Lecture 10: [Fault analysis](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture10.md) <br> Homework: .|


# talk-template

This a fork of the talk template https://github.com/glouppe/talk-template from Gilles Louppe, that uses [remark](https://github.com/gnab/remark) for rendering slides from markdown, [KaTeX](https://github.com/Khan/KaTeX) for typesetting TeX equations, and some customised CSS.

## Instructions for editing

- Clone this repository and move in this repository
- Start an HTTP server to serve the slides:
```
python -m http.server 8001
```
- Edit `lectureX.md` for making your slides.
- Use [decktape](https://github.com/astefanutti/decktape) for exporting slides to PDF.

## Markup language

Slides are written in Markdown. See the remark [documentation](https://github.com/gnab/remark/wiki/Markdown) for further details regarding the supported features.

This template also comes with grid-like positioning CSS classes (see `assets/grid.css`) and other custom CSS classes (see `assets/style.css`)

## Integration with GitHub pages

Slides can be readily integrated with [GitHub pages](https://pages.github.com/) by hosting the files in a GitHub repositery and enabling Pages in the Settings tab.

See e.g. [https://glouppe.github.io/talk-template](https://glouppe.github.io/talk-template). 
