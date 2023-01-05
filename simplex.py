"""Simplex Calculator

Made with PyQt5
"""

from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QSpacerItem, QSizePolicy,
                             QGridLayout, QScrollArea, QFrame, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp

from setup import SimplexSetup
from solve import SimplexSolve
from classes import QPBSimplex
from styles import SIMPLEX_STYLE_LIGHT, SIMPLEX_STYLE_DARK


class SimplexCalculator:
    """Main class for Simplex Calculator.
    Main PyQt window and app, as well as buttons and layouts are kept here.
    Handles SimplexSetup and SimplexSolve objects -- setup fields handling and applying simplex method respectively.
    """
    # Dimensions
    WINDOW_WIDTH = 480
    WINDOW_HEIGHT = 800
    WIDGET_WIDTH = 32
    # Setting and limiting user-editable parameters.
    START_VARIABLES = 2
    START_CONSTRAINTS = 2
    MIN_VARIABLES = 2
    MAX_VARIABLES = 20
    MIN_CONSTRAINTS = 1
    MAX_CONSTRAINTS = 20
    # Sets weather dark palette is on by default.
    dark_mode = True

    def __init__(self):
        """
        Main PyQt window and app, as well as buttons and layouts are created here.
        """
        # Create main Qt app and window.
        self.app = QApplication([])
        self.app.setStyle("Fusion")
        self.window = QWidget()
        self.window.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.window.setMinimumSize(380, 480)
        self.window.setWindowTitle("Simplex Method")

        ### Setting Variables
        variables_label = QLabel(self.window)
        variables_label.setText("Set Variables")
        # Decrease Variables Button
        variables_decrease = QPBSimplex(self.window, "-", self.WIDGET_WIDTH)
        variables_decrease.clicked.connect(lambda: (
            self.QLE_inc_dec(variables_edit, self.MIN_VARIABLES, self.MAX_VARIABLES, False),
            self.simplex_setup.update()))
        # QLineEdit Widget -- Updates as increase/decrease are pressed and is editable.
        variables_edit = QLineEdit(self.window)
        # Limit field input to digits -- Allow empty strings to enable user to clear field.
        variables_edit.setValidator(QRegExpValidator(QRegExp('(^[0-9]+$|^$)')))
        variables_edit.setMaxLength(2)
        variables_edit.setText(str(self.START_VARIABLES))
        variables_edit.setMaximumWidth(self.WIDGET_WIDTH)
        variables_edit.setAlignment(Qt.AlignCenter)
        variables_edit.editingFinished.connect(lambda: (
            self.QLE_valid_range(variables_edit, self.MIN_VARIABLES, self.MAX_VARIABLES),
            self.simplex_setup.update()))
        # Increase Variables Button
        variables_increase = QPBSimplex(self.window, "+", self.WIDGET_WIDTH)
        variables_increase.clicked.connect(lambda: (
            self.QLE_inc_dec(variables_edit, self.MIN_VARIABLES, self.MAX_VARIABLES),
            self.simplex_setup.update()))

        ### Setting Constraints
        constraints_label = QLabel(self.window)
        constraints_label.setText("Set Constraints")
        # Decrease Constraints Button
        constraints_decrease = QPBSimplex(self.window, "-", self.WIDGET_WIDTH)
        constraints_decrease.clicked.connect(lambda: (
            self.QLE_inc_dec(constraints_edit, self.MIN_CONSTRAINTS, self.MAX_CONSTRAINTS, False),
            self.simplex_setup.update()))
        # QLineEdit Widget -- Updates as increase/decrease are pressed and is direclty editable.
        constraints_edit = QLineEdit(self.window)
        constraints_edit.setValidator(QRegExpValidator(QRegExp('(^[0-9]+$|^$)')))
        constraints_edit.setMaxLength(2)
        constraints_edit.setText(str(self.START_CONSTRAINTS))
        constraints_edit.setMaximumWidth(self.WIDGET_WIDTH)
        constraints_edit.setAlignment(Qt.AlignCenter)
        constraints_edit.editingFinished.connect(lambda: (
            self.QLE_valid_range(constraints_edit, self.MIN_CONSTRAINTS, self.MAX_CONSTRAINTS),
            self.simplex_setup.update()))
        # Increase Constraints Button
        constraints_increase = QPBSimplex(self.window, "+", self.WIDGET_WIDTH)
        constraints_increase.clicked.connect(lambda: (
            self.QLE_inc_dec(constraints_edit, self.MIN_CONSTRAINTS, self.MAX_CONSTRAINTS),
            self.simplex_setup.update()))

        # Toggle Maximize/Minimize Button
        self.is_maximize = True
        self.max_min_button = QPushButton(self.window)
        self.max_min_button.setText("Maximize")
        # self.toggle_max_min()
        self.max_min_button.clicked.connect(self.toggle_max_min)

        # Randomize Button - Sets random values in all fields.
        randomize__button = QPushButton(self.window)
        randomize__button.setText("Randomize")
        # Lambdas are necessary because object does not yet exist as it requires layouts which do not exist.
        randomize__button.clicked.connect(lambda: self.simplex_setup.randomize_fields())

        # Reset Button
        reset_button = QPushButton(self.window)
        reset_button.setText("Reset")
        reset_button.clicked.connect(lambda: self.simplex_setup.reset_fields())

        # Calculate Button -- Generate SimplexSolve object and display solution screen.
        calculate_button = QPushButton(self.window)
        calculate_button.setText("Calculate")
        calculate_button.clicked.connect(self.calculate)

        # Back Button -- Go back to the previous screen.
        # Duplicate buttons are necessary because the same widget cannot be in two different frames or layouts
        back_button = QPushButton(self.window)
        back_button.setText("Back")
        back_button.clicked.connect(self.go_back)
        back_button2 = QPushButton(self.window)
        back_button2.setText("Back")
        back_button2.clicked.connect(self.go_back)

        # Settings Button -- Open Settings screen.
        settings_button = QPushButton(self.window)
        settings_button.setText("Settings")
        settings_button.clicked.connect(self.open_settings)
        settings_button2 = QPushButton(self.window)
        settings_button2.setText("Settings")
        settings_button2.clicked.connect(self.open_settings)

        # Toggle Dark Mode Button
        self.dark_mode_button = QPushButton(self.window)
        # self.dark_mode_button.setFixedWidth(300)
        self.dark_mode_button.clicked.connect(self.toggle_dark_mode)
        self.toggle_dark_mode()

        # First Solution Button
        first_soln_button = QPushButton(self.window)
        first_soln_button.setText("|<")
        # Lambdas are necessary because object does not yet exist
        first_soln_button.clicked.connect(lambda: self.simplex_solve.first_step())

        # Previous Solution Button
        prev_soln_button = QPushButton(self.window)
        prev_soln_button.setText("<")
        prev_soln_button.clicked.connect(lambda: self.simplex_solve.prev_step())

        # Next Solution Button
        next_soln_button = QPushButton(self.window)
        next_soln_button.setText(">")
        next_soln_button.clicked.connect(lambda: self.simplex_solve.next_step())

        # Last Solution Button
        last_soln_button = QPushButton(self.window)
        last_soln_button.setText(">|")
        last_soln_button.clicked.connect(lambda: self.simplex_solve.last_step())


        ### Layouts and Widget Placement
        # Primary layout for main window -- All child layouts are placed here.
        parent_layout = QVBoxLayout()
        # parent_layout.setSpacing(0)
        parent_layout.setContentsMargins(0, 12, 0, 12)

        ### Setup Screen Layouts
        # Sublayouts for setup screen are placed here.
        setup_parent_layout = QGridLayout()
        # The initial set variables/constraints and maximize/minimize buttons and associated widgets go here.
        setup_buttons_layout = QGridLayout()
        setup_buttons_layout.setSpacing(6)
        # Variable name edit fields and all constraint labels/edit fields go here.
        constraints_layout = QGridLayout()
        constraints_layout.setVerticalSpacing(2)
        constraints_layout.setHorizontalSpacing(2)
        constraints_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        # The inequalities and associated values are placed here.
        # This is a separate layout because they are present on the far right regardless of how many variables there are.
        inequality_layout = QGridLayout()
        inequality_layout.setSpacing(2)
        inequality_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        # Scroll area layout -- Both constraints_layout and inequality_layout are placed here.
        setup_fields_layout = QHBoxLayout()
        setup_fields_layout.setSpacing(2)
        setup_fields_layout.setContentsMargins(4, 4, 4, 4)
        setup_fields_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        ### Solution Screen Layouts
        # Sublayouts for solution screen are placed here.
        soln_parent_layout = QGridLayout()
        # Layout for displaying solution steps as labels. This will be a scroll area.
        self.soln_table_layout = QGridLayout()
        self.soln_table_layout.setSpacing(0)
        self.soln_table_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        # Button layout for cycling through solution steps.
        soln_button_layout = QHBoxLayout()

        # Settings Layout
        settings_layout = QGridLayout()

        # Spacers to fill empty voids and force items in layouts into desired positions.
        hori_spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        vert_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # print(dir(vert_spacer))

        # Placement of initial setup button -- constraint/variable labels, +/- buttons, and edit fields.
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

        # Placement of objective function and constraint value fields.
        setup_fields_layout.addLayout(constraints_layout)
        setup_fields_layout.addLayout(inequality_layout)

        # These buttons will sit below solution step table.
        soln_button_layout.addWidget(first_soln_button)
        soln_button_layout.addWidget(prev_soln_button)
        soln_button_layout.addWidget(next_soln_button)
        soln_button_layout.addWidget(last_soln_button)

        # Add scrollbar functionality to setup fields.
        # https://codeloop.org/pyqt5-gui-creating-qscrollarea/
        setup_scroll_widget = QWidget()
        setup_scroll_widget.setLayout(setup_fields_layout)
        setup_scroll_area = QScrollArea()
        setup_scroll_area.setWidget(setup_scroll_widget)
        setup_scroll_area.setWidgetResizable(True)
        # Remove scroll area from tabbing order.
        setup_scroll_area.setFocusPolicy(Qt.NoFocus)

        # Add scrollbar functionality to solution table.
        soln_scroll_widget = QWidget()
        soln_scroll_widget.setLayout(self.soln_table_layout)
        soln_scroll_area = QScrollArea()
        soln_scroll_area.setWidget(soln_scroll_widget)
        soln_scroll_area.setWidgetResizable(True)
        soln_scroll_area.setFocusPolicy(Qt.NoFocus)

        # Placement of sublayouts and widgets in primary layouts.
        setup_parent_layout.addWidget(settings_button,      0, 0, Qt.AlignRight)
        setup_parent_layout.addLayout(setup_buttons_layout, 1, 0, Qt.AlignCenter)
        setup_parent_layout.addWidget(setup_scroll_area,    2, 0)

        soln_parent_layout.addWidget(back_button,        0, 0, Qt.AlignLeft)
        soln_parent_layout.addWidget(settings_button2,   0, 1, Qt.AlignRight)
        soln_parent_layout.addWidget(soln_scroll_area,   1, 0, 1, 2)
        soln_parent_layout.addLayout(soln_button_layout, 2, 0, 1, 2, Qt.AlignCenter)

        settings_layout.addWidget(back_button2,          0, 0, Qt.AlignLeft)
        settings_layout.addWidget(self.dark_mode_button, 1, 0, Qt.AlignTop)
        settings_layout.addItem(hori_spacer,             0, 1)

        # Frames will contain primary layouts and be hidden/shown to simulate different "screens".
        self.setup_screen = QFrame()
        self.setup_screen.setLayout(setup_parent_layout)

        self.soln_screen = QFrame()
        self.soln_screen.setLayout(soln_parent_layout)
        self.soln_screen.hide()

        self.settings_screen = QFrame()
        self.settings_screen.setLayout(settings_layout)
        self.settings_screen.hide()

        # Placement of frames within main parent layout.
        parent_layout.addWidget(self.setup_screen)
        parent_layout.addWidget(self.soln_screen)
        parent_layout.addWidget(self.settings_screen)

        # Used in self.change_screens for screen switching.
        self.current_screen = self.setup_screen
        self.previous_screen = self.setup_screen

        # Create object which destroys/creates all constraint and variable editing fields.
        self.simplex_setup = SimplexSetup(self.window, setup_fields_layout, variables_edit, constraints_edit)
        # Object which creates solution table when calculate_button is pressed.
        self.simplex_solve = None

        # Override window's keyPressEvent to do things upon keystrokes.
        self.window.keyPressEvent = self.key_pressed
        self.window.setLayout(parent_layout)
        # Make go.
        self.window.show()
        self.app.exec()

    def QLE_valid_range(self, qle: QLineEdit, start: int, stop: int) -> None:
        """Limits the integer range of a QLineEdit widget.

        Parameters
        ---
        qle: PyQt QLineEdit
            The edit field widget.
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
        qle: PyQt QLineEdit
            The edit field widget.
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

    def toggle_dark_mode(self) -> None:
        """Toggles between light and dark modes when self.dark_mode_button is pressed.
        """
        # TODO: Change to make in terms of dark mode on/off.
        if self.dark_mode:
            self.dark_mode_button.setText("Dark Mode")
            self.window.setStyleSheet(SIMPLEX_STYLE_DARK)
        else:
            self.dark_mode_button.setText("Light Mode")
            self.window.setStyleSheet(SIMPLEX_STYLE_LIGHT)
        self.dark_mode = not self.dark_mode

    def toggle_max_min(self) -> None:
        """Toggles between maximize/minimize when self.max_min_button is pressed,
        changing inequality labels and dictating simplex calulation approach.
        """
        if self.is_maximize:
            self.max_min_button.setText("Minimize")
            # Index slice to exclude first element as that is the objective function's "=".
            for i in range(len(self.simplex_setup.QLEInqs))[1:]:
                self.simplex_setup.QLEInqs[i].label.setText("≥")
        else:
            self.max_min_button.setText("Maximize")
            for i in range(len(self.simplex_setup.QLEInqs))[1:]:
                self.simplex_setup.QLEInqs[i].label.setText("≤")
        self.is_maximize = not self.is_maximize

    def key_pressed(self, event):
        """Override function for main window.

        Closes application when escape key is pressed.
        https://stackoverflow.com/a/36556695
        """
        if event.key() == Qt.Key_Escape:
            self.window.close()
            self.app.quit()

    def calculate(self) -> None:
        """Create's SimplexSolve object, deletes old one if it exists, and displays solution frame.
        Connected to calculate_button.
        """
        if self.simplex_solve is not None:
            self.simplex_solve.delete()
        self.change_screens(self.soln_screen)
        self.simplex_solve = SimplexSolve(self.window, self.soln_table_layout, self.simplex_setup, self.is_maximize)

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
        # When changing from settings screen back to solutions screen, prevent back button from going back to settings.
        if self.current_screen == self.settings_screen and new_screen == self.soln_screen:
            self.previous_screen = self.setup_screen
        else:
            self.previous_screen = self.current_screen
        self.current_screen = new_screen
        self.current_screen.show()


if __name__ == "__main__":
    simplex_calculator = SimplexCalculator()
