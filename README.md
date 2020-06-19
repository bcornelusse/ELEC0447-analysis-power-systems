# ELEC0447 Analysis of Electric Power and Energy Systems

**UNDER CONSTRUCTION**

This is an introductory course on power systems analysis given at Master's level at ULiège.

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
| September 14 | Lecture 1: [Introduction](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture1.md) |
| September 21 | Lecture 2: [3-phase systems](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture2.md) |
| September 28 | Lecture 2: [The transmission line, and power flow analysis part 1](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture3.md) <br> Tutorial: write a power flow in python (apply to the case of the slides). |

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
