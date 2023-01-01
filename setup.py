"""SimplexSetup creates (and destroys) all input fields for objective function and constraints
depending on constraint and variable numbers set by user.
"""


from PyQt5.QtWidgets import QWidget, QLineEdit, QGridLayout
from classes import QLEVar, QLECon, QLEInq
from random import randint, choice

class SimplexSetup:
    """Handles all objective funcion and constraint entry fields, dynamically updating from initial setup fields.
    """
    def __init__(self, window: QWidget, layout: QGridLayout, variables_edit: QLineEdit, constraints_edit: QLineEdit):
        """
        Parameters
        ---
        window: PyQt QWidget
        layout: PyQt QGridLayout
            The layout of layouts where the QLECon/QLEVar and QLEInq objects are placed.
        variables_edit: PyQt QLineEdit
            The "Set Variables" edit field object
        constraints_edit: PyQt QLineEdit
            The "Set Constraints" edit field object
        """
        self.window = window
        self.cons_layout = layout.children()[0]
        self.ineq_layout = layout.children()[1]
        self.variables_edit = variables_edit
        self.constraints_edit = constraints_edit
        self.QLEVars = []
        self.QLEInqs = []
        # Add first inequality and edit field for objective function
        new_ineq = QLEInq(self.window, self.ineq_layout, 0, 0)
        self.QLEInqs.append(new_ineq)
        self.update()

    def update(self):
        """Called when variables or constraints edit field is updated, or when increase/decrease buttons are pressed.

        Calls both update_vars() update_cons().
        """
        # They currently must be called in this order to properly create QLEInq inequality objects upon initialization.
        self.update_cons()
        self.update_vars()

        # matrix = self.get_fields()
        # for row in matrix:
        #     print(row)

    def update_vars(self):
        """Add/remove QLEVar object from QLEVars list, creating/destroying its associated QLECon objects, and
        adding/removing to/from constraints layout.
        """
        # Get the current number of variables
        crnt_var_num = len(self.QLEVars)
        # Get the number of variables from the QLE field
        edit_var_num = int(self.variables_edit.text())
        # Get the current number of contraints from the QLE field
        crnt_con_num = int(self.constraints_edit.text())

        # Removing variable and associated contraint widgets
        if edit_var_num < crnt_var_num:
            # Range reversal is nesesarry to avoid index out of range errors when removing items
            for i in range(edit_var_num, crnt_var_num)[::-1]:
                deleted_var = self.QLEVars.pop(i)
                for qle_con in deleted_var.constraint_col:
                    qle_con.delete()
                deleted_var.delete()

        # Adding variable and associated constraint widgets
        elif edit_var_num > crnt_var_num:
            for col in range(crnt_var_num, edit_var_num):
                # Create constraints -- QLEVar object handles all constraint's in its column for variable name association
                constraint_col = []
                for row in range(crnt_con_num):
                    # Add 1 to row to account for objective function row
                    new_con = QLECon(self.window, self.cons_layout, row + 1, col)
                    constraint_col.append(new_con)
                new_var = QLEVar(self.window, self.cons_layout, 0, col, constraint_col)
                self.QLEVars.append(new_var)
            self.set_tab_order()

    def update_cons(self):
        """Add/remove QLECon objects to/from the layout as well as a QLEInq inequality at the end of row.
        """
        # Get the current number of constraints
        crnt_con_num = 0 if len(self.QLEVars) == 0 else len(self.QLEVars[0].constraint_col)
        # Get the number of constraints from the QLE field
        edit_con_num = int(self.constraints_edit.text())

        # Removing constraint widgets
        if edit_con_num < crnt_con_num:
            # Range reversal is nesesarry to avoid index out of range errors when removing items
            for i in range(edit_con_num, crnt_con_num)[::-1]:
                deleted_ineq = self.QLEInqs.pop(i + 1)
                deleted_ineq.delete()
                # Remove all QLECon objects in row
                for qle_var in self.QLEVars:
                    deleted_con = qle_var.constraint_col.pop(i)
                    deleted_con.delete()

        # Creating constraint widgets
        elif edit_con_num > crnt_con_num:
            for row in range(crnt_con_num, edit_con_num):
                # Add inequality and edit field -- Add 1 to row to account for objective function row
                new_ineq = QLEInq(self.window, self.ineq_layout, row + 1, 0)
                self.QLEInqs.append(new_ineq)
                # Add a constraint object for each variable
                for col, qle_var in enumerate(self.QLEVars):
                    new_con = QLECon(self.window, self.cons_layout, row + 1, col)
                    new_con.update_var_label(qle_var.name_field.text())
                    qle_var.constraint_col.append(new_con)
            self.set_tab_order()

    def set_tab_order(self) -> None:
        """Set the tab order of all variable name and contratint edit fields:
        left to right, top to bottom.

        Must be called every time variables or constraints are increased as default tab
        order is set to order in which widgets are added to the main PyQt QWidget window.
        """
        # To correctly set tab order, widgets must be set in the same order as the intended tab order.
        # Get a matrix of the objects themselves
        matrix = self.get_fields(False, False)
        # Set order of objective function first as it is currently the last row of the matrix
        for col, widget in enumerate(matrix[-1]):
            # When not on final column, connect widget to its name_field and name_field to the widget in next column
            if col + 1 < len(matrix[-1]):
                self.window.setTabOrder(widget, widget.name_field)
                self.window.setTabOrder(widget.name_field, matrix[-1][col + 1])
            # When on final column, connect objective inequality field to first field of the first constraint
            else:
                self.window.setTabOrder(widget, matrix[0][0])

        # Set order of all constraint and inequality fields
        for row, widget_row in enumerate(matrix[:-1]):
            for col, widget in enumerate(widget_row):
                # When not on final column, connect to item in next column
                if col + 1 < len(widget_row):
                    self.window.setTabOrder(widget, widget_row[col + 1])
                # When on final column but not on bottom row, connect to first item in next row
                elif row + 1 < len(matrix[:-1]):
                    self.window.setTabOrder(widget, matrix[row + 1][0])

    def get_fields(self, transpose: bool = False, is_floats: bool = True) -> list:
        """Gets the values of the constraint edit fields and objective function and 
        returns them as a matrix (two dimensional list).
        Components are defaulted to 0 if fields are left blank.

        Used to generate solution and to set correct tabbing order.

        Parameters
        ---
        transpose: boolean, optional
            Defaulted False. Set to True if the matrix's transpose is desired.
        is_floats: boolean, optional
            Defaulted True. Set to False if a matrix of widget objects is desired, otherwise the matrix
            will contain the float casted field values.
        """
        def get_component(widget):
            """Returns either a float of the value field or the widget itself depending on is_floats argument.
            """
            return (float(widget.text()) if widget.text() else 0.0) if is_floats else widget

        # It is more convenient to construct the transpose first with current structure.
        matrix = []
        # Add all constraint fields
        for i, var in enumerate(self.QLEVars):
            matrix.append([])
            for widget in var.constraint_col:
                matrix[i].append(get_component(widget))

        # Add inequality column as bottom row
        matrix.append([])
        for widget in self.QLEInqs[1:]:
            matrix[-1].append(get_component(widget))

        # Add objective function as far right column
        for i, widget in enumerate(self.QLEVars):
            matrix[i].append(get_component(widget))

        # Value of objective inequality field should always be 0 when not the object itself as field is for naming purposes
        component = 0.0 if is_floats else self.QLEInqs[0]
        matrix[-1].append(component)

        if not transpose:
            matrix = [list(x) for x in zip(*matrix)]

        return matrix

    def reset_fields(self) -> None:
        """Clears all initial setup value fields.
        """
        for var in self.QLEVars:
            var.setText("")
            var.name_field.setText("")
            var.set_con_text()
            for con in var.constraint_col:
                con.setText("")
        for inq in self.QLEInqs[1:]:
            inq.setText("")

    def randomize_fields(self) -> None:
        """Randomizes all initial setup value fields. Random values are integers based on specified ranges.

        Ranges are weighted depending on field type where objective function and constraint values are more likely
        to have a value of 1 to 10, and constraint inequality values are more likely to have a value of 10-60.
        """
        range_one = range(1, 11)
        range_two = range(10, 61)
        def random_field_val(perc: int, range_one: range, range_two: range) -> str:
            """Returns a string casted integer value.

            Parameters
            ---
            perc: int
                The percentage chance that the first range will be chosen.
            range_one: range
                A range of values
            range_two: range
                The second range of values to be chosen
            """
            p = randint(1, 100)
            return str(choice(range_one)) if p <= perc else str(choice(range_two))

        for var in self.QLEVars:
            var.setText(random_field_val(75, range_one, range_two))
            for con in var.constraint_col:
                con.setText(random_field_val(75, range_one, range_two))
        for inq in self.QLEInqs[1:]:
            inq.setText(random_field_val(25, range_one, range_two))

