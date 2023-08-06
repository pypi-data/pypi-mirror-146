# wowa
This package calculates weighted OWA functions and extending bivariate means" Functions are:
- py_WAM: WOWATree callback function if sorting is needed in general 
- py_OWA: WOWATree callback function if no sorting is needed when used in the tree
- WOWATree: symmetric base aggregator 
- WAn: processes the tree
- weightedOWAQuantifierBuild: calculates spline knots and coefficients for later use in weightedOWAQuantifier
- weightedOWAQuantifier: Calculates the value of the WOWA, with quantifier function obtained in weightedOWAQuantifierBuild
- ImplicitWOWA: Calculates implicit Weighted OWA function
- WAM: weighted arithmetic mean function
- OWA: ordered weighted averaging function


## Documentation
[User Manual](http://gbfiles.epizy.com/wowa-theory.pdf)

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
cb: Nallback function. Either pre-defined py_OWA() or py_WAM() or user defined of type float(ch*)(int, float[], float[], int)<br>
L: Number of binary tree levels. Run time = O[(n-1)L]  
#### Output parameters:
y = weightedf, double<br>

## Usage of WAn( x, w, L, F)
```python
from wowa import WAn
```
### Parameters
#### Input parameters:
x[]: NumPy array of inputs, size n, float<br> 
w[]: NumPy array of weights for OWA, size n, float<br>
L: Number of binary tree levels<br>
F: User defined callback function of type float(*F)( float, float)<br>
#### Output parameters:
y = result of tree processing, double<br>

## Usage of weightedOWAQuantifierBuild( p, w, temp, T)
```python
from wowa import weightedOWAQuantifierBuild
```
### Parameters
#### Input parameters:
p[]: NumPy array of weights of inputs x[], size n, float<br> 
w[]: NumPy array of weights for OWA, size n, float<br>
temp[]: working memory, keeps the spline knots and coefficients for later use in weightedOWAQuantifier. Should be at least 12(n+1) in length and the memory should be allocated by the calling program<br>
T:  = the number of knots in the monotone spline<br>
#### Output parameters:
no output<br>


## Usage of weightedOWAQuantifier( x[], p, w, temp, T);
```python
from wowa import weightedOWAQuantifier
```
Calculates the value of the WOWA, with quantifier function obtained in weightedOWAQuantifierBuild
### Parameters
x[]: NumPy array of inputs, size n, float<br> 
p[]: NumPy array of weights of inputs x[], size n, float<br> 
w[]: NumPy array of weights for OWA, size n, float<br>
temp[]: working memory, keeps the spline knots and coefficients for later use in weightedOWAQuantifier. Should be at least 12(n+1) in length and the memory should be allocated by the calling program<br>
T:  = the number of knots in the monotone spline<br>
#### Input parameters:
#### Output parameters:
y = double<br>


## Usage of ImplicitWOWA x, p, w)
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
y = float<br>


## Usage of WAM( n, x, w)
```python
from wowa import WAM
```
Weighted arithmetic mean function
### Parameters
#### Input parameters:
n: size of arrays<br>
x[]: NumPy array of size n, float<br>
w[]: NumPy array of size n, float<br>
#### Output parameters:
y: aggregated sum, float 


## Usage of OWA( n, x, w)
```python
from wowa import OWA
```
Ordered weighted averaging function
### Parameters
#### Input parameters:
n: size of arrays<br>
x[]: NumPy array of size n, float<br>
w[]: NumPy array of size n, float<br>
#### Output parameters:
y: aggregated sum, float


## Test
To unit test type:
```python
$ test/test.py
```