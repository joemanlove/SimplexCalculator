"""SimplexSetup creates (and destroys) all input fields for objective function and constraints
depending on constraint and variable numbers set by user.
"""

from random import randint, choice

from PyQt5.QtWidgets import QWidget, QLineEdit, QGridLayout

from classes import SLEVar, SLECon, SLEIneq


class SimplexSetup:
    """Handles all objective funcion and constraint entry fields, dynamically updating from initial setup fields.
    """
    def __init__(self, window: QWidget, layout: QGridLayout, variables_edit: QLineEdit, constraints_edit: QLineEdit):
        """
        Parameters
        ---
        window: PyQt QWidget
        layout: PyQt QGridLayout
            The layout of layouts where the SLECon/SLEVar and SLEIneq objects are placed.
        variables_edit: PyQt QLineEdit
            The "Set Variables" edit field object.
        constraints_edit: PyQt QLineEdit
            The "Set Constraints" edit field object.
        """
        self.window = window
        self.cons_layout = layout.children()[0]
        self.ineq_layout = layout.children()[1]
        self.variables_edit = variables_edit
        self.constraints_edit = constraints_edit
        self.SLEVars = []
        self.SLEIneqs = []
        # Add first inequality and edit field for objective function.
        self.SLEIneqs.append(SLEIneq(self.window, self.ineq_layout, 0, 0))
        self.update()

    def update(self) -> None:
        """Called when variables or constraints edit field is updated, or when increase/decrease buttons are pressed.

        Add/remove SLECon objects to/from the layout as well as a SLEIneq inequality object at the end of row.

        Add/remove SLEVar object from SLEVars list, creating/destroying its associated SLECon objects, and
        adding/removing to/from constraints layout.
        """
        # Get the current number of constraints.
        crnt_con_num = 0 if len(self.SLEVars) == 0 else len(self.SLEVars[0].constraint_col)
        # Get the number of constraints from the QLineEdit field.
        edit_con_num = int(self.constraints_edit.text())
        # Get the current number of variables.
        crnt_var_num = len(self.SLEVars)
        # Get the number of variables from the QLineEdit field.
        edit_var_num = int(self.variables_edit.text())

        # Creating constraint/inequality widgets.
        if edit_con_num > crnt_con_num:
            for row in range(crnt_con_num, edit_con_num):
                # Add inequality object at end of row -- Add 1 to row to account for objective function row.
                self.SLEIneqs.append(SLEIneq(self.window, self.ineq_layout, row + 1, 0))
                # Add a constraint object for each variable.
                for col, sle_var in enumerate(self.SLEVars):
                    new_con = SLECon(self.window, self.cons_layout, row + 1, col)
                    new_con.update_var_label(sle_var.name_field.text())
                    sle_var.constraint_col.append(new_con)
            self.set_tab_order()

        # Removing constraint/inequality widgets.
        elif edit_con_num < crnt_con_num:
            # Reverse range to avoid index out of range errors when removing items.
            for i in range(edit_con_num, crnt_con_num)[::-1]:
                # Do not delete first element as it belongs to objective function.
                self.SLEIneqs.pop(i + 1).delete()
                # Remove all SLECon objects in row.
                for sle_var in self.SLEVars:
                    sle_var.constraint_col.pop(i).delete()

        # Adding variable and associated constraint widgets.
        if edit_var_num > crnt_var_num:
            for col in range(crnt_var_num, edit_var_num):
                # Create constraints -- SLEVar object handles all constraint's in its column for variable name association.
                constraint_col = []
                for row in range(edit_con_num):
                    # Add 1 to row to account for objective function row.
                    constraint_col.append(SLECon(self.window, self.cons_layout, row + 1, col))
                self.SLEVars.append(SLEVar(self.window, self.cons_layout, 0, col, constraint_col))
            self.set_tab_order()

        # Removing variable and associated contraint widgets.
        elif edit_var_num < crnt_var_num:
            for i in range(edit_var_num, crnt_var_num)[::-1]:
                deleted_var = self.SLEVars.pop(i)
                for sle_con in deleted_var.constraint_col:
                    sle_con.delete()
                deleted_var.delete()

    def set_tab_order(self) -> None:
        """Set the tab order of all variable name and contratint edit fields:
        left to right, top to bottom.

        Must be called every time variables or constraints are increased as default tab
        order is set to order in which widgets are added to the main PyQt QWidget window.
        """
        # To correctly set tab order, widgets must be set in the same order as the intended tab order.

        # Get a matrix of the objects themselves.
        matrix = self.get_fields(False, False)
        # Set order of objective function first as it is currently the last row of the matrix.
        for col, widget in enumerate(matrix[-1]):
            # When not on final column, connect widget to its name_field and name_field to the widget in next column.
            if col + 1 < len(matrix[-1]):
                self.window.setTabOrder(widget, widget.name_field)
                self.window.setTabOrder(widget.name_field, matrix[-1][col + 1])
            # When on final column, connect objective inequality field to first field of the first constraint.
            else:
                self.window.setTabOrder(widget, matrix[0][0])

        # Set order of all constraint and inequality fields.
        for row, widget_row in enumerate(matrix[:-1]):
            for col, widget in enumerate(widget_row):
                # When not on final column, connect to item in next column.
                if col + 1 < len(widget_row):
                    self.window.setTabOrder(widget, widget_row[col + 1])
                # When on final column but not on bottom row, connect to first item in next row.
                elif row + 1 < len(matrix[:-1]):
                    self.window.setTabOrder(widget, matrix[row + 1][0])

    def get_fields(self, transpose: bool = False, is_floats: bool = True) -> list:
        """Gets the values of the constraint edit fields and objective function and
        returns them as a matrix (two dimensional list).
        Components are defaulted to 0 if fields are left blank.

        Used to generate solution and to set correct tabbing order.

        Parameters
        ---
        transpose: bool, optional
            Defaulted False. Set to True if the matrix's transpose is desired.
        is_floats: bool, optional
            Defaulted True. Set to False if a matrix of widget objects is desired, otherwise the matrix
            will contain the float casted field values.

        Returns
        ---
        list
            List of lists of floats or widgets from setup edit fields.
        """
        def get_component(widget):
            """Returns either a float of the value field or the widget itself depending on is_floats argument.

            If there is no entry, default to 0.
            """
            # if is_floats:
            #     if widget.text():
            #         component = float(widget.text())
            #     else:
            #         component = 0.0
            #         widget.setText("0")
            # else:
            #     component = widget
            # return component
            return (float(widget.text()) if widget.text() else 0.0) if is_floats else widget

        # It is more convenient to construct the transpose first with current structure.
        matrix = []
        # Add all constraint fields.
        for i, var in enumerate(self.SLEVars):
            matrix.append([])
            for widget in var.constraint_col:
                matrix[i].append(get_component(widget))

        # Add inequality column as bottom row.
        matrix.append([])
        for widget in self.SLEIneqs[1:]:
            matrix[-1].append(get_component(widget))

        # Add objective function as far right column.
        for i, widget in enumerate(self.SLEVars):
            matrix[i].append(get_component(widget))

        # Value of objective inequality field should always be 0 when not the object itself as field is for naming purposes.
        component = 0.0 if is_floats else self.SLEIneqs[0]
        matrix[-1].append(component)

        # Since matrix is currenlty the transpose, transpose it to get original matrix.
        if not transpose:
            # https://stackoverflow.com/a/4937526
            matrix = list(map(list, zip(*matrix)))

        return matrix

    def reset_fields(self) -> None:
        """Clears all initial setup value fields.
        Called when reset button is pressed on initial setup screen.
        """
        for var in self.SLEVars:
            var.setText("")
            var.name_field.setText("")
            var.set_con_text()
            for con in var.constraint_col:
                con.setText("")
        for ineq in self.SLEIneqs[1:]:
            ineq.setText("")
        self.SLEIneqs[0].setText("Z")

    def randomize_fields(self) -> None:
        """Randomizes all initial setup value fields. Random values are integers based on specified ranges.

        Ranges are weighted depending on field type where objective function and constraint values are more likely
        to have a value of 1 to 10, and constraint inequality values are more likely to have a value of 10-60.
        """
        range_one = range(1, 11)
        range_two = range(10, 61)
        def random_field_val(perc: int, range_one: range, range_two: range) -> str:
            """Returns a randomly generated integer string from two weighted ranges.
            https://stackoverflow.com/a/64573263

            Parameters
            ---
            perc: int
                The percentage chance that the first range will be chosen.
            range_one: range
                A range of values
            range_two: range
                The second range of values to be chosen

            Returns
            ---
            str
                A string casted integer value.
            """
            p = randint(1, 100)
            return str(choice(range_one)) if p <= perc else str(choice(range_two))

        for var in self.SLEVars:
            # 25% chance of 1 - 10 for objective function, 75% chance of 10+
            var.setText(random_field_val(25, range_one, range_two))
            for con in var.constraint_col:
                # 75% chance of 1 - 10 for constraint coefficients.
                con.setText(random_field_val(75, range_one, range_two))
        for ineq in self.SLEIneqs[1:]:
            # 25% chance of 1 - 10 for constraint value, 75% chance of 10+
            ineq.setText(random_field_val(25, range_one, range_two))


if __name__ == "__main__":
    from simplex import SimplexCalculator
    simplex_calculator = SimplexCalculator()
