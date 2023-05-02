from util.resources_path import resource_path


BLUE_STYLE = f'''

QFrame{{
    background-color: white
}}

QLabel{{
    color: black;
    font-family: Arial;
    font-weight: bold;
    font: 10pt;
}}

QLineEdit, QPlainTextEdit{{
    background: white;
    border: 2px solid rgb(91, 131, 247);
    border-radius: 10px;
    font-family: Arial;
    padding: 3px;
    font-weight: bold;
    font: 8pt;
}}

QLineEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus, QComboBox:focus{{
    border: 2px solid rgb(190, 19, 240);
    background: rgb(231, 237, 254);
}}

QPushButton{{
    border-style: none;
    padding: 11px;
    border-radius: 10px;
    background-color: rgb(27, 88, 241);
    font-weight: bold;
    color: white;
}}

QPushButton#dialog_delete_button{{
    background-color: #CE2412;
}}

QPushButton#dialog_delete_button:hover{{
    background-color: #CE7562;
}}

QPushButton:hover{{
    background-color: rgb(115, 151, 247);
}}

QPushButton:disabled{{
    background-color: #908C9E;
}}

QPushButton:pressed{{
    background-color: rgb(180, 33, 255);
}}

/*-----------------Personalizando QSpinBox, QDoubleSpinBox, QDateEdit, QComboBox-----------------------*/
QSpinBox, QDoubleSpinBox, QDateEdit, QComboBox, QLineEdit, QPlainTextEdit {{
    
    background: white;
    border: 2px solid rgb(91, 131, 247);
    font-family: Arial;
    font: 10pt;
    border-radius: 10px;
    height: 25px;
    width: 150px;
}}

QComboBox QAbstractItemView
{{
    selection-color: black;
    background-color: rgb(231, 237, 254);
}}

QSpinBox::up-button, QDoubleSpinBox::up-button, QDateEdit::up-button{{
    subcontrol-origin: border;
    subcontrol-position: top right; /* position at the top right corner */

    width: 16px;
    height: 16px;
    background-color: blue;
    image: url("{resource_path("view/ui/images/up_arrow.png")}");
    margin-right: 0.5em;
}}

QSpinBox::down-button, QDoubleSpinBox::down-button, QDateEdit::down-button{{
    subcontrol-origin: border;
    subcontrol-position: bottom right; /* position at the top right corner */


    width: 16px;
    height: 16px;
    image: url("{resource_path("view/ui/images/down_arrow.png")}");
    margin-right: 0.5em;
}}

QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover, QDateEdit::up-button:hover {{
    image: url("{resource_path("view/ui/images/hovered_up_arrow.png")}");
}}

QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed, QDateEdit::up-button:pressed {{
    image: url("{resource_path("view/ui/images/pressed_up_arrow.png")}");
}}

QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover, QDateEdit::down-button:hover,
QDateEdit::drop-down:hover, QComboBox::drop-down:hover {{
    image: url("{resource_path("view/ui/images/hovered_down_arrow.png")}");
}}

QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed, QDateEdit::down-button:pressed,
QDateEdit::drop-down:pressed, QComboBox::drop-down:pressed{{
    image: url("{resource_path("view/ui/images/pressed_down_arrow.png")}");
}}

QSpinBox:disabled, QDoubleSpinBox:disabled, QDateEdit:disabled, QComboBox:disabled,
QLineEdit:disabled, QPlainTextEdit:disabled{{
    background-color: #908C9E;
    border: 2px solid #908C9E;
    color: white;
}}

QSpinBox::down-button:disabled, QDoubleSpinBox::down-button:disabled, QDateEdit::down-button:disabled,
QDateEdit::drop-down:disabled, QComboBox::drop-down:disabled{{
    image: url("{resource_path("view/ui/images/disabled_down_arrow.png")}");
}}

QSpinBox::up-button:disabled, QDoubleSpinBox::up-button:disabled, QDateEdit::up-button:disabled,
QDateEdit::drop-up:disabled{{
    image: url("{resource_path("view/ui/images/disabled_up_arrow.png")}");
}}

QComboBox::drop-down, QDateEdit::drop-down{{
    subcontrol-origin: border;
    subcontrol-position: bottom right; /* position at the top right corner */


    width: 28px;
    height: 28px;
    image: url("{resource_path("view/ui/images/down_arrow.png")}");
    margin-right: 0.3em;
    margin-left: 0;
}}



/*---------------------------------------------------------------------*/

/***************Headers de la vista principal*******************************/
QLabel#management_label, QLabel#reports_label, QLabel#statistics_label {{
    color: black;
    font-family: Arial;
    font-weight: bold;
    font: 28pt;
}}

/***************************************************************************/





/**********************QCheckBox********************************************/

QCheckBox::indicator {{
    width: 30px;
    height: 20px;
}}


QCheckBox::indicator:unchecked {{
    image: url("{resource_path("view/ui/images/unchecked.png")}");
}}

QCheckBox::indicator:checked {{
    image: url("{resource_path("view/ui/images/checked.png")}");
}}
/***************************************************************************/






/*****************QRadioButton**********************************************/
QRadioButton::indicator {{
    width: 1em;
    height: 1em;
}}

QRadioButton::indicator::unchecked {{
    image: url("{resource_path("view/ui/images/unchecked_radio.png")}");
}}

QRadioButton::indicator::checked {{
    image: url("{resource_path("view/ui/images/checked_radio.png")}");
}}

QRadioButton{{
    color: black;
    font-family: Arial;
    font-weight: bold;
    font: 10pt;
}}
/***************************************************************************/





/*****************QGroupBox*************************************************/
QGroupBox {{
    margin-top: 1em;
    border: 2px solid rgb(91, 131, 247);
    border-radius: 10px;
    color: black;
    font-family: Arial;
    font-weight: bold;
    font: 9pt;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top center; /* position at the top center */
    padding-top: 5px;
}}

/***************************************************************************/

'''