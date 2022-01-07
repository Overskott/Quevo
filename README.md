# Evolving-quantum-circuits

This code is created for a pilot project done trough the [NordSTAR](https://www.oslomet.no/nordstar) research group at Oslo Meteropolitan university. It generates simulated quantum circuits to fit a desired probability outcome for eight initial conditions.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This code is creating quantum circuits for use with cellular automata. It uses an evolutionary algorithm to create quantum circuits with Qiskit. 

The circuit is represented as a list of integers, where each gate is three successive integers i.e.:

Three random gates as list:

`[2, 0, 1, 3, 1 ,1, 4, 0, 2]`

Gate 1 = 201, gate 2= 311, gate 3 = 402


The first int is what kind of gate it is (i.e. X-gate, CNOT, Hadamard).
The second int is what qubit is this assigned to (0 -> qubit 0, 1 -> qubit 1, ...)
The third int is what qubit is controlling the gate. in cases where gates do not have an
external controller, this int is ignored.

The table describing int, corresponding gate and if it uses control qubit, yes or no (Y/N):

| Int |  Gate   | Control |
| --- |:-------:| -------:|
|  0  | Hadamard|   N     |
|  1  | C-NOT   |   Y     |
|  2  | X	|   N     | 
|  3  | Swap    |   Y     |
|  4  | RZZ     |   Y     |
|  5  | RXX     |   Y     |
|  6  | Z       |   N     |
|  7  | Y       |   N     |

 

Some gates (RZZ, RXX) also need an angle value (theta) stored in a separate list. `theta in (0, 2*pi)`

## Technologies
Project is created with:
* Python version: 3.8 
* Qiskit version: 0.34.1



	
## Setup
This project uses Qiskit. The best way of installing qiskit is by using pip: `$ pip install qiskit`



```bash
$ pip install qiskit
```
