# Simplex Calculator
# Alexander Ralston
# Created 11//2022
# Last updated 01/14/2023
#
# Simplex Method Calculator for educational purposes.
# George Dantzig's simplex linear programming algorithm for solving optimization problems.
#
# TODO: Confirm minimize is functioning as intended.
#       Resolve error when objective function has a value, but corresponding contraint column has 0s.
#       Redo setup screen buttons with icons.
#       Add header to screens which displays name and preserves settings/back buttons?
#       More detailed README.md with screenshots and examples
#       Replace icons.
#       Settings:
#           Add option to display floats instead of fractions to a given amount of decimal points
#           Link to github
#           Option to display solution steps on a single page
#           Donate button?

from simplex import SimplexCalculator

simplex_calculator = SimplexCalculator()
