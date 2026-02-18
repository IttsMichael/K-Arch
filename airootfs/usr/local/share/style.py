def apply_style(widget):
    widget.setStyleSheet("""
    /* Base window - Absolute Black */
    QWidget {
        background-color: #000000; 
        color: #F8FAFC; 
        font-size: 13px;
        font-family: 'Segoe UI', 'Inter', sans-serif;
    }

    /* Global Disabled State */
    QWidget:disabled {
        color: #404040; 
    }

    /* Section titles - Electric Crystal Blue */
    QLabel[sectionTitle="true"] {
        font-size: 19px;
        font-weight: bold;
        color: #00BAFF;
        padding-bottom: 4px;
        border-bottom: 1px solid #1A1A1A; /* Subtle separator */
    }
    
    QLabel[sectionTitle="true"]:disabled {
        color: #262626;
    }

    /* Normal labels */
    QLabel {
        color: #A3A3A3; 
    }

    /* Buttons - High-Contrast Crystal Blue */
    QPushButton {
        background-color: #0082FF;
        border: 1px solid #0056B3;
        color: #FFFFFF; 
        font-weight: bold;
        padding: 8px 16px;
        border-radius: 5px;
    }

    QPushButton:hover {
        background-color: #339AFF;
        border-color: #00BAFF;
    }

    QPushButton:pressed {
        background-color: #0056B3;
    }

    QPushButton:disabled {
        background-color: #121212;
        border: 1px solid #1A1A1A;
        color: #404040;
    }

    /* Inputs - Pitch Black with Thin Borders */
    QComboBox, QSpinBox, QLineEdit {
        background-color: #000000;
        border: 1px solid #262626;
        padding: 6px;
        border-radius: 4px;
        color: #FFFFFF;
    }

    QComboBox:hover, QLineEdit:focus {
        border-color: #00BAFF;
    }

    /* Checkboxes */
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border-radius: 4px;
        border: 1px solid #333333;
        background-color: #000000;
    }

    QCheckBox::indicator:checked {
        background-color: #0082FF;
        border-color: #00BAFF;
        image: url("data:image/svg+xml;utf8,\
            <svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'>\
                <path fill='white' d='M6.2 11.2L3.3 8.3l1.1-1.1 1.8 1.8 4.3-4.3 1.1 1.1z'/>\
            </svg>");
    }

    /* Progress bar - Ultra Sharp Gradient */
    QProgressBar {
        border: 1px solid #262626;
        background-color: #080808;
        height: 10px;
        text-align: center;
        border-radius: 5px;
    }

    QProgressBar::chunk {
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, \
            stop:0 #0056B3, stop:1 #00BAFF);
        border-radius: 4px;
    }

    /* Scrollbars - Minimalist Black/Blue */
    QScrollBar:vertical {
        border: none;
        background: #000000;
        width: 10px;
        margin: 0px;
    }

    QScrollBar::handle:vertical {
        background: #262626;
        min-height: 20px;
        border-radius: 5px;
    }

    QScrollBar::handle:vertical:hover {
        background: #0082FF;
    }
    """)