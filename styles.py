"""Style sheet themes for Simplex Calculator.
"""

def replace_colors(style: str, color_map: dict) -> str:
    """Replaces color variable names in a PyQt style sheet (multi-line string) with hexidecimal color values.

    Parameters
    ---
    style: string
        Must be properly formatted as a PyQt style sheet
        https://doc.qt.io/qtforpython/overviews/stylesheet-examples.html
    color_map: dictionary
        Used to replace variable names with hexidecimal values

    Returns
    ---
    str
        A style sheet string for PyQt widget.
    """
    for key, val in color_map.items():
        style = style.replace(key, val)
    return style


light_map = {
    "bg_prime": "#F0F0F0",
    "bg_sub": "#FFFFFF",
    "text_color_prime": "#000000",
    "text_color_sub": "#525252",
    "border_prime": "#B9B9B9",
    "border_sub": "#B9B9B9",
    "button_select": "#F0F0F0",
    "icon-select": "#D9D9D9",
    "focus_color": "#FFFFFF"
}

dark_map = {
    "bg_prime": "#353535",
    "bg_sub": "#292929",
    "text_color_prime": "#FFFFFF",
    "text_color_sub": "#BBBBBB",
    "border_prime": "#353535",
    "border_sub": "#292929",
    "button_select": "#353535",
    "icon-select": "#424242",
    "focus_color": "#292929"
}

        # font-size: 16px;

SIMPLEX_STYLE_SHEET = ("""
    QWidget {
        background: bg_prime;
        color: text_color_prime;
    }

    QPushButton:pressed {
        background-color: button_select;
    }

    SSettingsButton {
        border: none;
        background-color: bg_prime;
    }

    SSettingsButton:pressed {
        background-color: icon-select;
    }

    SSettingsButton:focus {
        background-color: focus_color;
    }

    SLabelSetting {
        color: text_color_sub;
    }

    SCircleButton {
        icon-size: 25px;
        border-radius: 20px;
        width: 40px;
        height: 40px;
    }

    SCircleButton:focus {
        background-color: focus_color;
    }

    SCircleButton:pressed {
        background-color: icon-select;
    }

    QLineEdit {
        background: bg_sub;
    }

    SLabelSolve {
        padding: 4px;
        border: 1px solid text_color_prime;
    }

    QScrollArea {
        border: none;
        background: bg_prime;
    }

    QScrollBar:horizontal {
        height: 15px;
        border: none;
    }

    QScrollBar:vertical {
        width: 15px;
        border: none;
    }

    QScrollBar::handle {
        background: bg_sub;
        border: 1px solid border_sub;
    }

    QScrollBar::add-page, QScrollBar::sub-page {
        background: bg_prime;
        border: 1px solid border_sub;
    }
""")

SIMPLEX_STYLE_LIGHT = replace_colors(SIMPLEX_STYLE_SHEET, light_map)
SIMPLEX_STYLE_DARK = replace_colors(SIMPLEX_STYLE_SHEET, dark_map)

SIMPLEX_ICON_LIGHT = "#323232"
SIMPLEX_ICON_DARK = "#F0F0F0"
