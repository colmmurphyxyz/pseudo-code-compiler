# Pseudo-Code Compiler
pcc is a project that attempts to transpile pseudocode to executable Python.
The dialect of pseudocode used is that of 'Introduction to Algorithms - 4th Edition' by Thomas H. Cormen, 
Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein.

## Supported Python versions
The project has only been tested with Python 3.12.7, though any Python later than ~3.10 should work.

## Usage
### Via installation Script
**Windows**: [pcc_init.ps1](https://colmmurphy.xyz/pcc_init.ps1)
**Mac/Linux**: [pcc_init.sh](https://colmmurphy.xyz/pcc_init.sh)
```shell
git clone [git@github.com:colmmurphyxyz/pcc.git](https://github.com/colmmurphyxyz/pseudo-code-compiler.git)
python3 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
```
From the root directory of the project...
```shell
python3 pcc/pcc.py res/pc_examples/ch02/insertion_sort.pc
```
The transpiled Python program will be printed to the standard output, and also written to `out/out.py`

## Documentation
TODO...
