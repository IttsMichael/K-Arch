def apply_style(widget):
    widget.setStyleSheet("""
    /* Base window - Neutral Slate Charcoal */
    QWidget {
        background-color: #1C1E20; 
        color: #F5F9FF; /* Snow White text */
        font-size: 13px;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Section titles - Sky Blue */
    QLabel[sectionTitle="true"] {
        font-size: 18px;
        font-weight: bold;
        color: #91C8F6;
        padding-bottom: 5px;
    }

    /* Normal labels */
    QLabel {
        color: #D1D5DB; /* Neutral light grey */
    }

    /* Buttons - Meadow Green */
    QPushButton {
        background-color: #7FB845;
        border: none;
        color: #1A2E26; 
        font-weight: bold;
        padding: 8px 16px;
        border-radius: 6px;
    }

    QPushButton:hover {
        background-color: #96D156;
    }

    QPushButton:pressed {
        background-color: #91C8F6; /* Sky Blue on click */
        color: #1A2E26;
    }

    /* Inputs - Dark Neutral */
    QComboBox, QSpinBox, QLineEdit {
        background-color: #111214;
        border: 1px solid #374151;
        padding: 5px;
        border-radius: 4px;
        color: #F5F9FF;
    }

    QComboBox:hover, QLineEdit:focus {
        border-color: #91C8F6;
    }

    /* Checkboxes - Matched to Meadow Green */
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border-radius: 4px;
        border: 1px solid #374151;
        background-color: #111214;
    }

    QCheckBox::indicator:checked {
        background-color: #7FB845; /* Meadow Green - Matches Buttons */
        border-color: #7FB845;
        image: url("data:image/svg+xml;utf8,\
            <svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'>\
                <path fill='%231C1E20' d='M6.2 11.2L3.3 8.3l1.1-1.1 1.8 1.8 4.3-4.3 1.1 1.1z'/>\
            </svg>");
    }

    /* Progress bar - Gradient from Meadow to Sky */
    QProgressBar {
        border: 1px solid #374151;
        background-color: #111214;
        height: 14px;
        text-align: center;
        border-radius: 7px;
    }

    QProgressBar::chunk {
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, \
            stop:0 #7FB845, stop:1 #91C8F6);
        border-radius: 5px;
    }
    """)