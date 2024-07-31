import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets

from View.welcome_screen import WelcomeScreen


def main() -> None:
    """
    Main function for the program. Initialize the WelcomeScreen and gives to focus to the new QDialog.
    """
    from Persistence.data_access import DataAccess
    data_access = DataAccess()
    data_access.windows_cleaner()

    app = QApplication(sys.argv)
    app.setApplicationName('Proving theory')
    widget = QtWidgets.QStackedWidget()
    welcome = WelcomeScreen(widget)
    widget.addWidget(welcome)
    widget.setFixedWidth(1200)
    widget.setFixedHeight(800)
    widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
