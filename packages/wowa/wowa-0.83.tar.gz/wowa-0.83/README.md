# wowa
This package calculates weighted OWA functions and extending bivariate means" Functions are:
- py_WAM: WOWATree callback function if sorting is needed in general 
- py_OWA: WOWATree callback function if no sorting is needed when used in the tree
- WOWATree: symmetric base aggregator 
- WAn: processes the tree
- weightedOWAQuantifierBuild: calculates spline knots and coefficients for later use in weightedOWAQuantifier
- weightedOWAQuantifier: Calculates the value of the WOWA, with quantifier function obtained in weightedOWAQuantifierBuild
- ImplicitWOWA: Calculates implicit Weighted OWA function

## Documentation
[User Manual](https://github.com/nhenseler/wowa/blob/main/docs/wowa-theory.pdf)

## Installation
To install type:
```python
$ pip install wowa
```
## Usage of py_OWA( n, x, w)
```python
from wowa import py_OWA
```
WOWATree callback function if sorting is needed in general 
### Parameters
#### Input parameters:
Input parameters:
n: size of arrays<br>
x[]: NumPy array of size n, float<br>
w[]: NumPy array of size n, float<br>
#### Output parameters:
double y: aggregated sum 

## Usage of py_WAM( n, x, w)
```python
from wowa import py_WAM
```
WOWATree callback function if no sorting is needed when used in the tree
### Parameters
#### Input parameters:
Input parameters:
n: size of arrays<br>
x[]: NumPy array of size n, float<br>
w[]: NumPy array of size n, float<br>
#### Output parameters:
double y: aggregated sum 

## Usage of WOWATree( x, p, w, cb, L)
```python
from wowa import WOWATree
```
Symmetric base aggregator. The weights must add to one and be non-negative.
### Parameters
#### Input parameters:
x[]: NumPy array of inputs, size n, float<br> 
p[]: NumPy array of weights of inputs x[], size n, float<br> 
w[]: NumPy array of weights for OWA, size n, float<br>
cb: callback function<br>
L: number of binary tree levels. Run time = O[(n-1)L]  
#### Output parameters:
y = weightedf, double<br>

## Usage of WAn(double * x, double * w, int L, double(*F)( double, double))
```python
from wowa import WAn
```
### Parameters
#### Input parameters:
x[]: NumPy array of inputs, size n, float<br> 
w[]: NumPy array of weights for OWA, size n, float<br>
L: umber of binary tree levels
F: callback function<br>
#### Output parameters:
y = result of tree processing, double<br>

## Usage of weightedOWAQuantifierBuild( double p[], double w[], double temp[], int *T)
```python
from wowa import weightedOWAQuantifierBuild
```
### Parameters
p[]: NumPy array of weights of inputs x[], size n, float<br> 
w[]: NumPy array of weights for OWA, size n, float<br>
temp[]:
T:
#### Input parameters:
#### Output parameters:
no output<br>


## Usage of weightedOWAQuantifier(double x[], double p[], double w[], double temp[], int T);
```python
from wowa import weightedOWAQuantifier
```
Calculates the value of the WOWA, with quantifier function obtained in weightedOWAQuantifierBuild
### Parameters
x[]: NumPy array of inputs, size n, float<br> 
p[]: NumPy array of weights of inputs x[], size n, float<br> 
w[]: NumPy array of weights for OWA, size n, float<br>
#### Input parameters:
#### Output parameters:
y = double<br>


## Usage of ImplicitWOWA(double x[], double p[], double w[])
```python
from wowa import ImplicitWOWA
```
Calculates implicit Weighted OWA function
### Parameters
#### Input parameters:
x[]: NumPy array of inputs, size n, float<br> 
p[]: NumPy array of weights of inputs x[], size n, float<br> 
w[]: NumPy array of weights for OWA, size n, float<br>
#### Output parameters:
y = double<br>

## Test
To unit test type:
```python
$ test/test.py
```