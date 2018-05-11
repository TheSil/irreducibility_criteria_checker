# Irreducibility Criteria Checker
This repository contains Python scripts that can be used to check various Polynomial irreducibility criteria. Main purpose is to find, understand and possibly automate as many criteria as possible.

#Currently supported Criteria:

Eisenstein irreducibility criterion

Cohn irreducibility criterion

Dumas' criterion for Newton polygons

Checking irreducibility in finite field Fp for small primes

Murty's irreducibility criterion

Osada's irreducibility criterion

Perron's irreducibility criterion

Polya's irreducibility criterion

Schur's irreducibility criterion

Brauer's irreducibility criterion

Bonciocat's irreducibility criterion

# Basic usage

To run all currently supported criteria use


`
check_all.py "P(x)"
`

where P(x) is some univariate polynomial from Z[x], e.g.
 
 `
check_all.py "x^3-24*x^2-240*x-728"
`

To run specific criterion check, try for example:

 `
check_eisenstein.py "x^3-2*x^2+2*x+2"
`
