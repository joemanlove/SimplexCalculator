"""Style sheet themes for Simplex Calculator.
"""

def replace_colors(style: str, color_map: dict) -> str:
    """Replaces color variable names in a PyQt style sheet string with hexidecimal color values.

    Parameters
    ---
    style: string
        Must be properly formatted as a PyQt style sheet
        https://doc.qt.io/qtforpython/overviews/stylesheet-examples.html
    color_map: dictionary
        Used to replace variable names with hexidecimal values
    """
    for key, val in color_map.items():
        style = style.replace(key, val)
    return style

dark_map = {
    "bg_prime": "#353535",
    "bg_sub": "#292929",
    "text_color": "#FFFFFF",
    "border_prime": "#353535",
    "border_sub": "#292929",
    "button_select": "#353535",
}

light_map = {
    "bg_prime": "#F0F0F0",
    "bg_sub": "#FFFFFF",
    "text_color": "#000000",
    "border_prime": "#B9B9B9",
    "border_sub": "#B9B9B9",
    "button_select": "#F0F0F0",
}

SIMPLEX_STYLE_SHEET = ("""
    QWidget {
        background: bg_prime;
        color: text_color;
    }

    QPushButton:pressed {
        background-color: button_select;
    }

    QLineEdit {
        background: bg_sub;
    }

    QLabelSimplex {
        padding: 4px;
        border: 1px solid text_color;
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
