"""Simplex Calculator

Made with PyQt5
"""

from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QSpacerItem, QSizePolicy,
                             QGridLayout, QScrollArea, QAbstractScrollArea, QFrame, QHBoxLayout)
from PyQt5.QtGui import QPalette, QColor, QGuiApplication, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp, QRect

from classes import QPBSimplex, QLabelSimplex
from setup import SimplexSetup
from styles import SIMPLEX_STYLE_LIGHT, SIMPLEX_STYLE_DARK


class SimplexCalculator:
    """Main class for Simplex Calculator.
    """
    # Dimensions and limit constants
    WINDOW_WIDTH = 480
    WINDOW_HEIGHT = 800
    WIDGET_WIDTH = 32

    START_VARIABLES = 3
    START_CONSTRAINTS = 3
    MIN_VARIABLES = 2
    MAX_VARIABLES = 20
    MIN_CONSTRAINTS = 1
    MAX_CONSTRAINTS = 20

    def __init__(self):
        """
        Main PyQt window and app, as well as buttons and layouts are created here.
        """
        # Create main Qt app and window
        self.app = QApplication([])
        self.app.setStyle("Fusion")
        self.window = QWidget()
        self.window.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.window.setMinimumSize(380, 480)
        self.window.setWindowTitle("Simplex Method")

        # Toggle Palette Button
        self.palette_mode = 1
        self.palette_button = QPushButton(self.window)
        # self.palette_button.setFixedWidth(300)
        self.palette_button.clicked.connect(self.toggle_palette)
        self.toggle_palette()

        # Setting Variables
        variables_label = QLabel(self.window)
        variables_label.setText("Set Variables")
        # Decrease Variables Button
        variables_decrease = QPBSimplex(self.window, "-", self.WIDGET_WIDTH)
        variables_decrease.clicked.connect(lambda: (self.QLE_inc_dec(variables_edit, self.MIN_VARIABLES, self.MAX_VARIABLES, False),
                                                    self.simplex_setup.update()))
        # QLineEdit Widget -- Updates as increase/decrease are pressed and is editable.
        variables_edit = QLineEdit(self.window)
        # Limit field input to digits -- Allow empty strings to enable user to clear field.
        variables_edit.setValidator(QRegExpValidator(QRegExp('(^[0-9]+$|^$)')))
        variables_edit.setMaxLength(2)
        variables_edit.setText(str(self.START_VARIABLES))
        variables_edit.setMaximumWidth(self.WIDGET_WIDTH)
        variables_edit.setAlignment(Qt.AlignCenter)
        variables_edit.editingFinished.connect(lambda: (self.QLE_valid_range(variables_edit, self.MIN_VARIABLES, self.MAX_VARIABLES),
                                                        self.simplex_setup.update()))
        # Increase Variables Button
        variables_increase = QPBSimplex(self.window, "+", self.WIDGET_WIDTH)
        variables_increase.clicked.connect(lambda: (self.QLE_inc_dec(variables_edit, self.MIN_VARIABLES, self.MAX_VARIABLES),
                                                    self.simplex_setup.update()))

        # Setting Constraints
        constraints_label = QLabel(self.window)
        constraints_label.setText("Set Constraints")
        # Decrease Constraints Button
        constraints_decrease = QPBSimplex(self.window, "-", self.WIDGET_WIDTH)
        constraints_decrease.clicked.connect(lambda: (self.QLE_inc_dec(constraints_edit, self.MIN_CONSTRAINTS, self.MAX_CONSTRAINTS, False),
                                                      self.simplex_setup.update()))
        # QLineEdit Widget -- Updates as increase/decrease are pressed and is direclty editable
        constraints_edit = QLineEdit(self.window)
        constraints_edit.setValidator(QRegExpValidator(QRegExp('(^[0-9]+$|^$)')))
        constraints_edit.setMaxLength(2)
        constraints_edit.setText(str(self.START_CONSTRAINTS))
        constraints_edit.setMaximumWidth(self.WIDGET_WIDTH)
        constraints_edit.setAlignment(Qt.AlignCenter)
        constraints_edit.editingFinished.connect(lambda: (self.QLE_valid_range(constraints_edit, self.MIN_CONSTRAINTS, self.MAX_CONSTRAINTS),
                                                          self.simplex_setup.update()))
        # Increase Constraints Button
        constraints_increase = QPBSimplex(self.window, "+", self.WIDGET_WIDTH)
        constraints_increase.clicked.connect(lambda: (self.QLE_inc_dec(constraints_edit, self.MIN_CONSTRAINTS, self.MAX_CONSTRAINTS),
                                                      self.simplex_setup.update()))

        # Toggle Maximize/Minimize Button
        self.is_maximized = True
        self.max_min_button = QPushButton(self.window)
        self.max_min_button.setText("Maximize")
        # self.toggle_max_min()
        self.max_min_button.clicked.connect(self.toggle_max_min)

        # Randomize Button - Sets random values in all fields
        randomize__button = QPushButton(self.window)
        randomize__button.setText("Randomize")
        randomize__button.clicked.connect(self.randomize_fields)

        # Reset Button
        reset_button = QPushButton(self.window)
        reset_button.setText("Reset")
        reset_button.clicked.connect(self.reset_fields)

        # Calculate Button -- Generate SimplexSolve object and display solution screen
        calculate_button = QPushButton(self.window)
        calculate_button.setText("Calculate")
        calculate_button.clicked.connect(self.calculate)

        # Back button -- Go back to the previous screen
        # Duplicate buttons are necessary because the same widget cannot be in two different frames or layouts
        back_button = QPushButton(self.window)
        back_button.setText("Back")
        back_button.clicked.connect(self.go_back)
        back_button2 = QPushButton(self.window)
        back_button2.setText("Back")
        back_button2.clicked.connect(self.go_back)

        # Settings button -- Open Settings screen
        settings_button = QPushButton(self.window)
        settings_button.setText("Settings")
        settings_button.clicked.connect(self.open_settings)
        settings_button2 = QPushButton(self.window)
        settings_button2.setText("Settings")
        settings_button2.clicked.connect(self.open_settings)


        # Layouts and Widget Placement
        # Primary layout for main window -- All child layouts are placed here
        parent_layout = QHBoxLayout()
        # parent_layout.setSpacing(0)
        parent_layout.setContentsMargins(0, 12, 0, 12)
        # Parent layouts for setup buttons and setup fields layouts.
        setup_parent_layout = QGridLayout()
        soln_parent_layout = QGridLayout()
        # The initial set variables/constraints and maximize/minimize buttons abd associated widgets go here
        setup_buttons_layout = QGridLayout()
        setup_buttons_layout.setSpacing(6)
        # Variable name edit fields and all constraint labels/edit fields go here
        constraints_layout = QGridLayout()
        constraints_layout.setVerticalSpacing(2)
        constraints_layout.setHorizontalSpacing(2)
        # The inequalities and associated values are placed here.
        # This is a separate layout because they are present on the far right regardless of how many variables there are.
        inequality_layout = QGridLayout()
        inequality_layout.setSpacing(2)
        # Both constraints_layout and inequality_layout are placed here
        setup_fields_layout = QGridLayout()
        setup_fields_layout.setSpacing(2)
        setup_fields_layout.setContentsMargins(4, 4, 4, 4)
        # Layout for solution steps.
        self.soln_table_layout = QGridLayout()
        self.soln_table_layout.setSpacing(0)
        # Parent layout for solution layout is for proper spacing purposes
        soln_table_parent_layout = QGridLayout()
        # Settings layout
        settings_layout = QGridLayout()

        # Frames will contain primary layouts and be hidden/shown to simulate different "screens"
        self.setup_screen = QFrame()
        self.setup_screen.setLayout(setup_parent_layout)

        self.soln_screen = QFrame()
        self.soln_screen.setLayout(soln_parent_layout)
        self.soln_screen.hide()

        self.settings_screen = QFrame()
        self.settings_screen.setLayout(settings_layout)
        self.settings_screen.hide()

        # Used in Simplex.change_screens for screen switching
        self.current_screen = self.setup_screen
        self.previous_screen = self.setup_screen

        # Spacers to force items in layouts into desired positions
        hori_spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        vert_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # print(dir(vert_spacer))

        # Placement of initial setup button -- constraint/variable labels, +/- buttons, and edit fields
        setup_buttons_layout.addWidget(variables_label,      0, 0, 1, 3, Qt.AlignCenter)
        setup_buttons_layout.addWidget(constraints_label,    0, 3, 1, 3, Qt.AlignCenter)
        setup_buttons_layout.addWidget(variables_decrease,   1, 0)
        setup_buttons_layout.addWidget(variables_edit,       1, 1)
        setup_buttons_layout.addWidget(variables_increase,   1, 2)
        setup_buttons_layout.addWidget(constraints_decrease, 1, 3)
        setup_buttons_layout.addWidget(constraints_edit,     1, 4)
        setup_buttons_layout.addWidget(constraints_increase, 1, 5)
        setup_buttons_layout.addWidget(self.max_min_button,  2, 0, 1, 6)
        setup_buttons_layout.addWidget(randomize__button,    3, 0, 1, 3)
        setup_buttons_layout.addWidget(reset_button,         3, 3, 1, 3)
        setup_buttons_layout.addWidget(calculate_button,     4, 0, 1, 6)

        # Placement of objective function and constraint value fields
        setup_fields_layout.addItem(hori_spacer,          0, 0)
        setup_fields_layout.addLayout(constraints_layout, 0, 1, Qt.AlignTop)
        setup_fields_layout.addLayout(inequality_layout,  0, 2, Qt.AlignTop)
        setup_fields_layout.addItem(hori_spacer,          0, 3)

        # Horizontal spacers will force labels together regardless of how wide window is
        soln_table_parent_layout.addItem(hori_spacer,              0, 0)
        soln_table_parent_layout.addLayout(self.soln_table_layout, 0, 1, Qt.AlignTop)
        soln_table_parent_layout.addItem(hori_spacer,              0, 2)

        # Add scrollbar functionality to setup fields and solution table
        # https://codeloop.org/pyqt5-gui-creating-qscrollarea/
        setup_scroll_widget = QWidget()
        setup_scroll_widget.setLayout(setup_fields_layout)
        setup_scroll_area = QScrollArea()
        setup_scroll_area.setWidget(setup_scroll_widget)
        setup_scroll_area.setWidgetResizable(True)

        soln_scroll_widget = QWidget()
        soln_scroll_widget.setLayout(soln_table_parent_layout)
        soln_scroll_area = QScrollArea()
        soln_scroll_area.setWidget(soln_scroll_widget)
        soln_scroll_area.setWidgetResizable(True)

        # Placement of sub layouts in primary layouts
        setup_parent_layout.addWidget(settings_button,      0, 0, Qt.AlignRight)
        setup_parent_layout.addLayout(setup_buttons_layout, 1, 0, Qt.AlignCenter)
        setup_parent_layout.addWidget(setup_scroll_area,    2, 0)

        soln_parent_layout.addWidget(back_button,      0, 0, Qt.AlignLeft)
        soln_parent_layout.addWidget(settings_button2, 0, 1, Qt.AlignRight)
        soln_parent_layout.addWidget(soln_scroll_area, 1, 0, 1, 2)

        settings_layout.addWidget(back_button2,        0, 0, Qt.AlignLeft)
        settings_layout.addWidget(self.palette_button, 1, 0, Qt.AlignTop)
        settings_layout.addItem(hori_spacer,           0, 1)

        # Placement of primary sublayouts within main parent layout
        parent_layout.addWidget(self.setup_screen)
        parent_layout.addWidget(self.soln_screen)
        parent_layout.addWidget(self.settings_screen)

        # Create object which destroys/creates all constraint and variable editing fields
        self.simplex_setup = SimplexSetup(self.window, setup_fields_layout, variables_edit, constraints_edit)

        # Override window's keyPressEvent to do things upon keystrokes
        self.window.keyPressEvent = self.key_pressed
        self.window.setLayout(parent_layout)
        self.window.show()
        self.app.exec()

    def QLE_valid_range(self, qle: QLineEdit, start: int, stop: int) -> None:
        """Limits the integer range of a QLineEdit widget.

        Parameters
        ---
        qle: PyQt QLineEdit object

        start: int
            The starting value for the range.
        stop: int
            The stopping value for the range -- INCLUSIVE
        """
        if qle.text().isdigit():
            value = int(qle.text())
        else:
            value = 0
        if value > stop:
            qle.setText(str(stop))
        elif value < start:
            qle.setText(str(start))

    def QLE_inc_dec(self, qle: QLineEdit, start: int, stop: int, increment: bool = True) -> None:
        """Increments or decrements the integer value of a QLineEdit widget.

        Parameters
        ---
        qle: PyQt QLineEdit object

        start: int
            Cannot decrement below this value.
        stop: int
            Cannot increment above this value -- INCLUSIVE
        increment: bool, optional
            Defaulted True. Set to False to decrement.
        """
        value = int(qle.text())
        if increment and value < stop:
            qle.setText(str(value + 1))
        elif not increment and value > start:
            qle.setText(str(value - 1))

    def toggle_palette(self) -> None:
        """Toggles between light and dark modes when self.palette_button is pressed.
        """
        if self.palette_mode:
            self.palette_button.setText("Dark Mode")
            self.window.setStyleSheet(SIMPLEX_STYLE_DARK)
        else:
            self.palette_button.setText("Light Mode")
            self.window.setStyleSheet(SIMPLEX_STYLE_LIGHT)
        self.palette_mode = not self.palette_mode

    def toggle_max_min(self) -> None:
        """Toggles between maximize/minimize when self.max_min_button is pressed,
        changing inequality labels and dictating simplex calulation approach.
        """
        if self.is_maximized:
            self.max_min_button.setText("Minimize")
            # Index slice to exclude first element as that is the objective function's "="
            for i in range(len(self.simplex_setup.QLEInqs))[1:]:
                self.simplex_setup.QLEInqs[i].label.setText("≥")
        else:
            self.max_min_button.setText("Maximize")
            for i in range(len(self.simplex_setup.QLEInqs))[1:]:
                self.simplex_setup.QLEInqs[i].label.setText("≤")
        self.is_maximized = not self.is_maximized

    def key_pressed(self, event):
        """Override function for main window.

        Closes application when escape key is pressed.
        https://stackoverflow.com/a/36556695
        """
        if event.key() == Qt.Key_Escape:
            self.window.close()
            self.app.quit()

    def reset_fields(self) -> None:
        """Clears all initial input fields and deletes SimplexSolve object, clearing solution table. 
        Connected to reset_button.
        """
        try:
            del self.simplex_solve
        except AttributeError:
            print("No solution to delete.")
        finally:
            self.simplex_setup.reset_fields()

    def randomize_fields(self) -> None:
        """Randomizes all initial input fields.
        Connected to randomize_button.
        """
        self.simplex_setup.randomize_fields()

    def calculate(self) -> None:
        """Create's SimplexSolve object, deletes old one if it exists, and displays solution frame
        Connected to calculate_button.
        """
        try:
            del self.simplex_solve
        except AttributeError:
            print("No current solution to delete. Generating new one.")
        finally:
            self.change_screens(self.soln_screen)
            self.simplex_solve = SimplexSolve(self.window, self.soln_table_layout, self.simplex_setup)

    def open_settings(self) -> None:
        """Open settings menu.
        Set previous screen to current previous, current screen to settings frame.
        """
        self.change_screens(self.settings_screen)

    def go_back(self) -> None:
        """Changes self.current_screen to self.previous_screen
        """
        self.change_screens(self.previous_screen)

    def change_screens(self, new_screen: QFrame) -> None:
        """Changes frame visibility to new QFrame.

        Parameters
        ---
        new_screen: PyQt QFrame
            The frame to be shown.
            Expected frames are self.setup_screen, self.soln_screen, self.settings_screen
        """
        self.current_screen.hide()
        # When changing from settings screen back to solutions screen, prevent back button from going back to settings
        if self.current_screen == self.settings_screen and new_screen == self.soln_screen:
            self.previous_screen = self.setup_screen
        else:
            self.previous_screen = self.current_screen
        self.current_screen = new_screen
        self.current_screen.show()


