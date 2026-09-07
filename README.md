# ELEC0447 Analysis of Electric Power and Energy Systems

This is an introductory course on power systems analysis given at the Master's level at ULiège.

We will use eCampus for notifications, homework submissions, questions, etc. 

Prerequisites: 
 - Notions of electrical circuits analysis (https://github.com/bcornelusse/livre_circuits_electriques_ELEC0053/)
 - Notions of (complex) calculus
 - Notions of scientific computing (we will use Python)

Instructors: 
 - Bertrand Cornélusse
 - Francesco Moglia

# Lectures (2026-2027).

| Date | Lecture | Topics |
| --- | --- | --- |
|	 September 17 	|	1	|	 [Course organization and introduction](Lectures/Introduction/main.pdf)	|
|	              	|	  |	 [Sinusoidal steady-state analysis](Lectures/SSSA/main.pdf)	|
|	              	|	  |	 [List of exercises on sinusoïdal steady-state analysis](pdf/ELEC0447-TP1.pdf) 	|
|	 September 24  |	2 |	 [3-phase systems, per unit normalization](Lectures/ThreePhaseAndPu/main.pdf)	| 
|	              	|	  |	 [Exercises on 3-phase systems, per unit normalization](pdf/ELEC0447-TP2.pdf) 	|
|	 October  1   	|	3	|	 [The transmission line](Lectures/TransmissionLine/main.pdf) |
|	 	             |	 	|	 [Introduction to the power flow analysis](Lectures/IntroPowerFlow/main.pdf)	|
|           	   	|	 	|	 [Project 1: Two-feeder distribution network analysis with PandaPower](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/ELEC0447_project_1_2025.pdf)	and [Data](https://bcornelusse.github.io/ELEC0447-analysis-power-systems/pdf/ELEC0447_project_1_2025_network.xlsx)|
|	 October 8   	 |	4	|	 [The transformer and its inclusion in the power flow analysis](Lectures/TransfomerAndPF/main.pdf) 	|
|	              	|	  |	Q&A Project 1 |
|	              	|	  |	 [Exercises on transmission lines](pdf/ELEC0447-TP3.pdf)	|
|	 October 15   	|	5	|	 [The synchronous generator and the inclusion of generator limits in the power flow analysis](Lectures/SynchronousGenerator/main.pdf)	|
|	              	|	 	|	[Exercises on transformers](pdf/ELEC0447-TP4.pdf)|
|	 October 22   	|	- | ??? |
|	 October 29   	|	- | No lecture - Autumn break |
|	 November 5   	|	6 |	Presentation of the Energy Challenge related project: designing the distribution network of your virtual campus |
|	              	|	  |	[HVDC and its inclusion in the power flow analysis](Lectures/HVDC/main.pdf) |
|	              	|	  |	Q&A Project 1 |
|	               |	 	|	[Exercises on synchronous machines](pdf/ELEC0447-TP5.pdf) 	|
|	November 12    |	7	|	Project 1 presentations by students.  	|
|	 November 19 	 |	8	|	[Frequency control](Lectures/frequency_control/main.pdf)  	|
|	              	|	  |	Project 2 statement: Transmission network analysis with PandaPower (see on ecampus).	|
|	 November 26  	|	9	|	Frequency control, end	|
|	 December 3  	 |	10	|	[Introduction to stability and control problems](Lectures/intro_stability/intro_stability.pdf) (video on ecampus) 	|
|                |    | [Voltage regulation](Lectures/voltage_stability/voltage_stability.pdf) (videos on ecampus)	|
|	              	|	   |	[Exercises on voltage (in)stability](pdf/ELEC0447-TP6.pdf) |
|	 December 10   |	11	|	 [Transient stability](Lectures/transient/main.pdf) (videos on ecampus) |
|	 December 17  	|	12	|	 (TBC) Visit of Elia's national dispatch center (organizational details via ecampus) 	|
|	 January      	|	  	|	 Oral exam,  [list of questions](pdf/20231212_ELEC0447_exam_questions.pdf) 	|



# Compiling LaTeX Lecture Slides

The Beamer lecture slides located in `Lectures/` can be compiled using the compilation script [`Lectures/compile_all.sh`](Lectures/compile_all.sh):

```bash
cd Lectures

# Compile all slide decks
./compile_all.sh

# Or compile specific decks only
./compile_all.sh SSSA Introduction

# Compile and clean auxiliary files (.aux, .log, .toc, etc.)
./compile_all.sh -c
```
