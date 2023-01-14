"""SimplexSolve produces solution step matrices for Simplex Calculator
and generates/destroys corresponding labels.
"""

from copy import deepcopy
from fractions import Fraction
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

from classes import SLabelSolve


class SimplexSolve:
    """Generates and displays all solution steps.
    """
    def __init__(self, window: QWidget, layout: QGridLayout, simplex_setup, soln_step_label: QLabel, is_maximize: bool):
        """
        Parameters
        ---
        window: PyQt QWidget
        layout: PyQt QGridLayout
            soln_table_layout where labels are added.
        simplex_setup: SimplexSetup
        is_maximize: bool
            Determines whether problem is maximization or minimization and dictates certain solution steps and labels.
            Set with maximize/minimize button on setup screen.
        """
        self.window = window
        self.layout = layout
        self.simplex_setup = simplex_setup
        self.soln_step_label = soln_step_label
        self.is_maximize = is_maximize
        self.soln_index = 0
        self.soln_matrices = []
        self.header_labels = []
        # Label matrix indices will correspond to solution steps in soln_matrices
        self.label_matrix = []
        self.create_matrices()
        self.solve()
        self.update_labels()

    def solve(self) -> None:
        """Applies the simplex method.
        """
        def is_negative(matrix_row) -> bool:
            """Tests weather there is a negative number in a list of floats/ints.
            Stopping condition for simplex method.
            """
            for val in matrix_row:
                if val < 0:
                    return True
            return False

        # Current matrix is the most recent solution matrix (last step completed).
        matrix = deepcopy(self.soln_matrices[-1])

        # Continue until the bottom row is all positive.
        while is_negative(matrix[-1]):
            pivot_row, pivot_col, pivot = self.find_pivot(matrix)
            # Make pivot value 1 by dividing the pivot row by the pivot value.
            matrix[pivot_row] = [x/pivot for x in matrix[pivot_row]]

            # TODO: Rephrase these comments to make more clear.
            # Clear the pivot column, leaving only the pivot (now 1) and making the rest zeros:
            # Loop through each row -- excluding pivot row -- and add each component in the row by the
            # corresponding component of the pivot row multiplied by the value of the row's component
            # in the pivot column and flip sign of result.
            for row_vector in matrix[:pivot_row] + matrix[pivot_row + 1:]:
                val = row_vector[pivot_col]
                for i in range(len(row_vector)):
                    row_vector[i] += (-1)*val*matrix[pivot_row][i]
            # Save completed step.
            self.soln_matrices.append(matrix)
            # Get copy of completed step.
            matrix = deepcopy(self.soln_matrices[-1])

            # print(str(Fraction(pivot).limit_denominator()))
            # [print([str(Fraction(x).limit_denominator()) for x in row]) for row in matrix]

    def find_pivot(self, matrix: list) -> tuple:
        """Find the current pivot and return its matrix indices and value.

        Parameters
        ---
        matrix: list
            The current matrix.

        Returns
        ---
        tuple: (pivot_row, pivot_col, pivot_val)
            A tuple of 3 values.
            The first two are integers corresponding to the privot row index and pivot column index, respectively.
            The last is the pivot value.
        """
        # Get pivot column index which corresponds to the smallest value of the bottom row.
        pivot_col = matrix[-1].index(min(matrix[-1]))
        # Divide each component of the last column with its row's pivot_col component. Exclude bottom row.
        # A None will be placed in the list for negatives or zeros in pivot column to be discounted in next step.
        divided_col = [x[-1] / x[pivot_col] if x[pivot_col] > 0 else None for x in matrix[:-1]]
        # Get the index of the smallest value -- while discounting any Nones in the list.)
        pivot_row = divided_col.index(min([x for x in divided_col if x is not None]))
        return (pivot_row, pivot_col, matrix[pivot_row][pivot_col])

    def update_labels(self) -> None:
        """Update all labels in solution table to display current solution step.

        Update the solution step label which displays the current soltion step number out of
        the total steps, e.g. 1/3, 2/3 etc.
        """
        for row, matrix_row in enumerate(self.label_matrix):
            for col, label in enumerate(matrix_row):
                val = self.soln_matrices[self.soln_index][row][col]
                if float(val).is_integer():
                    label.setText(str(int(val)))
                # If value is a float, display as a simplified fraction.
                # https://stackoverflow.com/a/23344270
                else:
                    fraction = Fraction(val).limit_denominator()
                    label.setText(str(fraction))
        
        # Update solution step number.
        self.soln_step_label.setText(f"{self.soln_index + 1} / {len(self.soln_matrices)}")

    def next_step(self) -> None:
        """Increments index of soln_matrices by 1 and updates labels.

        Connected to next button on solution screen.
        """
        # Do not increment above the number of solution steps.
        if self.soln_index + 1 < len(self.soln_matrices):
            self.soln_index += 1
            self.update_labels()

    def prev_step(self) -> None:
        """Decrements index of soln_matrices by 1 and updates labels.

        Connected to previous button on solution screen.
        """
        # Do not decrement below zero.
        if self.soln_index > 0:
            self.soln_index -= 1
            self.update_labels()

    def first_step(self) -> None:
        """Skips to initial table.
        """
        self.soln_index = 0
        self.update_labels()

    def last_step(self) -> None:
        """Skips to final iteration table.
        """
        self.soln_index = len(self.soln_matrices) - 1
        self.update_labels()

    def create_matrices(self) -> None:
        """Turns a matrix of values from initial input objective function and constraint fields into the initial
        matrix used for applying simplex method and creates a corresponding matrix of label widgets as well as
        as labels for header names to be displayed on solution screen.

        Example
        ---
        An input of 2 constraints and 2 variables:\n
        Z  = 12X1 + 16X2\n
        C1:  1X1 +  2X2\n
        C2:  1X1 +  1X2\n
        Will result in the following matrix:\n
        [[1, 2, 40],\n
         [1, 1, 30],\n
         [12, 16, 0]]\n
        And will be turned into:\n
        [[1, 2, 1, 0, 0, 40],\n
         [1, 1, 0, 1, 0, 30],\n
         [-12, -16, 0, 0, 1, 0]]
        """
        # Get matrix of setup value fields.
        val_matrix = self.simplex_setup.get_fields(not self.is_maximize)
        # Create initial solution matrix.
        soln_matrix = []
        for row, matrix_row in enumerate(val_matrix):
            soln_matrix.append([])
            for col, val in enumerate(matrix_row):
                # If the float has trailing zeros after decimal, int cast it.
                val = int(val) if val.is_integer() else val
                # Flip signs of objective function values.
                val = val * -1 if row + 1 == len(val_matrix) else val
                soln_matrix[row].append(val)
            # Insert slack values before constraint inequality value.
            for i in range(len(val_matrix)):
                val = 1 if i == row else 0
                soln_matrix[row].insert(-1, val)
        self.soln_matrices.append(soln_matrix)

        # Create header name labels on first row.
        # Get a list of the objective terms, one column of constraint terms, and the objective function name.
        if self.is_maximize:
            widget_list = (self.simplex_setup.SLEVars + self.simplex_setup.SLEVars[0].constraint_col +
                [self.simplex_setup.SLEIneqs[0]])
        # If minimization is selected, add constraints to the list before variables.
        else:
            widget_list = (self.simplex_setup.SLEVars[0].constraint_col + self.simplex_setup.SLEVars +
                [self.simplex_setup.SLEIneqs[0]])
        # Create header lables from widget_list, e.g. X1, X2, S1, S2, Z.
        for col, widget in enumerate(widget_list):
            # Give each label in the header row a bottom border to create a line.
            label = SLabelSolve(self.window, widget.get_name(), ["bottom"])
            self.layout.addWidget(label, 0, col)
            self.header_labels.append(label)
        # Add a blank label with borders to complete lines in table.
        label = SLabelSolve(self.window, "", ["bottom", "left"])
        self.layout.addWidget(label, 0, col + 1)
        self.header_labels.append(label)

        # Create label matrix from solution matrix -- labels of constraint and objective function values.
        for row, matrix_row in enumerate(soln_matrix):
            self.label_matrix.append([])
            for col, val in enumerate(matrix_row):
                # Borders create vertical or horizontal lines where appropriate in the solution "table".
                borders = []
                # Last column gets a left border.
                if col + 1 == len(matrix_row):
                    borders.append("left")
                # Last row gets a top border.
                if row + 1 == len(soln_matrix):
                    borders.append("top")
                label = SLabelSolve(self.window, str(val), borders)
                # Add 1 to row to account for header labels.
                self.layout.addWidget(label, row + 1, col)
                self.label_matrix[row].append(label)

    def delete(self) -> None:
        """Removes all labels from the soltion table's layout.
        """
        # Delete header labels.
        for i in range(len(self.header_labels))[::-1]:
            deleted_widget = self.header_labels.pop(i)
            self.layout.removeWidget(deleted_widget)
            deleted_widget.deleteLater()
            del deleted_widget
        # Delete solution table labels.
        for matrix_row in self.label_matrix:
            for i in range(len(matrix_row))[::-1]:
                deleted_widget = matrix_row.pop(i)
                self.layout.removeWidget(deleted_widget)
                deleted_widget.deleteLater()
                del deleted_widget
        del self


if __name__ == "__main__":
    from simplex import SimplexCalculator
    simplex_calculator = SimplexCalculator()
