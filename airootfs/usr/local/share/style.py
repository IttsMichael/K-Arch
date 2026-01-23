def apply_style(widget):
    widget.setStyleSheet("""
    /* Base window */
    QWidget {
        background-color: #0f1115;
        color: #e6e6e6;
        font-size: 12px;
    }

    /* Section titles */
    QLabel[sectionTitle="true"] {
        font-size: 15px;
        font-weight: bold;
        color: #ffffff;
        padding-bottom: 4px;
    }

    /* Normal labels */
    QLabel {
        color: #e6e6e6;
    }

    /* Buttons */
    QPushButton {
        background-color: #1b1f27;
        border: 1px solid #2b2f38;
        padding: 6px 14px;
        border-radius: 4px;
    }

    QPushButton:hover {
        background-color: #232834;
        border-color: #1793d1; /* Arch blue */
    }

    QPushButton:pressed {
        background-color: #1793d1;
        color: #ffffff;
    }

    QPushButton:disabled {
        background-color: #16181d;
        color: #777777;
        border-color: #222222;
    }

    /* Inputs */
    QComboBox, QSpinBox, QLineEdit {
        background-color: #16181d;
        border: 1px solid #2b2f38;
        padding: 4px 6px;
        border-radius: 4px;
        selection-background-color: #1793d1;
        selection-color: #ffffff;
    }

    QComboBox:hover, QSpinBox:hover, QLineEdit:hover {
        border-color: #1793d1;
    }

    QComboBox::drop-down {
        border: none;
    }

    /* Dropdown list */
    QComboBox QAbstractItemView {
        background-color: #16181d;
        border: 1px solid #2b2f38;
        selection-background-color: #1793d1;
        selection-color: #ffffff;
    }

    /* Checkboxes */
    QCheckBox {
        spacing: 8px;
    }

    QCheckBox::indicator {
        width: 16px;
        height: 16px;
        border-radius: 3px;
        border: 1px solid #2b2f38;
        background-color: #16181d;
    }

    QCheckBox::indicator:hover {
        border-color: #1793d1;
    }

    QCheckBox::indicator:checked {
        background-color: #1793d1;
        border-color: #1793d1;
        image: url("data:image/svg+xml;utf8,\
            <svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'>\
                <path fill='white' d='M6.2 11.2L3.3 8.3l1.1-1.1 1.8 1.8 4.3-4.3 1.1 1.1z'/>\
            </svg>");
    }

    QCheckBox::indicator:disabled {
        background-color: #111318;
        border-color: #222222;
    }


    /* Progress bar */
    QProgressBar {
        border: 1px solid #2b2f38;
        background-color: #16181d;
        height: 16px;
        text-align: center;
    }

    QProgressBar::chunk {
        background-color: #1793d1;
    }
    """)
