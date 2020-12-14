# Irreducibility Criteria Checker
This repository contains Python scripts that can be used to check various Polynomial irreducibility criteria. Main purpose is to find, understand and possibly automate as many criteria as possible.

## Eisenstein irreducibility criterion
https://en.wikipedia.org/wiki/Eisenstein%27s_criterion

## Cohn's irreducibility criterion
https://en.wikipedia.org/wiki/Cohn%27s_irreducibility_criterion

## Dumas' criterion for Newton polygons
See section Dumas's criterion in book Polynomials by Prasolov. 

## Checking irreducibility in finite field Fp
Algorithmic approach is used to decompose the polynomial into irreducible factors in finite fields Fp for small primes p. If the polynomial is irreducible in any of them, or if degrees of irreducible factors are not compatible, irreducibility over integers is implied.

## Murty's irreducibility criterion
See Theorem 1 in http://cms.dm.uba.ar/academico/materias/2docuat2011/teoria_de_numeros/Irreducible.pdf.

## Osada's irreducibility criterion
See Theorem 2.2.7 ([Os1]) in book Polynomials by Prasolov. 

## Perron's irreducibility criterion
https://en.wikipedia.org/wiki/Perron%27s_irreducibility_criterion

## Polya's irreducibility criterion
See Theorem 2.2.8 (Polya) in book Polynomials by Prasolov. 

## Schur's irreducibility criterion
See Schur's theorem for example in http://www.math.uconn.edu/~kconrad/blurbs/gradnumthy/schurtheorem.pdf.

## Brauer's irreducibility criterion
See Theorem 2.2.6 ([Br]) in book Polynomials by Prasolov. 

## Bonciocat's irreducibility criterion
See https://arxiv.org/pdf/1304.0874.pdf advanced use of newton polygons.

# Dependencies

Install required Python dependencies using:

`
python -m pip install -r requirements.txt
`

# Basic usage

Run test suite:

`
python -m unittest discover"
`

To run specific criterion check, try for example:

 `
python criteria/eisenstein.py "x^3-2*x^2+2*x+2"
`

To run all currently supported criteria use:


`
python check_all.py "P(x)"
`

where P(x) is some univariate polynomial from Z[x], e.g.
 
 `
python check_all.py "x^3-24*x^2-240*x-728"
`

This will also performs various substituions (e.g. shift f(x+c) or reciprocal polynomials.).




