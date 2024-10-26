# CAS2SMI

Cas2Smi is a small script to convert CAS number to the isomeric SMILES format using PubChem.

**Author:** &nbsp;&nbsp;Phong Lam<br />
**Email:**  &nbsp;&nbsp;&nbsp;phong.lam@icm.uu.se <br />
**Place:** &nbsp;&nbsp;&nbsp;Jens Carlsson Lab. Uppsala University <br />
**Date:** &nbsp;&nbsp;  2024 </br >

# Installation 

Clone the current repository:

    git clone https://github.com/phonglam3103/cas2smi.git

I will assume that you are familiar with virtual environment concept, for example [Anaconda](https://docs.anaconda.com/anaconda/install/index.html).As the script is fairly small, I would not expect any conflicts with other programs. An example of setting up the environment:

    conda env create -f cas2smi/environment.yml
    conda activate cas2smi
    pip install -e cas2smi

# Usage

## Input

The program requires a comma-separated or tab-separated file containing two columns (Name, CAS) without headers.

```
    o-Tolylboronic acid, 16419-60-6
    3-Hydroxyphenylboronic acid, 87199-18-6
```

OR for excel file:

```
    o-Tolylboronic acid          |   16419-60-6
    3-Hydroxyphenylboronic acid  |   87199-18-6
```

## Usage

The script only takes in the text file or excel file (with the `-xls` flag). Then, for each of the entry, a request will be sent to PubChem to retrieve the isomeric SMILES. The output will be the name of the input with the "_SMILES" subfix.

```bash
cas2smi example.smi
cas2smi boronic_acid.xlsx -xls
```
