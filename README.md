# ELEC0447 Analysis of Electric Power and Energy Systems

This is an introductory course on power systems analysis given at Master's level at ULiège.

We will use eCampus for notifications, homeworks submissions, questions, etc. 

Prerequisites: 
 - Notions of electrical circuits analysis (https://github.com/bcornelusse/livre_circuits_electriques_ELEC0053/)
 - Notions of (complex) calculus
 - Notions of scientific computing (we will use Python)

Instructors: 
 - Bertrand Cornélusse
 - Louis Wehenkel

# Lectures (2022-2023) 

| Date | Lecture | Topics |
| --- | --- | --- |
| September 15 | 1 | [Course organization and introduction](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture1_intro.md) ([pdf file](pdf/lecture1_intro.pdf)) |
|              |   | [Sinusoïdal steady-state analysis](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture1_SSSA.md) ([pdf file](pdf/lecture1_SSSA.pdf))|
|              |   | [List of exercises on sinusoïdal steady-state analysis](pdf/ELEC0447-TP1.pdf) |
| September 22 | 2 | [3-phase systems, per unit normalization](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture2_3ph_pu.md) ([pdf file](pdf/lecture2_3ph_pu.pdf))|
|              |   | Mandatory test on sinusoïdal steady-state analysis |
|              |   |  |
| September 29 | 3 | [The transmission line, and introduction to the power flow analysis](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture3_tl_pf1.md) ([pdf file](pdf/lecture3_tl_pf1.pdf))|
|              |   | [Exercises on 3-phase systems, per unit normalization](pdf/ELEC0447-TP2.pdf) |
| October 6    | 4 | [Power flow analysis - solution methods](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture3_tl_pf1.md#28) ([pdf file](pdf/lecture3_tl_pf1.pdf))|
|              |   | [The transformer and its inclusion in the power flow analysis](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture4.md) ([pdf](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/lecture4.pdf)) |
|              |   | [Exercises on transmission lines](pdf/ELEC0447-TP3.pdf)|
|              |   | Assignment 1: implement power flow analysis on a 4-bus test system, submit on GradeScope. [Case 0 solved during the practice session](pdf/CASE0.pdf) |
| October 13   | 5 | [The synchronous generator and the inclusion of generator limits in the power flow analysis](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture5.md) ([pdf](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/lecture5.pdf))|
|              |   | [Exercises on transformers](pdf/ELEC0447-TP4.pdf) |
| October 20   | 6 | [HVDC and its inclusion in the power flow analysis](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture6.md) ([pdf](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/lecture6.pdf)) |
|              |   | [Assignment 2: add a transformer and generator limits in power flow analysis on a 4-bus test system](pdf/statement0_solved_pf2.pdf). Submit on GradeScope. |
|              |   | [Exercises on synchronous machines](pdf/ELEC0447_TP5.pdf)|
| October 27   | NO LECTURE | 
| November 10  | 7 | [Voltage regulation](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture7.md) ([pdf](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/lecture7.pdf))  |
|              |   | [Exercises on voltage (in)stability](pdf/ELEC0447-TP6.pdf) |
|              |   | [PandaPower project description](PandapowerProject/2022_pandapower_project_ELEC0447.pdf) and [code template](https://colab.research.google.com/drive/10quG_fRyqRbz1JwFu6GGfXqlMp_1dKyO?usp=sharing)|
| November 17  | 8 | [Transient and dynamic stability](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture8.md) ([pdf](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/lecture8.pdf)) |
|              |   | [Exercises session](pdf/ELEC0447-TP7.pdf) |
| November 24   | 9 | [Control of interconnected power systems and economic dispatch](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture9.md) ([pdf](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/lecture9.pdf)) |
|              |   | [Exercises session](pdf/ELEC0447-TP8.pdf) |
| December 1   | 10 | Seminar by Dr. Gilles Chaspierre, Elia Grid International. |
|              |    | Seminar by Dr. Bertrand Godard, Ampacimon. 
| December 8   | 11 | Oral presentation of PandaPower project results by students|
| December 15   | 12 | No activity planned for now |



# Old lectures (2021-2022)

| Date | Lecture | Topics |
| --- | --- | --- |
| September 16 | 1 | [Course organization and introduction](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture1_intro.md) ([pdf file](pdf/lecture1_intro.pdf))|
|              |   | [Sinusoïdal steady-state analysis](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture1_SSSA.md) ([pdf file](pdf/lecture1_SSSA.pdf))|
|              |   | [List of exercises on sinusoïdal steady-state analysis](pdf/ELEC0447-TP1.pdf) |
| September 23 | 2 | [3-phase systems, per unit normalization](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture2_3ph_pu.md) ([pdf file](pdf/lecture2_3ph_pu.pdf))|
|              |   | Mandatory test on sinusoïdal steady-state analysis |
|              |   | [**Test solution and statistics on results**](notebooks/Test1_solved.ipynb) |
| September 30 | 3 | [The transmission line, and introduction to the power flow analysis](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture3_tl_pf1.md) ([pdf file](pdf/lecture3_tl_pf1.pdf))|
|              |   | [Exercises on 3-phase systems, per unit normalization](pdf/ELEC0447-TP2.pdf) |
| October 7    | 4 | [Power flow analysis - solution methods](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture3_tl_pf1.md#28) ([pdf file](pdf/lecture3_tl_pf1.pdf))|
|              |   | [The transformer and its inclusion in the power flow analysis](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture4.md) ([pdf](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/lecture4.pdf)) |
|              |   | [Exercises on transmission lines](pdf/ELEC0447-TP3.pdf)|
|              |   | Assignment 1: implement power flow analysis on a 4-bus test system, submit on GradeScope. [Case 0 solved during the practice session](pdf/statement0_solved.pdf) |
| October 14   | 5 | [The synchronous generator and the inclusion of generator limits in the power flow analysis](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture5.md) ([pdf](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/lecture5.pdf))|
|              |   | [Exercises on transformers](pdf/ELEC0447-TP4.pdf) |
| October 21   | 6 | [Exercises on synchronous machines](pdf/ELEC0447_TP5.pdf) (starts at 13:45)|
|              |   | [Assignment 2: add a transformer and generator limits in power flow analysis on a 4-bus test system](pdf/statement0_solved_pf2.pdf). Submit on GradeScope. |
|              |   | [HVDC and its inclusion in the power flow analysis](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture6.md) ([pdf](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/lecture6.pdf)) (please watch the video available on eCampus) |
| October 28   | 7 | [Voltage regulation](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture7.md) ([pdf](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/lecture7.pdf))  |
|              |   | [PandaPower project description](PandapowerProject/2021_pandapower_project_ELEC0447.pdf) and [code template](https://colab.research.google.com/drive/1laIHGFlrfPkd_WFO0_UyB-wjXEZEzHoX?usp=sharing)|
| November 18  | 8 | [Transient and dynamic stability](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture8.md) ([pdf](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/lecture8.pdf)) |
|              |   | [Exercises on voltage (in)stability](pdf/ELEC0447-TP6.pdf) |
| November 25  | 9 | [Control of interconnected power systems and economic dispatch](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/?p=lecture9.md) ([pdf](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/lecture9.pdf)) |
|              |   | [Exercises session](pdf/ELEC0447-TP7.pdf) |
| December 2   | 10 | Q&A session |
| December 9   | 11 | Q&A session |
| December 16   | 11 | Oral presentation of PandaPower project results by students|




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
