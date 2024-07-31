import os

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from Model.model import Model
from Model.actions import Actions
from Model.task_is_not_provable_exception import TaskIsNotProvableException
from Model.formula_in_steps_exception import FormulaInStepsException

from View.welcome_screen import WelcomeScreen
from View.hyp_dialog import HypDialog
from View.axiom_dialog import AxiomDialog
from View.help_dialog import HelpDialog


class ProvingMethodScreen(QDialog):
    """
    Represents the proving method for users. Shows the task (formula set and consequence formula), the base axioms, that
    built in. Shows the steps that completed by the user. Action buttons placed on the screen, such as:
        HYP - uses hypothesis from proving method
        AXIOM - uses axioms and substitute given formulas form user to the axiom
        MP - use the modus ponens detaching rule to the two steps given by user
        MT - use the modus tollens detaching rule to the two steps given by user
        MTP - use the modus tollendo ponens detaching rule to the two steps given by user
        MPT - use the modus ponendo tollens detaching rule to the two steps given by user
        CS - use the conditional syllogism rule to the two steps given by user
        HINT - gives hint for using syntax rule if possible
        ADD AXIOM - user can add an axiom, it is only added if the formula is a real axiom
        USE ADDED AXIOM - use added axiom, if the user added at all
        DELETE LINES - delete steps if the user want to
        SAVE - save the current proving method
        HOME - go to the welcome screen

    Attributes:
        __widget: Widget, that handles shown dialogs
        __proving_method_layout (QVBoxLayout): vertical layout contains the steps of the proving method
        __axiom_layout (QVBoxLayout): vertical contain contains the task and the base axioms
        __actions_layout (QHBoxLayout): horizontal layout contains the action buttons (hyp, axiom, help)
        __actions_2_layout (QHBoxLayout): horizontal layout contains the action buttons (mp, mt, mtp, mpt, cs)
        __additions_layout (QHBoxLayout): horizontal layout contains the addition actions (hint, add axioms, use added
            axioms, delete lines)
        __outer_layout (QGridLayout): grid layout that contains tha axioms, actions, additions, proving_method layouts
            and the save, home buttons
        __model (Model): handles proving method logic

    """

    def __init__(self, widget: QtWidgets.QWidget) -> None:
        """
        Initialize the ProvingMethodScreen using the window_xmls\\proving_method_screen.ui xml file.
        Initialize the layouts, and the buttons on the screen.

        Args:
            widget: QWidget handles screen changing.
        """
        super(ProvingMethodScreen, self).__init__()
        loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'window_xmls\\proving_method_screen.ui'), self)
        self.setWindowTitle('Proving method')
        self.__widget = widget

        self.__outer_layout = QtWidgets.QGridLayout()
        self.__axiom_layout = QtWidgets.QVBoxLayout()
        self.__actions_layout = QtWidgets.QHBoxLayout()
        self.__actions_2_layout = QtWidgets.QHBoxLayout()
        self.__additions_layout = QtWidgets.QHBoxLayout()
        self.__proving_method_layout = QtWidgets.QVBoxLayout()
        self.__proving_method_layout_next_prev_buttons = QtWidgets.QHBoxLayout()

        self.__home_button = QtWidgets.QPushButton('Home')
        self.__home_button.setFont(QtGui.QFont("MS Shell Dlg 2", weight=QtGui.QFont.Bold))
        self.__home_button.clicked.connect(self.__go_to_welcome)
        self.__save_button = QtWidgets.QPushButton('Save')
        self.__save_button.setFont(QtGui.QFont("MS Shell Dlg 2", weight=QtGui.QFont.Bold))
        self.__save_button.clicked.connect(self.__save_model)

        self.__hyp_action_button = QtWidgets.QPushButton('HYP')
        self.__axiom_action_button = QtWidgets.QPushButton('AXIOM')
        self.__help_button = QtWidgets.QPushButton('HELP')
        self.__mp_action_button = QtWidgets.QPushButton('MP')
        self.__mt_action_button = QtWidgets.QPushButton('MT')
        self.__mtp_action_button = QtWidgets.QPushButton('MTP')
        self.__mpt_action_button = QtWidgets.QPushButton('MPT')
        self.__cs_action_button = QtWidgets.QPushButton('CS')
        self.__hint_button = QtWidgets.QPushButton('HINT')
        self.__add_axiom_button = QtWidgets.QPushButton('ADD AXIOM')
        self.__use_added_axiom_button = QtWidgets.QPushButton('USE ADDED AXIOM')
        self.__delete_lines_button = QtWidgets.QPushButton('DELETE LINES')
        self.__next_button = QtWidgets.QPushButton('NEXT')
        self.__prev_button = QtWidgets.QPushButton('PREV')
        self.__current_proving_method_layout = 0
        self.__model = None

    def init_model_with_new_config(self) -> None:
        """
        Tries to make a model object. Reads saving_new_proving_method_config file that contains
        necessary data for a new model object. If constructing a new model was successful, then shows the layout's data
        and places them in the outer layout.


        Raises:
            OSError: if the file reading was not successful
            ValueError: if the input was not successful
        """
        from Model.Utils.utils import Utils
        try:
            formulas = Utils.load_new_proving_method_config()
        except OSError:
            raise OSError
        except ValueError:
            raise ValueError

        try:
            self.__model = Model(formula_set=list(set(formulas[0])), consequence_formula=formulas[1])
        except ValueError:
            raise ValueError

        if not self.__model.task_is_provable():
            message_box = QtWidgets.QMessageBox()
            message_box.setIcon(QtWidgets.QMessageBox.Question)
            message_box.setWindowTitle('Task is not provable')
            message_box.setText('Do you want to continue?')
            message_box.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            result = message_box.exec_()
            if result == QtWidgets.QMessageBox.Cancel:
                raise TaskIsNotProvableException()

        if self.__model.formula_set_contains_tautology():
            message_box = QtWidgets.QMessageBox()
            message_box.setIcon(QtWidgets.QMessageBox.Question)
            message_box.setWindowTitle('Axiom(s) in the formula set!')
            message_box.setText('Do you want to delete them?')
            message_box.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            result = message_box.exec_()
            if result == QtWidgets.QMessageBox.Ok:
                self.__model.delete_tautologies()

        self.__initialize_layouts()

    def init_model_with_loaded_config(self) -> None:
        """
        Tries to load and make a model object. Get a file path with load_loading_window function, and gets the
        necessary data for a new model object. If constructing a new model was successful, then shows the layout's data
        and places them in the outer layout.

        Raises:
            OSError: if the file reading was not successful
            ValueError: if the input was not successful
        """
        from Persistence.data_access import DataAccess
        try:
            data_access = DataAccess()
            path = data_access.load_loading_window()
        except OSError:
            raise OSError
        except ValueError:
            raise ValueError

        try:
            self.__model = Model(file_path=path)
        except ValueError:
            raise ValueError

        self.__initialize_layouts()

    def __initialize_layouts(self):
        """
        Sets all layouts and widgets on the outer layout.
        Executes the __set_proving_method function.
        If the proving has ended, the task's color set red.
        """
        self.__show_model_data()
        self.__set_model_actions()
        self.__outer_layout.addLayout(self.__axiom_layout, 0, 0)
        self.__outer_layout.addWidget(self.__home_button, 1, 0)
        self.__outer_layout.addWidget(self.__save_button, 1, 1)
        self.__outer_layout.addLayout(self.__proving_method_layout, 0, 1)
        self.__set_proving_method_layout()
        self.setLayout(self.__outer_layout)

        if self.__model.end:
            self.__axiom_layout.itemAt(0).widget().setStyleSheet('color:Red')

    def __go_to_welcome(self) -> None:
        """
        Initializes a WelcomeScreen and gives the focus the that new screen.
        """
        welcome_screen = WelcomeScreen(self.__widget)
        self.__widget.addWidget(welcome_screen)
        self.__widget.setCurrentIndex(self.__widget.currentIndex() + 1)

    def __show_model_data(self) -> None:
        """
        Sets the axiom layout. Shows the task, the base axioms as a label.
        """
        from View.Utils.utils import text_formatter
        task = self.__model.get_formula_set_consequence_concat()
        task = task.replace('|-', ';')
        task = text_formatter(task)
        task = task.replace(';', '|-')
        if len(task) > 40:
            task_members = task.split('|-')
            if len(task_members[0]) <= 40:
                task = task.replace('|-', '\n|-')
            else:
                formula_set_members = task_members[0].split(',')
                full_task = ''
                current_task = ''
                for formula in formula_set_members:
                    if len(current_task + formula + ',') < 40:
                        current_task = current_task + formula + ','
                    else:
                        full_task = full_task + current_task + '\n'
                        current_task = formula + ','
                if current_task != '':
                    full_task = full_task + current_task[:-1]
                task = full_task + '|-' + task_members[1]
                task = task.replace('|-', '\n|-')
        label = QtWidgets.QLabel('Task: ' + task)
        label.setFont(QtGui.QFont("MS Shell Dlg 2", 14))
        if len(task) < 200:
            label.setFont(QtGui.QFont("MS Shell Dlg 2", 14))
        else:
            label.setFont(QtGui.QFont("MS Shell Dlg 2", 10))
        label.setStyleSheet('color:white')
        self.__axiom_layout.addWidget(label)
        label = QtWidgets.QLabel('Axioms:')
        label.setFont(QtGui.QFont("MS Shell Dlg 2", 12))
        label.setStyleSheet('color:white')
        self.__axiom_layout.addWidget(label)
        for idx, axiom in enumerate(self.__model.base_axioms):
            label = QtWidgets.QLabel(str(str(idx + 1) + '. ' + text_formatter(axiom)))
            label.setFont(QtGui.QFont("MS Shell Dlg 2", 10))
            label.setStyleSheet('color:white')
            self.__axiom_layout.addWidget(label)

    def __set_model_actions(self) -> None:
        """
        Adds all buttons to their layouts, and sets their clicked property.
        """
        self.__actions_layout.addWidget(self.__hyp_action_button)
        self.__hyp_action_button.clicked.connect(self.__hyp_button_action)
        self.__hyp_action_button.setFont(QtGui.QFont("MS Shell Dlg 2", weight=QtGui.QFont.Bold))

        self.__actions_layout.addWidget(self.__axiom_action_button)
        self.__axiom_action_button.clicked.connect(self.__axiom_button_action)
        self.__axiom_action_button.setFont(QtGui.QFont("MS Shell Dlg 2", weight=QtGui.QFont.Bold))

        self.__actions_layout.addWidget(self.__help_button)
        self.__help_button.clicked.connect(self.__get_help)
        self.__help_button.setFont(QtGui.QFont("MS Shell Dlg 2", weight=QtGui.QFont.Bold))

        self.__actions_2_layout.addWidget(self.__mp_action_button)
        self.__mp_action_button.clicked.connect(self.__mp_button_action)
        self.__mp_action_button.setFont(QtGui.QFont("MS Shell Dlg 2", weight=QtGui.QFont.Bold))

        self.__actions_2_layout.addWidget(self.__mt_action_button)
        self.__mt_action_button.clicked.connect(self.__mt_button_action)
        self.__mt_action_button.setFont(QtGui.QFont("MS Shell Dlg 2", weight=QtGui.QFont.Bold))

        self.__actions_2_layout.addWidget(self.__mtp_action_button)
        self.__mtp_action_button.clicked.connect(self.__mtp_button_action)
        self.__mtp_action_button.setFont(QtGui.QFont("MS Shell Dlg 2", weight=QtGui.QFont.Bold))

        self.__actions_2_layout.addWidget(self.__mpt_action_button)
        self.__mpt_action_button.clicked.connect(self.__mpt_button_action)
        self.__mpt_action_button.setFont(QtGui.QFont("MS Shell Dlg 2", weight=QtGui.QFont.Bold))

        self.__actions_2_layout.addWidget(self.__cs_action_button)
        self.__cs_action_button.clicked.connect(self.__cs_button_action)
        self.__cs_action_button.setFont(QtGui.QFont("MS Shell Dlg 2", weight=QtGui.QFont.Bold))

        self.__additions_layout.addWidget(self.__hint_button)
        self.__hint_button.clicked.connect(self.__hint_action)
        self.__hint_button.setFont(QtGui.QFont("MS Shell Dlg 2", weight=QtGui.QFont.Bold))

        self.__additions_layout.addWidget(self.__add_axiom_button)
        self.__add_axiom_button.clicked.connect(self.__add_axiom_button_action)
        self.__add_axiom_button.setFont(QtGui.QFont("MS Shell Dlg 2", weight=QtGui.QFont.Bold))

        self.__additions_layout.addWidget(self.__use_added_axiom_button)
        self.__use_added_axiom_button.clicked.connect(self.__use_added_axiom_action)
        self.__use_added_axiom_button.setFont(QtGui.QFont("MS Shell Dlg 2", weight=QtGui.QFont.Bold))

        self.__additions_layout.addWidget(self.__delete_lines_button)
        self.__delete_lines_button.clicked.connect(self.__delete_lines_button_action)
        self.__delete_lines_button.setFont(QtGui.QFont("MS Shell Dlg 2", weight=QtGui.QFont.Bold))

        self.__prev_button.clicked.connect(self.__prev_button_action)
        self.__prev_button.setFont(QtGui.QFont("MS Shell Dlg 2", weight=QtGui.QFont.Bold))

        self.__next_button.clicked.connect(self.__next_button_action)
        self.__next_button.setFont(QtGui.QFont("MS Shell Dlg 2", weight=QtGui.QFont.Bold))

        self.__proving_method_layout_next_prev_buttons.addWidget(self.__prev_button)
        self.__proving_method_layout_next_prev_buttons.addWidget(self.__next_button)

        self.__axiom_layout.addLayout(self.__actions_layout)
        self.__axiom_layout.addLayout(self.__actions_2_layout)
        self.__axiom_layout.addLayout(self.__additions_layout)

    def __set_proving_method_layout(self) -> None:
        """
        Deletes all labels int the proving_method layout. Then sets new labels, that represents the
        proving method. Sets their style.
        """
        from View.Utils.utils import text_formatter
        for i in reversed(range(self.__proving_method_layout.count())):
            try:
                self.__proving_method_layout.itemAt(i).widget().setParent(None)
                self.__proving_method_layout.itemAt(i).layout().setParent(None)
            except AttributeError:
                pass

        for i in reversed(range(self.__proving_method_layout_next_prev_buttons.count())):
            try:
                self.__proving_method_layout_next_prev_buttons.itemAt(i).widget().setParent(None)
            except AttributeError:
                pass

        self.__proving_method_layout.setAlignment(Qt.AlignTop)
        label = QtWidgets.QLabel('Proving Method:')
        label.setFont(QtGui.QFont("MS Shell Dlg 2", 14))
        label.setStyleSheet('color:white')
        self.__proving_method_layout.addWidget(label)

        if not self.__model:
            return

        current_steps = self.__model.get_steps_string()
        if not current_steps:
            return

        from_shown = 15 * self.__current_proving_method_layout
        steps = self.__model.get_steps_string()
        try:
            for index in range(from_shown, from_shown + 15):
                steps[index] = text_formatter(steps[index])
                if 100 >= len(steps[index]) > 75:
                    current = steps[index][:75] + '\n' + steps[index][75:]
                elif 100 < len(steps[index]) < 180:
                    current = steps[index][:75] + '\n' + steps[index][75:150] + '\n' + steps[index][150:]
                elif 180 <= len(steps[index]):
                    current = steps[index][:75] + '\n' + steps[index][75:150] + '\n' + steps[index][150:225] + '\n' + \
                              steps[index][225:]
                else:
                    current = steps[index]
                label = QtWidgets.QLabel(text_formatter(current))
                label.setFont(QtGui.QFont("MS Shell Dlg 2", 10))
                label.setStyleSheet('color:white')
                self.__proving_method_layout.addWidget(label)
        except IndexError:
            pass

        if len(self.__model.get_steps_string()) > 15:
            self.__proving_method_layout.addLayout(self.__proving_method_layout_next_prev_buttons)

        self.__on_end()

    def __prev_button_action(self) -> None:
        """
        If the model's steps list is more than 15 and not the first 15 steps are shown, then this
        decreases by one the current proving method layout, and shows the previous 15 step
        """
        if len(self.__model.steps) > 15:
            if self.__current_proving_method_layout > 0:
                self.__current_proving_method_layout = self.__current_proving_method_layout - 1
                self.__set_proving_method_layout()

    def __next_button_action(self) -> None:
        """
        If the model's steps list is more than 15 and not the last 15 steps are shown, then this
        increases by one the current proving method layout, and shows the next 15 step
        """
        if len(self.__model.steps) > 15:
            max_size = len(self.__model.steps) // 15
            if self.__current_proving_method_layout < max_size:
                self.__current_proving_method_layout = self.__current_proving_method_layout + 1
                self.__set_proving_method_layout()

    def __hyp_button_action(self) -> None:
        """
        If the proving method ended, then shows a message box. Otherwise, initialize a new HypDialog
        and the user can use the hypothesis. If the formula set is empty raises a message box.
        """
        if self.__model.end:
            self.__on_end_msg_box()
            return
        if self.__model.formula_set:
            hyp_dialog = HypDialog()
            hyp_dialog.add_data(self.__model)
            hyp_dialog.exec_()
            hyp = hyp_dialog.hyp
            if hyp != 'Cancel':
                self.__try_hyp(hyp)
        else:
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle('Warning!')
            message_box.setText('The formula set is empty!')
            message_box.exec_()

    def __try_hyp(self, formula: str) -> None:
        """
        Tries to execute the hypothesis rule. If it was successful the new step is added to the steps, otherwise,
        it raises a messagebox.

        Args:
            formula: logical formula, that must be in the formula set.
        """
        try:
            if self.__model.add_step(formula, Actions.HYP):
                self.__set_proving_method_layout()
            else:
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle('Warning!')
                message_box.setText('Something wrong with HYP!')
                message_box.exec_()
        except FormulaInStepsException:
            self.__on_formula_in_steps_action()

    def __axiom_button_action(self) -> None:
        """
        If the proving method ended, then shows a message box. Otherwise, initialize a new AxiomDialog
        and the user can use the base axioms. In the AxiomDialog the user can choose an axiom and the user has the
        opportunity to substitute formulas into the axiom.
        """
        if self.__model.end:
            self.__on_end_msg_box()
            return
        if self.__model.base_axioms:
            axiom_dialog = AxiomDialog()
            axiom_dialog.add_data(self.__model)
            axiom_dialog.exec_()
            data = axiom_dialog.data
            axiom = axiom_dialog.axiom
            self.__try_axiom(axiom, data)

    def __try_axiom(self, formula: str, data: list, base_axiom: bool = True) -> None:
        """
        Tries to execute the axiom rule with the axiom and substitute the data into the formula. If it was successful
        the new step is added to the steps, otherwise, it raises a messagebox.

        Args:
            formula: axiom formula
            data: list of logical formula strings, that will be substituted into the axiom
            base_axiom: using the base axioms if True, else using additional axioms.
        """
        if len(data) == 0:
            return
        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle('Warning!')
        try:
            if base_axiom:
                if self.__model.add_step(formula, Actions.AXIOM, data=data):
                    self.__set_proving_method_layout()
                else:
                    message_box.setText('Something wrong with AXIOM!')
                    message_box.exec_()
            else:
                if self.__model.action_added_axiom(formula, data):
                    self.__set_proving_method_layout()
                else:
                    message_box.setText('Something wrong with ADDED AXIOM!')
                    message_box.exec_()
        except FormulaInStepsException:
            self.__on_formula_in_steps_action()

    def __mp_button_action(self) -> None:
        """
        Calls the rule_button_action with MP Action
        """
        self.__rule_button_action(Actions.MP)

    def __mt_button_action(self) -> None:
        """
        Calls the rule_button_action with MT Action
        """
        self.__rule_button_action(Actions.MT)

    def __mtp_button_action(self) -> None:
        """
        Calls the rule_button_action with MTP Action
        """
        self.__rule_button_action(Actions.MTP)

    def __mpt_button_action(self) -> None:
        """
        Calls the rule_button_action with MPT Action
        """
        self.__rule_button_action(Actions.MPT)

    def __cs_button_action(self) -> None:
        """
        Calls the rule_button_action with CS Action
        """
        self.__rule_button_action(Actions.CS)

    def __rule_button_action(self, action: Actions) -> None:
        """
        If the proving method ended, then shows a message box. Otherwise, shows two QInputDialog
        and the user can set the 2 indexes for using modus ponens, modus tollens, affirming the consequent and denying
         the antecedent. One is the implication formulas, and the other is the
        formula, that will be detached from the formula. If the input in the dialogs are incorrect, a message box
        raised. Otherwise, call the try_rule_exec function, with the inputs.

        Args:
            action: stands for which rule will be used
        """
        if self.__model.end:
            self.__on_end_msg_box()
            return
        if action != Actions.MTP:
            implication_number, dialog_1 = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Implication number: ')
        else:
            implication_number, dialog_1 = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Disjunction number: ')
        detached_number, dialog_2 = QtWidgets.QInputDialog.getInt(self, 'Input Dialog', 'Detached number: ')

        if dialog_1 and dialog_2:
            if implication_number < 1 or detached_number < 1:
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle('Warning!')
                message_box.setText('Given numbers must be, higher than 0!')
                message_box.exec_()
            else:
                self.__try_rule_exec(implication_number, detached_number, action)
        else:
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle('Warning!')
            message_box.setText('Given inputs are incorrect!')
            message_box.exec_()

    def __try_rule_exec(self, implication_number: int, detached_number: int, action: Actions) -> None:
        """
        Tries to execute the modus ponens, modus tollens, modus ponendo tollens, modus tollendo ponens and the
        conditional syllogism rules with the implication_number and the detached_number.
        If it was successful the new step is added to the steps, otherwise, it raises a messagebox.

        Args:
            implication_number: the index of the first formula of the rule
            detached_number: the index of the second formula of the rule
            action: The current Action, alias syntax rule
        """
        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle('Warning!')
        try:
            if action == Actions.MP:
                if self.__model.add_step('', Actions.MP, implication_formula_number=(implication_number - 1),
                                         formula_to_be_detached_number=(detached_number - 1)):
                    self.__set_proving_method_layout()
                else:
                    message_box.setText('Something is wrong with Modus Ponens rule')
                    message_box.exec_()

            elif action == Actions.MT:
                if self.__model.add_step('', Actions.MT, implication_formula_number=(implication_number - 1),
                                         formula_to_be_detached_number=(detached_number - 1)):
                    self.__set_proving_method_layout()
                else:
                    message_box.setText('Something is wrong with Modus Tollens rule')
                    message_box.exec_()

            elif action == Actions.MTP:
                if self.__model.add_step('', Actions.MTP, implication_formula_number=(implication_number - 1),
                                         formula_to_be_detached_number=(detached_number - 1)):
                    self.__set_proving_method_layout()
                else:
                    message_box.setText('Something is wrong with Modus Tollendo Ponens rule')
                    message_box.exec_()

            elif action == Actions.MPT:
                if self.__model.add_step('', Actions.MPT, implication_formula_number=(implication_number - 1),
                                         formula_to_be_detached_number=(detached_number - 1)):
                    self.__set_proving_method_layout()
                else:
                    message_box.setText('Something is wrong with Modus Ponendo Tollens rule')
                    message_box.exec_()

            elif action == Actions.CS:
                if self.__model.add_step('', Actions.CS, implication_formula_number=(implication_number - 1),
                                         formula_to_be_detached_number=(detached_number - 1)):
                    self.__set_proving_method_layout()
                else:
                    message_box.setText('Something is wrong with Conditional Syllogism rule')
                    message_box.exec_()
        except FormulaInStepsException:
            self.__on_formula_in_steps_action()

    def __hint_action(self) -> None:
        """
        Tries to give hint to the user. Calls the model's get_hint function, if it returns a tuple, that
        first element is True, then raises a message box with the remaining data of the return value contains
        hint to modus ponens. Otherwise, if the model can't give any hint, then it raises a message box that tells,
        there is no option for using the modus ponens rule.
        """
        from View.Utils.utils import text_formatter
        current_hint = list(self.__model.get_hint())
        if current_hint[0]:
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle('Hint!')
            text = text_formatter(current_hint[1]) + ", " + text_formatter(current_hint[2])
            message_box.setText(text)
            message_box.exec_()
        else:
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle('Warning!')
            message_box.setText("Can't execute rule!")
            message_box.exec_()

    def __add_axiom_button_action(self) -> None:
        """
        Gives an opportunity to the user, to add an axiom. Shows a QInputDialog where the user can type a formula, and
        the model's add_axioms function called. That checks if it is an axiom or not. If it is, the axiom added
        to the model's added_axioms list.
        """
        if self.__model.end:
            self.__on_end_msg_box()
            return
        axiom, dialog = QtWidgets.QInputDialog.getText(self, 'Add axiom', 'New axiom: ')
        if dialog:
            if not self.__model.add_axiom(axiom):
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle('Warning!')
                message_box.setText("Can't add this formula to axioms!")
                message_box.exec_()
        else:
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle('Warning!')
            message_box.setText('Given inputs are incorrect!')
            message_box.exec_()

    def __use_added_axiom_action(self) -> None:
        """
        Initialize an AxiomDialog, that contains the added axioms, and the user can choose one of them,
        and can substitute formulas into it. If there are no added axioms or the proving method ended, it raises a
        message box and returns.
        """
        if self.__model.end:
            self.__on_end_msg_box()
            return
        if len(self.__model.added_axioms) == 0:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setWindowTitle('Warning')
            msg_box.setText("There is no added axioms!")
            msg_box.exec_()
            return
        if self.__model.base_axioms:
            axiom_dialog = AxiomDialog()
            axiom_dialog.add_data(self.__model, base_axioms=False)
            axiom_dialog.exec_()
            data = axiom_dialog.data
            axiom = axiom_dialog.axiom
            self.__try_axiom(axiom, data, base_axiom=False)

    def __delete_lines_button_action(self) -> None:
        """
        Gives opportunity for the user to delete lines. Raises a QInputDialog where the user can choose an index
        and the lines at the index, and below will be deleted from the steps (proving method). Checks, if there are no
        step in steps, the function raises a message box and returns.
        """
        if len(self.__model.steps) == 0:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setWindowTitle('Warning')
            msg_box.setText("There are no steps!")
            msg_box.exec_()
            return
        deletion_index, dialog = QtWidgets.QInputDialog.getInt(self, 'Deleting steps',
                                                               'Specify the number of the step from which '
                                                               'downwards all steps will be deleted:')
        if dialog:
            if deletion_index < 1:
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle('Warning!')
                message_box.setText('Given numbers must be, higher than 0!')
                message_box.exec_()
            else:
                if not self.__model.delete_steps(deletion_index - 1):
                    msg_box = QtWidgets.QMessageBox()
                    msg_box.setWindowTitle('Warning')
                    msg_box.setText("Deletion was not successful!")
                    msg_box.exec_()
                else:
                    self.__current_proving_method_layout = 0
                    self.__set_proving_method_layout()
                    self.__on_end()
        else:
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle('Warning!')
            message_box.setText('Given input are incorrect!')
            message_box.exec_()

    def __on_end(self) -> None:
        """
        If the model has ended the function changes the last line of the steps and the task to red.
        """
        if self.__model.end:
            self.__axiom_layout.itemAt(0).widget().setStyleSheet('color:Red')
            if self.__proving_method_layout.count() > 0:
                for idx in range(self.__proving_method_layout.count()):
                    widget_item = self.__proving_method_layout.itemAt(idx)
                    if isinstance(widget_item.widget(), QtWidgets.QLabel):
                        label_text = widget_item.widget().text()
                        from View.Utils.utils import text_formatter
                        if '. ' + text_formatter(self.__model.consequence_formula) + ' [' in label_text:
                            self.__proving_method_layout.itemAt(idx).widget().setStyleSheet('color:Red')
                            break
        else:
            self.__axiom_layout.itemAt(0).widget().setStyleSheet('color:White')

    def __on_end_msg_box(self) -> None:
        """
        Raises a message box when the function called, that shows the user, that tha proving method ended.
        """
        if self.__model.end:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setWindowTitle('Warning')
            msg_box.setText('End, the formula proved!')
            msg_box.exec_()

    def __save_model(self) -> None:
        """
        On click event for the SAVE button. when it is called, the whole proving method will be saved.
        model's save_model function is called.
        """
        if not self.__model.save_model():
            msg_box = QtWidgets.QMessageBox()
            msg_box.setWindowTitle('Warning')
            msg_box.setText("Can't save!")
            msg_box.exec_()
        else:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setWindowTitle('Success')
            msg_box.setText("Saved!")
            msg_box.exec_()

    @staticmethod
    def __get_help() -> None:
        """
        Initialize a HelpDialog for the user, and gives the focus to the new Dialog.
        """
        help_dialog = HelpDialog(config=False)
        help_dialog.exec_()

    @staticmethod
    def __on_formula_in_steps_action() -> None:
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle('Warning')
        msg_box.setText("The evaluated formula appears in the current steps!")
        msg_box.exec_()
