![](/img/Proving_theory.png)

<img alt="Static Badge" src="https://img.shields.io/badge/Downloads%20-%20822KB%20-%20lightblue">
<img alt="Static Badge" src="https://img.shields.io/badge/Python-%20v3.11%2B%20-%20blue">
<img alt="Static Badge" src="https://img.shields.io/badge/Packages-%20PyQt5%2B%20-%20red">
<img alt="Static Badge" src="https://img.shields.io/badge/Packages-%20sympy%20-%20lime">

# Practicing tool for Logic Subject

* [About](#about)
* [Installation](#installation)
* [Run the Program](#run-the-program)
* [Usage](#usage)
* [Maintainers](#maintainers)
* [Feedback](#feedback)

## About

Proof Theory is a syntactic method for examining consequences. This software allows for proof-theoretical derivations.

## Installation

1. Clone the repository.
2. Get the 3.11+ Python interpreter, or create a conda environment.
3. Install `PyQt5` and `sympy` with pip.

## Run the program

Run the program from command line prompt:
1. Set the python path: `set PYTHONPATH=[full path to /src directory]`
2. Change direction to View directory: `cd /src/View`
3. Execute: `python3 main.py` or `python main.py`

## Usage

![](/img/welcome_screen.png)

On the opening screen, users can choose to start a new proof theory configuration or reload a previous one.

![](/img/welcome_screen.png)

On the configuration screen, users can type in a set of formulas and a consequence formula. The program checks that the formulas are valid logical formulas and that brackets are in the correct positions. Further details are available in the help menu.

![](/img/help.png)

Help screen.

![](/img/proof_theory_screen.png)

In the proving area, users can use the hypothesis axiom and various detaching rules. It is also possible to add an axiom, provided the given formula is an axiom. The help section shows further details about rule usage. The hint button attempts to execute a detaching rule if feasible. Users can also save the current derivation.

![](/img/loading_screen.png)

On the loading screen, users can load a previous derivation of a conclusion. The buttons display the saving date, time, and the conclusion. Saves can be deleted.

## Maintainers

Benedek Sz. Csullog (benedek.csullog@gmail.com)

## Feedback

Please use this section to describe how you would like other developers/users to contact you or provide feedback.