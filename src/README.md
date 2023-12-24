# MPI Project

This project implements a factory simulation with the Digital Twin concept using parallel programming techniques. The simulation models interconnected production machines performing various operations on products, aiming to demonstrate the importance of parallel programming in real-life scenarios and showcase implementations of Industry 4.0 principles.


# Prerequisites
-Python
-OpenMPI
-mpi4py

# Installation

1. Install open-mpi with Homebrew
```bash
brew update
brew install open-mpi
```
2. Install mpi4py
```bash
pip install mpi4py
```


# Running the code

on Windows:
```bash
mpiexec -n 1 python main.py input.txt output.txt
```
on MacOS:
```bash
mpiexec --oversubscribe -n 1 python main.py input.txt output.txt
```

# Contact

Huriye Ceylin Gebeş - huriye.gebes@boun.edu.tr
Damla Kayıkçı - damla.kayikci@boun.edu.tr

Project Link: [https://github.com/damlakayikci/MPI-Project](https://github.com/damlakayikci/MPI-Project)