import os
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget


class WelcomeScreen(QDialog):
    """
    Welcome screen, the first screen that can be seen.
    The QDialog has only two buttons, one loads the NewProvingMethodConfigScreen, and the other loads
    the LoadingScreen.

    Attributes:
        __widget: Widget, that handles shown dialogs
    """

    def __init__(self, widget: QWidget) -> None:
        """
        Initializes the window. Loads the window_xmls/welcome_screen.ui file.
        Connects the functions to the buttons
        """
        super(WelcomeScreen, self).__init__()
        loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'window_xmls\\welcome_screen.ui'), self)
        self.__widget = widget

        self.new_proving_method_button.clicked.connect(self.__go_to_new_proving_method_config)
        self.load_proving_method_button.clicked.connect(self.__go_to_loading_screen)

    def __go_to_new_proving_method_config(self):
        """
        Initializes a NewProvingMethodConfigScreen and gives the focus the that new screen.
        """
        from View.new_proving_method_config_screen import NewProvingMethodConfigScreen
        new_proving_method_config = NewProvingMethodConfigScreen(self.__widget)
        self.__widget.addWidget(new_proving_method_config)
        self.__widget.setCurrentIndex(self.__widget.currentIndex() + 1)

    def __go_to_loading_screen(self) -> None:
        """
        Initializes a LoadingScreen and gives the focus the that new screen.
        """
        from View.loading_screen import LoadingScreen
        loading_screen = LoadingScreen(self.__widget)
        self.__widget.addWidget(loading_screen)
        self.__widget.setCurrentIndex(self.__widget.currentIndex() + 1)
