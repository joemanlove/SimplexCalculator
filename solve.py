"""SimplexSolve produces solution step matrices for Simplex Calculator
and generates/destroys corresponding labels.
"""

from PyQt5.QtWidgets import QWidget, QLineEdit, QGridLayout
from copy import deepcopy
from classes import QLabelSimplex

class SimplexSolve:
    """Generates and displays all solution steps.
    """
    def __init__(self, window: QWidget, layout: QGridLayout, simplex_setup, is_maximize: bool):
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
        self.is_maximize = is_maximize
        self.soln_matrices = []
        self.header_labels = []
        # Label matrix indices will correspond to solution steps in self.matrices
        self.label_matrix = []
        self.create_matrices()
        # self.solve()
        # for i, matrix in enumerate(self.soln_matrices):
        #     print(f"Step: {i + 1}")
        #     for row in matrix:
        #         print(row)

    def solve(self) -> None:
        """Applies the simplex method.
        """
        def is_negative(matrix_row) -> bool:
            for val in matrix_row:
                if val < 0:
                    return True
            return False
        # Current matrix is the most recent solution matrix (last step completed).
        matrix = deepcopy(self.soln_matrices[-1])
        while is_negative(matrix[-1]):
            pivot_row, pivot_col, pivot = self.find_pivot(matrix)
            matrix[pivot_row] = [x/pivot for x in matrix[pivot_row]]
            for row_vector in matrix[:pivot_row]+matrix[pivot_row+1:]:
                val = row_vector[pivot_col]
                for i in range(len(row_vector)):
                    row_vector[i] += (-1)*matrix[pivot_row][i]*val
            self.soln_matrices.append(matrix)
            matrix = deepcopy(self.soln_matrices[-1])
            # [print(x) for x in matrix]

    def find_pivot(self, matrix: list) -> tuple:
        """Find the current pivot and return its matrix index.

        Parameters
        ---
        matrix: list
            The current matrix.

        Returns
        ---
        tuple
            A tuple of 3 values.
            The first two are integers corresponding to the privot row index and pivot column index, respectively.
            The last is the pivot value.
        """
        # Get pivot column index which corresponds to the smallest value of the bottom row.
        pivot_col = matrix[-1].index(min(matrix[-1]))
        # Divide each component of the last column with its row's pivot_col component. Exclude bottom row.
        reduced_col = [x[-1] / x[pivot_col] for x in matrix[:-1]]
        # Get the index of the smallest value
        pivot_row = reduced_col.index(min(reduced_col))
        return (pivot_row, pivot_col, matrix[pivot_row][pivot_col])

    def next_step(self) -> None:
        """
        Connected to next button on solution screen.
        """
        pass

    def prev_step(self) -> None:
        """
        Connected to previous button on solution screen.
        """
        pass

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
        # Create initial solution matrix
        soln_matrix = []
        for row, matrix_row in enumerate(val_matrix):
            soln_matrix.append([])
            for col, val in enumerate(matrix_row):
                # If the float has trailing zeros after decimal, int cast it
                val = int(val) if val.is_integer() else val
                # Flip signs of objective function values
                val = val * -1 if row == len(val_matrix) - 1 else val
                soln_matrix[row].append(val)
            # Insert slack values before constraint inequality value
            for i in range(len(val_matrix)):
                val = 1 if i == row else 0
                soln_matrix[row].insert(-1, val)
        self.soln_matrices.append(soln_matrix)

        # Create header name labels on first row (e.g. X1, X2, S1, S2, Z)
        # Get a list of the onjective terms, one column of constraint terms, and the objective function name
        widget_list = self.simplex_setup.QLEVars+self.simplex_setup.QLEVars[0].constraint_col+[self.simplex_setup.QLEInqs[0]]
        for col, widget in enumerate(widget_list):
            # Give each label in the header row a bottom border to create a line
            label = QLabelSimplex(self.window, self.layout, widget.get_name(), 0, col, ["bottom"])
            self.header_labels.append(label)
        # Add a blank label with borders to complete lines in table
        label = QLabelSimplex(self.window, self.layout, "", 0, col + 1, ["bottom", "left"])
        self.header_labels.append(label)

        # Create label matrix from solution matrix -- labels of constraint and objective function values
        for row, matrix_row in enumerate(soln_matrix):
            self.label_matrix.append([])
            for col, val in enumerate(matrix_row):
                # Borders create vertical or horizontal lines where appropriate in the solution "table"
                borders = []
                # Last column gets a left border
                if col == len(matrix_row) - 1:
                    borders.append("left")
                # Last row gets a top border
                if row == len(soln_matrix) - 1:
                    borders.append("top")
                # Add 1 to row to account for header labels
                label = QLabelSimplex(self.window, self.layout, str(val), row + 1, col, borders)
                self.label_matrix[row].append(label)

    def delete(self) -> None:
        """Removes all labels from the soltion table's layout.
        """
        # Delete header labels
        for i in range(len(self.header_labels))[::-1]:
            deleted_widget = self.header_labels.pop(i)
            self.layout.removeWidget(deleted_widget)
            deleted_widget.deleteLater()
            del deleted_widget
        # Delete solution table labels
        for matrix_row in self.label_matrix:
            for i in range(len(matrix_row))[::-1]:
                deleted_widget = matrix_row.pop(i)
                self.layout.removeWidget(deleted_widget)
                deleted_widget.deleteLater()
                del deleted_widget
        del self


if __name__ == "__main__":
    from simplex import SimplexCalculator
    simplex = SimplexCalculator()
