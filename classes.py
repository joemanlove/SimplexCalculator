"""Customized PyQt widgets for Simplex Calculator.

SCircleButton: QToolButton child
SPushButton: QPushButton child
SSettingsButton: QToolButton child
SIcon: QIcon child
SLabelSolve: QLabel child
SLEVar: QLineEdit child
SLECon: QLineEdit child
SLEIneq: QLineEdit child
"""

from os import path

from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QLabel, QGridLayout, QComboBox,
                             QToolButton, QSizePolicy, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QRegExpValidator, QRegion, QPixmap, QColor, QIcon, QPixmap
from PyQt5.QtCore import Qt, QRegExp


from styles import SIMPLEX_ICON_LIGHT, SIMPLEX_ICON_DARK


class SCircleButton(QToolButton):
    """Child class of PyQt QToolButton.
    Forces button selection to be a circle.

    https://stackoverflow.com/a/48291001
    """

    def resizeEvent(self, event) -> None:
        """Force button selection area to be a circle.

        https://stackoverflow.com/a/48291001
        """
        self.setMask(QRegion(self.rect(), QRegion.Ellipse))
        QToolButton.resizeEvent(self, event)

    def set_icon(self, icon_name: str) -> None:
        """Displays an icon on the button.

        Parameters
        ---
        icon_name: str
            The file name of the icon with extension. Icons shuold be placed in /assets and
            the directory path should be excluded from the name.
        """
        # Redefined SIcon is used to allow color changes for light/dark mode.
        self.icon = SIcon(self, icon_name)


class SPushButton(QPushButton):
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


class SSettingsButton(QToolButton):
    """Child of PyQt QToolButton. Used to display and change individual settings for Simplex Calculator.
    """
    BUTTON_HEIGHT = 80
    ICON_SIZE = 40
    WIDGET_PADDING = 20

    def __init__(self, window: QWidget, text: str = ""):
        """Child of PyQt QToolButton. Used to display and change individual settings for Simplex Calculator.
        Parameters
        ---
        window: PyQt QWidget
        text: str, optional
            Defaults to "". The descriptive text of the setting to be displayed.
        """
        super().__init__(window)
        # Force button to expand horizontally to fill window
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setStyleSheet(f"height: {self.BUTTON_HEIGHT}px; icon-size: {self.ICON_SIZE}px;")
        # This layout will be used to place icon and label widgets.
        # https://stackoverflow.com/a/44292292
        self.setLayout(QGridLayout())
        self.layout().setAlignment(Qt.AlignLeft)
        self.layout().setSpacing(self.WIDGET_PADDING)
        self.layout().setContentsMargins(self.WIDGET_PADDING, int(self.WIDGET_PADDING*.65),
                                         self.WIDGET_PADDING, int(self.WIDGET_PADDING*.65))

        # The description_label and setting_label (displays current setting) go here.
        self.vert_layout = QVBoxLayout()
        self.vert_layout.setSpacing(4)
        self.layout().addLayout(self.vert_layout, 0, 1)

        # Used to describe setting.
        self.description_label = QLabel()
        self.description_label.setText(text)
        self.description_label.setStyleSheet("background: none;")
        self.vert_layout.addWidget(self.description_label)

    def set_icon(self, icon_name: str):
        """Displays an icon to be associated with the individual setting.

        Parameters
        ---
        icon_name: str
            The file name of the icon with extension. Icons shuold be placed in /assets and
            the directory path should be excluded from the name.
        """
        # Turn this widget's icon into a PushButton so that it can be placed appropriately in layout.
        # Setting an icon, rather than manually rescaling a pixmap on a label, produced better resolution.
        self.icon = QPushButton()
        # Prevent selection of icon button by tabbing.
        self.icon.setFocusPolicy(Qt.NoFocus)
        # Set the pushutton's icon to an SIcon for proper dark mode color swapping.
        self.icon.icon = SIcon(self.icon, icon_name)
        self.icon.setStyleSheet("border: none; background: none;")
        # Override the icon's mousePressEvent with the parent's.
        self.icon.mousePressEvent = self.mousePressEvent
        self.layout().addWidget(self.icon, 0, 0)

    def set_setting_label(self):
        """The setting label will be displayed directly below descriptive label and will display the
        crrent setting, e.g. "On" or "Off".

        Use self.setText to update this label within connected function.
        """
        self.setting_label = SLabelSetting()
        # self.setting_label.setText("More Testing")
        self.setting_label.setStyleSheet("background: none;")
        self.setText = lambda text: self.setting_label.setText(text)
        self.vert_layout.addWidget(self.setting_label)

    def set_line_edit(self) -> None:
        """Creates a QLineEdit widget.

        Used for font size and decimal places setting.
        """
        self.line_edit = QLineEdit()
        self.line_edit.setMaxLength(2)
        self.line_edit.setMaximumWidth(40)
        self.line_edit.setAlignment(Qt.AlignCenter)
        # Limit field input to digits -- Allow empty strings to enable user to clear field.
        self.line_edit.setValidator(QRegExpValidator(QRegExp('(^[0-9]+$|^$)')))
        self.vert_layout.addWidget(self.line_edit)
        
        # Force clicking on entire setting button to engage widget.
        def mouse_release(event):
            self.setDown(False)
            self.line_edit.setFocus()
            self.line_edit.selectAll()

        self.mouseReleaseEvent = mouse_release

