import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

from View.welcome_screen import WelcomeScreen
from View.proving_method_screen import ProvingMethodScreen


class LoadingScreen(QDialog):
    """
    LoadingScreen QDialog handles the saves. Gives opportunity to load proving methods, that saved before.
    Lists all saves in a scroll area.

    Attributes:
        __widget: Widget, that handles shown dialogs
        __data: (list of tuples) list of files' full path and tasks' name
        __vbox: (QVBoxLayout) vertical layouts for buttons
        __button_widget: (QWidget) widget for vbox
        __scroll_area: (QScrollArea) scroll area shown in the window, contains button_widget

    """

    def __init__(self, widget: QtWidgets) -> None:
        """
        Initialize the LoadingScreen.
        """
        super(LoadingScreen, self).__init__()
        self.__widget = widget
        self.__scroll_area = None
        self.__button_widget = None
        self.__vbox = None
        self.__data = None
        self.__init_ui()

    def __init_ui(self) -> None:
        """
        Initialize the variables in constructor. Lists all saves from Persistence.Saves
        Shows a list of buttons, buttons' text represents the datetime and task name.
        Every button binded to a save, if the user presses it, then the try_load_model function executed
        """
        from Persistence.data_access import DataAccess
        from View.Utils.utils import text_formatter
        data_access = DataAccess()
        self.__scroll_area = QtWidgets.QScrollArea()
        self.__button_widget = QtWidgets.QWidget()
        self.__vbox = QtWidgets.QVBoxLayout()
        self.__data = list(data_access.model_list())
        for elem in self.__data:
            horizontal_box = QtWidgets.QHBoxLayout()

            elem = list(elem)
            button = QtWidgets.QPushButton()
            task = elem[1]
            task = task.replace('|-', ';')
            task = text_formatter(task)
            task = task.replace(';', '|-')
            button.setText(task)
            button.clicked.connect(lambda _, path=elem[0]: self.__try_load_model(path))
            horizontal_box.addWidget(button)

            del_button = QtWidgets.QPushButton()
            del_button.setText('Delete')
            del_button.clicked.connect(lambda _, path=elem[0]: self.__delete_save(path))
            del_button.setFixedWidth(60)
            horizontal_box.addWidget(del_button)
            self.__vbox.addLayout(horizontal_box)

        button = QtWidgets.QPushButton()
        button.setText('Back')
        button.clicked.connect(self.__go_to_welcome)
        self.__vbox.addWidget(button)

        self.__button_widget.setLayout(self.__vbox)
        self.__scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.__scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__scroll_area.setWidgetResizable(True)
        self.__scroll_area.setWidget(self.__button_widget)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.__scroll_area)
        self.setLayout(main_layout)

        self.setGeometry(400, 400, 400, 400)

    def __go_to_welcome(self) -> None:
        """
        Initializes a WelcomeScreen and gives the focus the that new screen.
        """
        welcome_screen = WelcomeScreen(self.__widget)
        self.__widget.addWidget(welcome_screen)
        self.__widget.setCurrentIndex(self.__widget.currentIndex() + 1)

    def __try_load_model(self, path: str) -> None:
        """
        Tries to load a new ProvingMethodScreen. Uses the save_loading_window and saves the path of the file
        to be loaded.
        Tries to load the file, and initialize a new model object. If loading was successful the window gives
        the focus to a new ProvingMethodScreen. Otherwise, the focus stays and a message box shows up.

        Args:
            path: full path to a saved file in the Persistence.Saves
        """
        from Persistence.data_access import DataAccess
        try:
            data_access = DataAccess()
            data_access.save_loading_window(path)
            proving_method_screen = ProvingMethodScreen(self.__widget)
            proving_method_screen.init_model_with_loaded_config()
            self.__widget.addWidget(proving_method_screen)
            self.__widget.setCurrentIndex(self.__widget.currentIndex() + 1)
        except (OSError, ValueError):
            msg_box = QtWidgets.QMessageBox()
            msg_box.setWindowTitle('Warning')
            msg_box.setText("Can't load the file!")
            msg_box.exec_()

    def __delete_save(self, path: str) -> None:
        try:
            os.remove(path)
        except OSError:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setWindowTitle('Warning')
            msg_box.setText("Can't delete the save!")
            msg_box.exec_()
        loading_screen = LoadingScreen(self.__widget)
        self.__widget.addWidget(loading_screen)
        self.__widget.setCurrentIndex(self.__widget.currentIndex() + 1)
