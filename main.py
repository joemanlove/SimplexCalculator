# Simplex Calculator
# Alexander Ralston
# Created 11//2022
# Last updated 01/14/2023
#
# Simplex Method Calculator for educational purposes.
# George Dantzig's simplex linear programming algorithm for solving optimization problems.
#
# TODO:
# More detailed README.md with screenshots and examples
## Simplex Funcionality
# Confirm minimize is functioning as intended.
# Resolve error when objective function has a value, but corresponding contraint column has 0s.
# Allow negative numbers as input for constraint fields (and objetive function?)
# Allow ability to switch inequalites of contraints.
## UI
# Make the rows of the solution screen tables selectable to highlight the row.
# When screen changing, new screen displays briefly in place before entering screen -- sometimes.
# Redo setup screen buttons with icons.
# Add header to screens which displays name and preserves settings/back buttons?
# Allow user to name contraint rows.
# Replace icons with own alternatives.
# Add Dark mode icon and font size icon.
# Settings:
#   Add option to display floats instead of fractions to a given amount of decimal points.
#   Option to display solution steps on a single page?
#   Donate button?

from simplex import SimplexCalculator

simplex_calculator = SimplexCalculator()
