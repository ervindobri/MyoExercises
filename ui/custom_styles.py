class CustomQStyles:
    pressedKeyButtonStyle = """ QPushButton
                    {
                        border: 1px solid green;
                        background-color: #7FFFD4;
                        border-radius: 7px;
                        margin: 5px;
                    }
                    """
    keyButtonStyle = """ QPushButton
            {
                border: 1px solid grey;
                background-color: white;
                border-radius: 7px;
                margin: 5px;
            }
            """
    timerStyle = """
        QTimeEdit
        {
            background-color: #20c1dc;
            border-radius: 7px;
            color: white;
            font-weight: bold;
            text-align: center;
        }
        QTimeEdit::down-button{
            width: 0;
        }
        QTimeEdit::up-button{
            width: 0;
        }
        
    """
    blue = "#00bbde"
    lightBlue = "#a0f1ff"

    comboStyle = """
            QWidget
            {
                background-color: white;
                border: 1px solid #20c1dc;
                border-radius: 7px;
                font-size: 12px;
            }
        """

    tabStyle = """
            QTabWidget {background-color: white; border: none;}
            QTabWidget::pane {
             border: none;
                background: white;
                border-top: 1px solid #bebebe;
              }
            QTabBar {background-color: white;}
            QTabBar::tab:selected
            {
                color: #454545;
                background-color: white;
                font-weight: bold;    
                border-bottom: 4px solid #20c1dc;
            }
            QTabBar::tab
            {
                color: #bebebe;
                background-color: white;
                font-size: 13px;
                width: 50px;   
                text-align: left; 
            }
        """

    listStyle = """
        QListView::item
        {
            background-color: white;
            margin: 3px;
        }
        QListView::item::selected
        {
            background-color: white;
            border: 1px solid #00bbde;
            border-radius: 7px;
            margin: 3px;
            color: #00bbde;
        }
    """
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