class SimplexSolve:
    """Generates and displays all solution steps.
    """
    def __init__(self, window: QWidget, layout: QGridLayout, simplex_setup: SimplexSetup):
        """
        Parameters
        ---
        window: PyQt QWidget
        layout: PyQt QGridLayout
        simplex_setup: SimplexSetup
        """
        self.window = window
        self.layout = layout
        self.simplex_setup = simplex_setup
        self.matrices = []
        soln_matrix, self.label_matrix = self.create_initial_matrices()
        self.matrices.append(soln_matrix)

    def __del__(self):
        for matrix_row in self.label_matrix:
            for i in range(len(matrix_row))[::-1]:
                deleted_widget = matrix_row.pop(i)
                self.layout.removeWidget(deleted_widget)
                deleted_widget.deleteLater()
                del deleted_widget
        del self

    def create_initial_matrices(self) -> list:
        """Turns a matrix of values from initial input objective function and constraint fields into the initial
        matrix used for applying simplex method and creates a corresponding matrix of label widgets.
        
        Returns
        ---
        tuple
            Returns a tuple of two matrices -- the initial solution matrix and a corresponding label matrix.

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
        val_matrix = self.simplex_setup.get_fields()
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
            # Insert slack values before constraint inequality value.
            for i in range(len(val_matrix)):
                val = 1 if i == row else 0
                soln_matrix[row].insert(-1, val)

        # Create label matrix from solution matrix
        label_matrix = [[]]
        # Start with creating name labels on first row (e.g. X1, X2, S1, S2, Z)
        widget_list = self.simplex_setup.QLEVars+self.simplex_setup.QLEVars[0].constraint_col+[self.simplex_setup.QLEInqs[0]]
        for col, widget in enumerate(widget_list):
            label = QLabelSimplex(self.window, self.layout, widget.get_name(), 0, col, ["bottom"])
            label_matrix[0].append(label)
        # Add a blank label with borders to complete lines in table
        label = QLabelSimplex(self.window, self.layout, "", 0, col+ + 1, ["bottom", "left"])
        label_matrix[0].append(label)

        # Create all other labels of constraint and objective function values
        for row, matrix_row in enumerate(soln_matrix):
            label_matrix.append([])
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
                label_matrix[row + 1].append(label)

        return soln_matrix, label_matrix


if __name__ == "__main__":
    simplex = SimplexCalculator()