class SLabelSetting(QLabel):
    """Setting label for SSettingsButton. Displays current setting text

    Used solely to set custom color within styles.py.
    """
    def __init__(self, window: QWidget = None):
        super().__init__(window)


class SIcon(QIcon):
    """Child class of PyQt QIcon. Allows color swapping between light and dark mode.

    Sourced icons must be solid white in color to properly create color masks.
    """
    def __init__(self, parent, icon_name: str):
        """
        Parameters
        ---
        parent: PyQt object
            The parent widget must be one that has a setIcon method, e.g. QPushButton, QToolButton etc.
        icon_name: str
            The file name of the icon with extension. Icons shuold be placed in /assets and
            the directory path should be excluded from the name.
        """
        super().__init__()
        self.parent = parent
        # Color at index 0 and 1 are light mode color and dark mode color respectively.
        self.colors = [SIMPLEX_ICON_LIGHT, SIMPLEX_ICON_DARK]
        self.current_color = self.colors[0]

        # Change color of icon using a pixel map and a mask.
        # https://stackoverflow.com/a/38369468
        # Icon must be solid white to start with.
        self.pixmap = QPixmap(path.join(path.dirname(__file__), f"assets/{icon_name}"))
        mask = self.pixmap.createMaskFromColor(QColor('#FFFFFF'), Qt.MaskOutColor)
        self.pixmap.fill((QColor(self.current_color)))
        self.pixmap.setMask(mask)
        self.addPixmap(self.pixmap)

        self.parent.setIcon(self)
        # Give parent own's color_swap method.
        self.parent.color_swap = self.color_swap

    def color_swap(self, is_dark_mode: bool) -> None:
        """Swap icon color between dark mode color scheme and light mode color scheme.

        Parameters
        ---
        is_dark_mode: bool
            The current dark mode state. Used as an index to select color from self.colors.
        """
        new_color = self.colors[is_dark_mode]
        mask = self.pixmap.createMaskFromColor(QColor(self.current_color), Qt.MaskOutColor)
        self.pixmap.fill((QColor(new_color)))
        self.pixmap.setMask(mask)
        self.addPixmap(self.pixmap)
        # Parent's icon must be reset.
        self.parent.setIcon(self)
        self.current_color = new_color


class SLabelSolve(QLabel):
    """Child class of PyQt QLabel. Used for displaying components of solutions matrices.
    """
    def __init__(self, window: QWidget, text: str, borders: list = []):
        """Child class of PyQt QLabel. Used for displaying components of solutions matrices.

        Parameters
        ---
        window: PyQt QWidget
            The main window.
        text: str
            The text to be displayed on the label.
        borders: list
            A list of strings indicating what borders will be drawn. Used to create lines of table.
            Expected strings are "top", "bottom", "left", or "right".
        """
        QLabel.__init__(self, window)
        self.setText(text)
        self.setAlignment(Qt.AlignCenter)

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


class SLineEdit(QLineEdit):
    """Child class of PyQt QLineEdit object and parent of SLEVar, SLECon, and SLEIneq child classes.
    """
    def __init__(self, window: QWidget, layout: QGridLayout, row_index: int, col_index: int):
        """Child class of PyQt QLineEdit object and parent of SLEVar, SLECon, and SLEIneq child classes.
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


class SLEVar(SLineEdit):
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
            The object index within the SLE_vars list which also corresponds to the column of the layout.
            Used for default variable name and determining the label text when object is in the first column.
        constraint_col: list
            The list of associated constraint SLECon objects for variable name label updating.
            This is a column of constraint fields in the setup screen.
        """
        SLineEdit.__init__(self, window, layout, row_index, col_index)
        self.constraint_col = constraint_col

        self.name_field = QLineEdit(window)
        self.name_field.setMaxLength(3)
        self.name_field.setMaximumWidth(40)
        self.name_field.setAlignment(Qt.AlignCenter)

        label = QLabel(window)
        label.setIndent(1)
        label.setAlignment(Qt.AlignLeft)
        # The first component displays objective function name instead of "+".
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

        for sle_con in self.constraint_col:
            sle_con.update_var_label(current_text)

    def get_name(self) -> str:
        """
        Returns
        ---
        str
            The value of the name_field's edit field. Used for solution table labeling.
        """
        return self.name_field.text()


class SLECon(SLineEdit):
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
        SLineEdit.__init__(self, window, layout, row_index, col_index)
        # Text displayed will be connected to SLEVar name_field.
        self.var_label = QLabel(window)
        self.var_label.setIndent(1)

        label = QLabel(window)
        label.setIndent(1)
        label.setAlignment(Qt.AlignLeft)
        sub = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        # Label will be "+" if not the first in a row, otherwise it will be constraint number label.
        label_text = f"C{row_index}:".translate(sub) if col_index == 0 else "+"
        label.setText(label_text)

        # Add these in the order in which they should appear in app.
        self.widgets.append(label)
        self.widgets.append(self)
        self.widgets.append(self.var_label)
        self.add()

    def update_var_label(self, new_name: str) -> None:
        """Sets the variable name label to the given string. Called when associated SLEVar field is updated.

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


class SLEIneq(SLineEdit):
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
        SLineEdit.__init__(self, window, layout, row_index, col_index)
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
