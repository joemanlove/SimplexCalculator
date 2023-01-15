"""Simplex Calculator

Made with PyQt5
"""

import sys
import webbrowser

from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QSpacerItem, QSizePolicy,
                             QFrame, QGridLayout, QScrollArea, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp, QPropertyAnimation, QEasingCurve, QRect

from setup import SimplexSetup
from solve import SimplexSolve
from classes import SPushButton, SCircleButton, SSettingsButton
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

    DEFUALT_FONT_SIZE = 15
    # Sets weather dark mode is on by default.
    is_dark_mode = True

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
        # Used when swapping between light and dark mode.
        self.style_sheets = [SIMPLEX_STYLE_LIGHT, SIMPLEX_STYLE_DARK]
        # All widgets with SIcons should be placed here for color swapping.
        self.icon_buttons = []
        self.font_style = (f"QWidget {{font-size: {self.DEFUALT_FONT_SIZE}px;}}")

        ### Setting Variables
        variables_label = QLabel(self.window)
        variables_label.setText("Set Variables")
        # Decrease Variables Button
        variables_decrease = SPushButton(self.window, "-", self.WIDGET_WIDTH)
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
        variables_increase = SPushButton(self.window, "+", self.WIDGET_WIDTH)
        variables_increase.clicked.connect(lambda: (
            self.QLE_inc_dec(variables_edit, self.MIN_VARIABLES, self.MAX_VARIABLES),
            self.simplex_setup.update()))

        ### Setting Constraints
        constraints_label = QLabel(self.window)
        constraints_label.setText("Set Constraints")
        # Decrease Constraints Button
        constraints_decrease = SPushButton(self.window, "-", self.WIDGET_WIDTH)
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
        constraints_increase = SPushButton(self.window, "+", self.WIDGET_WIDTH)
        constraints_increase.clicked.connect(lambda: (
            self.QLE_inc_dec(constraints_edit, self.MIN_CONSTRAINTS, self.MAX_CONSTRAINTS),
            self.simplex_setup.update()))

        # Toggle Maximize/Minimize Button
        self.is_maximize = True
        self.max_min_button = QPushButton(self.window)
        self.max_min_button.setText("Maximize")
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
        # Duplicate buttons are necessary because the same widget cannot be in two different frames or layouts.
        back_button = SCircleButton(self.window)
        back_button.set_icon("back.png")
        back_button.clicked.connect(self.go_back)
        self.icon_buttons.append(back_button)
        back_button2 = SCircleButton(self.window)
        back_button2.set_icon("back.png")
        back_button2.clicked.connect(self.go_back)
        self.icon_buttons.append(back_button2)

        # Settings Button -- Open Settings screen.
        settings_button = SCircleButton(self.window)
        settings_button.set_icon("settings.png")
        settings_button.clicked.connect(self.open_settings)
        self.icon_buttons.append(settings_button)
        settings_button2 = SCircleButton(self.window)
        settings_button2.set_icon("settings.png")
        settings_button2.clicked.connect(self.open_settings)
        self.icon_buttons.append(settings_button2)

        ### Solution Screen Buttons
        # Solution Step Label -- Display step number out of total steps e.g. 1/3
        self.soln_step_label = QLabel(self.window)
        self.soln_step_label.setStyleSheet("font-size: 30px")

        # First Solution Button -- Skip to initial step.
        first_soln_button = SCircleButton(self.window)
        first_soln_button.set_icon("first.png")
        # Lambdas are necessary because object does not yet exist
        first_soln_button.clicked.connect(lambda: self.simplex_solve.first_step())
        self.icon_buttons.append(first_soln_button)

        # Previous Solution Button
        prev_soln_button = SCircleButton(self.window)
        prev_soln_button.set_icon("previous.png")
        prev_soln_button.clicked.connect(lambda: self.simplex_solve.prev_step())
        self.icon_buttons.append(prev_soln_button)

        # Next Solution Button
        next_soln_button = SCircleButton(self.window)
        next_soln_button.set_icon("next.png")
        next_soln_button.clicked.connect(lambda: self.simplex_solve.next_step())
        self.icon_buttons.append(next_soln_button)

        # Last Solution Button
        last_soln_button = SCircleButton(self.window)
        last_soln_button.set_icon("last.png")
        last_soln_button.clicked.connect(lambda: self.simplex_solve.last_step())
        self.icon_buttons.append(last_soln_button)

        ### Settings Screen Buttons
        # Toggle Dark Mode Button
        self.dark_mode_button = SSettingsButton(self.window, "Dark Mode")
        self.dark_mode_button.set_setting_label()
        self.dark_mode_button.clicked.connect(self.toggle_dark_mode)

        # Change Font Size Button
        font_size_button = SSettingsButton(self.window, "Font Size")
        font_size_button.set_line_edit()
        font_size_button.line_edit.setText(str(self.DEFUALT_FONT_SIZE))
        font_size_button.line_edit.editingFinished.connect(lambda: (
            # Limit range to 12 through 22
            self.QLE_valid_range(font_size_button.line_edit, 12, 22),
            self.change_font_size(int(font_size_button.line_edit.text())),
            font_size_button.line_edit.clearFocus()))

        # Opens GitHub repo.
        github_button = SSettingsButton(self.window, "Visit Simplex Calculator on GitHub")
        github_button.set_icon("github.png")
        github_button.clicked.connect(self.open_github)
        self.icon_buttons.append(github_button)

        ### Layouts and Widget Placement
        # Primary layout for main window -- All child layouts are placed here.
        parent_layout = QHBoxLayout()
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
        soln_button_layout = QGridLayout()

        # Settings Layout
        settings_layout = QGridLayout()
        settings_layout.setAlignment(Qt.AlignTop)

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
        soln_button_layout.addWidget(self.soln_step_label,   0, 0, 1, 4, Qt.AlignCenter)
        soln_button_layout.addWidget(first_soln_button, 1, 0)
        soln_button_layout.addWidget(prev_soln_button,  1, 1)
        soln_button_layout.addWidget(next_soln_button,  1, 2)
        soln_button_layout.addWidget(last_soln_button,  1, 3)

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

        settings_layout.addWidget(back_button2,          0, 0)
        settings_layout.addWidget(self.dark_mode_button, 1, 0)
        settings_layout.addWidget(font_size_button,      2, 0)
        settings_layout.addWidget(github_button,         3, 0)

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

        # Apply current dark_mode settings to palette and icon buttons.
        self.is_dark_mode = not self.is_dark_mode
        self.toggle_dark_mode()
        # Create object which destroys/creates all constraint and variable editing fields.
        self.simplex_setup = SimplexSetup(self.window, setup_fields_layout, variables_edit, constraints_edit)
        # Object which creates solution table when calculate_button is pressed goes here.
        self.simplex_solve = None

        # Override window's keyPressEvent to do things upon keystrokes.
        self.window.keyPressEvent = self.key_pressed
        # Make go.
        self.window.setLayout(parent_layout)
        self.window.show()
        sys.exit(self.app.exec())

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

    def toggle_max_min(self) -> None:
        """Toggles between maximize/minimize when self.max_min_button is pressed,
        changing inequality labels and dictating simplex calulation approach.
        """
        # Index slice to exclude first element as that is the objective function's "=".
        for i in range(len(self.simplex_setup.SLEIneqs))[1:]:
            if self.is_maximize:
                self.max_min_button.setText("Minimize")
                self.simplex_setup.SLEIneqs[i].label.setText("≥")
            else:
                self.max_min_button.setText("Maximize")
                self.simplex_setup.SLEIneqs[i].label.setText("≤")
        self.is_maximize = not self.is_maximize

    def calculate(self) -> None:
        """Creates SimplexSolve object, deletes old one if it exists, and displays solution frame.
        Connected to calculate_button.
        """
        if self.simplex_solve is not None:
            self.simplex_solve.delete()
        self.change_screens(self.soln_screen)
        self.simplex_solve = SimplexSolve(self.window, self.soln_table_layout, self.simplex_setup,
            self.soln_step_label, self.is_maximize)

    def open_settings(self) -> None:
        """Open settings menu.
        Set previous screen to current previous, current screen to settings frame.
        """
        self.change_screens(self.settings_screen)

    def go_back(self) -> None:
        """Changes self.current_screen to self.previous_screen
        """
        self.change_screens(self.previous_screen, True)

    def toggle_dark_mode(self) -> None:
        """Toggles between dark mode on/off when self.dark_mode_button is pressed.
        """
        # is_dark_mode will act as an index for selecting style sheet from self.style_sheets.
        self.is_dark_mode = not self.is_dark_mode
        off_on = ["Off", "On"]
        self.dark_mode_button.setText(off_on[self.is_dark_mode])
        # Preserve current font size.
        self.window.setStyleSheet(self.font_style + self.style_sheets[self.is_dark_mode])
        # Change all icon colors.
        for button in self.icon_buttons:
            button.icon.color_swap(self.is_dark_mode)

    def change_font_size(self, font_size: int) -> None:
        """Changes font size via global style sheet from limited user input.

        Connected to font_size_button in settings screen.

        Parameters
        ---
        font_size: int
        """
        # Updates self.font_style, concatenates it with the current dark/light mode style sheet, and sets it.
        self.font_style = (f"QWidget {{font-size: {font_size}px;}}")
        self.window.setStyleSheet(self.font_style + self.style_sheets[self.is_dark_mode])

    def open_github(self) -> None:
        """Opens Simplex Calculator's GitHub repo in the default browser.

        https://github.com/nonetypes/SimplexCalculator
        """
        webbrowser.get().open("https://github.com/nonetypes/SimplexCalculator", new = 2)

    def change_screens(self, new_screen: QFrame, is_going_back: bool = False) -> None:
        """Changes frame visibility to new QFrame.

        Parameters
        ---
        new_screen: PyQt QFrame
            The frame to be shown.
            Expected frames are self.setup_screen, self.soln_screen, self.settings_screen
        is_going_back: bool, optional
            Defaulted False. Set to true if back button was pressed, making new screen enter from left
            side, otherwise it will enter in from right.
        """
        # Disable old screen to prevent selection of last button pressed (on old screen) with spacebar.
        self.current_screen.setDisabled(True)
        self.current_screen.hide()
        new_screen.setDisabled(False)
        new_screen.show()

        # Create animation to make new screen "slide" into view.
        # https://forum.qt.io/topic/3709/simple-animation-not-working/3
        self.animation = QPropertyAnimation(new_screen, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)

        # If back button was pressed, screen will appear to slide in from left.
        if is_going_back:
            self.animation.setStartValue(QRect(-self.window.width(), self.current_screen.y(),
                self.window.width(), self.window.height()))
        # If back button was not pressed, screen will appear to slide in from right.
        else:
            self.animation.setStartValue(QRect(self.window.width(), self.current_screen.y(),
                self.window.width(), self.window.height()))

        self.animation.setEndValue(self.current_screen.geometry())
        self.animation.start()

        # When changing from settings screen back to solutions screen, prevent back button from going back to settings.
        if self.current_screen == self.settings_screen and new_screen == self.soln_screen:
            self.previous_screen = self.setup_screen
        else:
            self.previous_screen = self.current_screen
        self.current_screen = new_screen

    def key_pressed(self, event):
        """Override function for main window.

        Closes application when escape key is pressed.
        https://stackoverflow.com/a/36556695
        """
        if event.key() == Qt.Key_Escape:
            self.window.close()
            self.app.quit()
