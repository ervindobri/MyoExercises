class CustomQStyles:


    blue = "#00bbde"
    lightBlue = "#a0f1ff"

    lineEditStyle = """
        QLineEdit
        {
            background-color: white;
            border: 1px solid #00bbde;
            border-radius: 7px;
        }
    """
    buttonStyle = """
        QPushButton
        {
            background-color: #00bbde;
            color: white;
            font-weight: bold;
            border-radius: 7px;
        }
        QPushButton:hover
        {
            background-color: #01a6c3;
            color: white;
            font-weight: bold;
            border-radius: 7px;
        }
        QPushButton:pressed
        {
            background-color: #00a5c3;
            color: white;
            font-weight: bold;
            border-radius: 7px;
        }
        
    """
    outlineButtonStyle = """
        QPushButton
        {
            background-color: white;
            border: 1px solid #00bbde;
            border-radius: 7px;
            color: #00bbde;
            font-weight: bold;
        }
        QPushButton:hover
        {
            background-color: #a0f1ff;
            border: 1px solid #00bbde;
            color: white;
            font-weight: bold;
            border-radius: 7px;
        }
    """
    recordButtonStyle = """
        QPushButton
        {
            background-color: #00bbde;
            border: 1px solid red;
            color: white;
            font-weight: bold;
            border-radius: 7px;
        }"""