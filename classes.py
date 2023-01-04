"""Customized PyQt widgets for Simplex Calculator.

QPBSimplex: QPushButon child
QLEVar: QLineEdit child
QLECon: QLineEdit child
QLEInq: QLineEdit child
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QGridLayout
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp


class QPBSimplex(QPushButton):
    """Child class of PyQt QPushButton object.
    """
    def __init__(self, window: QWidget, text: str, size: int):
        """Child class of PyQt QPushButton object.
        Creates a simple push button of a set square size with a given label.
        Used for increase/decrease buttons for variables/constraints.

        Parameters
        ---
        window: QWidget
            Main PyQt window.
        text: str
            Text to be displayed on button.
        size: int
            Square dimensions of the button.
        """
        QPushButton.__init__(self, window)
        self.setText(text)
        self.setMaximumWidth(size)
        self.setAutoRepeat(True)
        # Will delay button function in miliseconds when held down.
        self.setAutoRepeatDelay(500)


class QLabelSimplex(QLabel):
    """Child class of PyQt QLabel. Used for displaying components of solutions matrix table.
    """
    def __init__(self, window: QWidget, layout: QGridLayout, text: str, row_index: int, col_index: int, borders: list = []):
        """Child class of PyQt QLabel. Used for displaying components of solutions matrix table.

        Parameters
        ---
        window: PyQt QWidget
            The main window.
        layout: PyQt QGridLayout
            The layout where widgets are placed.
        text: str
            The text to be displayed on the label.
        row_num: int
            The row number for placement within the given layout.
        col_num: int
            The column number for placement within the given layout.
        borders: list
            A list of strings indicating what borders will be drawn. Used to create lines of table.
            Expected strings are "top", "bottom", "left", or "right".
        """
        QLabel.__init__(self, window)
        # Create border
        # Below string will be divided into substrings, if a direction within borders is present,
        # the substring is replaced with an empty string.
        style = "border-top-style:none; border-bottom-style:none; border-right-style:none; border-left-style:none;"
        style_list = style.split()
        for direction in borders:
            for i, sub_str in enumerate(style_list):
                if direction.lower() in sub_str:
                    style_list[i] = ""
                    break
        style = " ".join(style_list)
        self.setStyleSheet(style)
        self.setText(text)
        self.setAlignment(Qt.AlignCenter)
        layout.addWidget(self, row_index, col_index)


class QLESimplex(QLineEdit):
    """Child class of PyQt QLineEdit object and parent of QLEVar, QLECon, and QLEInq child classes.
    """
    def __init__(self, window: QWidget, layout: QGridLayout, row_index: int, col_index: int):
        """Child class of PyQt QLineEdit object and parent of QLEVar, QLECon, and QLEInq child classes.
        Used for inputting values into constraint and objective function edit fields during setup.

        Parameters
        ---
        window: PyQt QWidget
            The main window.
        layout: PyQt QGridLayout
            The layout where widgets are placed.
        row_num: int
            The row number for placement within the given layout.
        col_num: int
            The column number for placement within the given layout.
        """
        QLineEdit.__init__(self, window)
        self.setMaximumWidth(42)
        self.setAlignment(Qt.AlignCenter)
        # Limit field input to digits separated by a decimal and allows user to input an empty string to clear field.
        self.setValidator(QRegExpValidator(QRegExp('(^?[0-9]*\.?[0-9]+$|^$)')))

        self.layout = layout
        self.row_index = row_index
        self.col_index = col_index
        self.widgets = []

    def add(self) -> None:
        """Adds self and associated widgets to the initialized layout.
        """
        # Since each object contains multiple widgets (including itself),
        # place them in the appropriate column by multiplying the column index by the number of widgets.
        for i, widget in enumerate(self.widgets):
            self.layout.addWidget(widget, self.row_index, (self.col_index*len(self.widgets)) + i, Qt.AlignCenter)

    def delete(self) -> None:
        """Deletes self and associated widgets and removes them from the layout.
        """
        for i in range(len(self.widgets))[::-1]:
            deleted_widget = self.widgets.pop(i)
            self.layout.removeWidget(deleted_widget)
            deleted_widget.deleteLater()
            del deleted_widget

    def get_name(self) -> str:
        pass


class QLEVar(QLESimplex):
    """Child class of PyQt QLineEdit object. Component object for objective function.

    Since these are created with a loop, a class wrapper becomes necessary to prevent the
    connected function from being associated with the last object created within the loop,
    i.e. prevent cell variable from loop:
    https://pylint.pycqa.org/en/latest/user_guide/messages/warning/cell-var-from-loop.html
    """
    def __init__(self, window: QWidget, layout: QGridLayout, row_index: int, col_index: int, constraint_col: list):
        """Child class of PyQt QLineEdit object. Component object for objective function.
        Contains variable naming field, objective value field, and "+" label.

        Parameters
        ---
        window: PyQt QWidget
        layout: PyQt QGridLayout
        row_index: int
            The row index. Determines positioning within layout.
        col_index: int
            The object index within the QLE_vars list which also corresponds to the column of the layout.
            Used for default variable name and determining the label text when object is in the first column.
        constraint_col: list
            The list of associated constraint QLECon objects for variable name label updating.
            This is a column of constraint fields in the setup screen.
        """
        QLESimplex.__init__(self, window, layout, row_index, col_index)
        self.constraint_col = constraint_col

        self.name_field = QLineEdit(window)
        self.name_field.setMaxLength(3)
        self.name_field.setMaximumWidth(40)
        self.name_field.setAlignment(Qt.AlignCenter)

        label = QLabel(window)
        label.setIndent(1)
        label.setAlignment(Qt.AlignLeft)
        # Add extra padding for alignmet with "Constraint #" labels
        # label_style = "padding-right: 26px" if col_index == 0 else ""
        # label.setStyleSheet(label_style)
        # Extra spaces are added to align with "Constraint #"
        # label_text = "Objective: " if col_index == 0 else "+"
        # TODO: Default value should either reflect objective function name input or be more descriptive.
        label_text = "Z:" if col_index == 0 else "+"

        label.setText(label_text)

        # Add these in the order in which they appear in app.
        self.widgets.append(label)
        self.widgets.append(self)
        self.widgets.append(self.name_field)
        self.add()

        self.set_con_text()
        self.name_field.editingFinished.connect(self.set_con_text)

    def set_con_text(self) -> None:
        """Connected to QLineEdit simplex variable field when box is deselected or enter is pressed.

        Updates current name of all its associated constraints to reflect field.
        Defaulted to X₁, X₂, etc. when field is left blank.
        """
        # Subscripts for defaulted name label
        sub = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        # Prevent user from setting variable name to whitespace(s) with strip()
        current_text = self.name_field.text().strip()

        if current_text == "":
            current_text = f"X{self.col_index + 1}".translate(sub)
            self.name_field.setText(current_text)

        for qle in self.constraint_col:
            qle.update_var_label(current_text)

    def get_name(self) -> str:
        """
        Returns
        ---
        str
            The value of the name_field's edit field. Used for solution table labeling.
        """
        return self.name_field.text()


class QLECon(QLESimplex):
    """Child class of PyQt QLineEdit constraint object.
    """
    def __init__(self, window: QWidget, layout: QGridLayout, row_index: int, col_index: int):
        """Child class of PyQt QLineEdit constraint object.

        In addition to the edit field, contains the associated variable name label and "+" sign.

        Parameters
        ---
        window: PyQt QWidget
        layout: PyQt QGridLayout
        row_index: int
            1 should be added to this upon initialization to account for the objective function row.
        col_index: int
            The object column index. Determines the label text when object is in the first column and
            positioning within layout.
        """
        QLESimplex.__init__(self, window, layout, row_index, col_index)
        # Text displayed will be connected to QLEVar name_field.
        self.var_label = QLabel(window)
        self.var_label.setIndent(1)

        label = QLabel(window)
        label.setIndent(1)
        label.setAlignment(Qt.AlignLeft)
        # Add extra padding for alignmet with "Constraint 10" labels
        # label_style = "padding-right: 8px" if col_index == 0 and row_index < 10 else ""
        # label.setStyleSheet(label_style)
        # label_text = f"Constraint {row_index}: " if col_index == 0 else "+"
        sub = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        # Label will be "+" if not the first in a row, otherwise it will be constraint number label.
        label_text = f"C{row_index}:".translate(sub) if col_index == 0 else "+"
        label.setText(label_text)

        # Diagnositic -- Display indices in the edit fields.
        # self.setText(str(row_index)+str(col_index))

        # Add these in the order in which they should appear in app.
        self.widgets.append(label)
        self.widgets.append(self)
        self.widgets.append(self.var_label)
        self.add()

    def update_var_label(self, new_name: str) -> None:
        """Sets the variable name label to the given string. Called when associated QLEVar field is updated.

        Parameters
        ---
        new_name: str
        """
        self.var_label.setText(new_name)

    def get_name(self) -> str:
        """
        Returns
        ---
        str
            The slack name. Used for solution table labeling.
        """
        sub = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        return f"S{self.row_index}".translate(sub)


class QLEInq(QLESimplex):
    """Child class of PyQt QLineEdit. Displayed on far right column of constraint input fields and objective function.
    """
    def __init__(self, window: QWidget, layout: QGridLayout, row_index: int, col_index: int):
        """Contains inequality label as well as QLineEdit field widget. Displayed on far right column
        of constraint input fields and objective function.

        Parameters:
        ---
        window: PyQt QWidget
        layout: PyQt QGridLayout
        row_index: int
            1 should be added to this upon initialization to account for the objective function row when creating
            contraints. If 0, properties will change to allow the user to name the objective function.
        col_index: int
            The object column index. Determines the label text when object is in the first column.
        """
        QLESimplex.__init__(self, window, layout, row_index, col_index)
        # Inequality label text will ultimately be determined by Minimize/Maximize button.
        label_text = "≤"
        # Change properties for objective function.
        if row_index == 0:
            label_text = "="
            self.setValidator(None)
            self.setText("Z")
            self.setMaxLength(3)
            # Default objective function variable to "Z" if field is left blank.
            self.editingFinished.connect(lambda: self.setText("Z") if self.text().strip() == "" else self.text())

        self.label = QLabel(window)
        self.label.setAlignment(Qt.AlignLeft)
        self.label.setText(label_text)

        # Add these in the order in which they should appear in app.
        self.widgets.append(self.label)
        self.widgets.append(self)
        self.add()

    def get_name(self) -> str:
        """
        Returns
        ---
        str
            The value of the edit field. Used to get name of objective function for solution table labeling.
        """
        return self.text()


if __name__ == "__main__":
    from simplex import SimplexCalculator
    simplex = SimplexCalculator()
