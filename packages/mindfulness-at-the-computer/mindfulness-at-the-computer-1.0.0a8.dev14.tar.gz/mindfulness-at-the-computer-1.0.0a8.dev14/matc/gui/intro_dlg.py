import logging
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import matc.gui.breathing_dlg
import matc.globa
import matc.settings

NEXT = "Next >>"
PREV = "<< Prev"
MARGIN_TOP = 35
WIDGET_SPACING = 10

"""
An alternative to using a custom QDialog can be to use QWizard with QWizardPages
"""


class Label(QtWidgets.QLabel):
    def __init__(self, i_text: str, i_font_size: matc.globa.FontSize = matc.globa.FontSize.xlarge):
        super().__init__(text=i_text)
        self.setWordWrap(True)
        self.setFont(matc.globa.get_font(i_font_size))
        # text_qll.setAlignment(QtCore.Qt.AlignHCenter)


class IconImage(QtWidgets.QLabel):
    def __init__(self, i_file_name: str):
        super().__init__()
        # text_qll.setAlignment(QtCore.Qt.AlignHCenter)
        self.setPixmap(QtGui.QPixmap(matc.globa.get_app_icon_path(i_file_name)))
        # self.setAlignment(QtCore.Qt.AlignHCenter)


class IntroDlg(QtWidgets.QDialog):
    """
    The introduction wizard with examples of dialogs and functionality to adjust initial settings
    """
    close_signal = QtCore.pyqtSignal(bool)
    # -the boolean indicates whether or not we want the breathing dialog to open

    def __init__(self):
        super().__init__()

        self.wizard_qsw_w3 = QtWidgets.QStackedWidget()
        self.prev_qpb = QtWidgets.QPushButton(PREV)
        self.next_qpb = QtWidgets.QPushButton(NEXT)


        self.prev_qpb.clicked.connect(self.on_prev_clicked)
        self.next_qpb.clicked.connect(self.on_next_clicked)

        hbox_l3 = QtWidgets.QHBoxLayout()
        hbox_l3.addStretch(1)
        hbox_l3.addWidget(self.prev_qpb, stretch=1)
        hbox_l3.addWidget(self.next_qpb, stretch=1)
        hbox_l3.addStretch(1)

        vbox_l2 = QtWidgets.QVBoxLayout()
        vbox_l2.addWidget(self.wizard_qsw_w3)
        vbox_l2.addLayout(hbox_l3)

        welcome_description_ll = Label(
            "<p>Welcome to Mindfulness at the Computer!</p>"
            "<p>This introduction will help you understand how to use the application</p>"
            "<p>Mindfulness at the Computer is an application that helps you stay mindful while using the computer by reminding you to take short (interactive) breathing breaks.</p>"
            "<p>The main parts of the application:</p><ul>"
            "<li>The system tray icon</li>"
            "<li>The breathing dialog</li>"
            "<li>The settings window</li>"
            "</ul>"
            "<p>These will now be discussed on the following pages. "
            "Please click *next* to continue</p>"
        )
        welcome_page = IntroPage("Welcome", welcome_description_ll)
        self.wizard_qsw_w3.addWidget(welcome_page)

        systray_description_ll = Label(
            "When you run Mindfulness at the Computer it is accessible via the system tray. "
            "From the menu that opens when clicking on this icon you can:<ul>"
            "<li>Open the settings window</li>"
            "<li>Invoke a breathing session (using the last phrase)</li>"
            "<li>Invoke a breathing session using a selected phrase</li>"
            "<li>Exit the application</li>"
            "</ul>"
        )
        icon_image = IconImage("icon.png")
        notification_description_ll = Label(
            "<p><b>The breathing notification</b></p>"
            "This notification pops up every once in a while. "
            "It prepares you for taking a breathing break. "
            "(You can adjust how often you would like to take a breathing break)."
        )
        icon_br_image = IconImage("icon-b.png")
        systray_page = IntroPage("The system tray", systray_description_ll, icon_image,
            notification_description_ll, icon_br_image)
        self.wizard_qsw_w3.addWidget(systray_page)

        br_dlg_description_ll = Label(
            "This dialog helps you to relax and return to your breathing. "
            "Try it out, it is interactive!"
        )
        self.breathing_dlg = matc.gui.breathing_dlg.BreathingGraphicsView(i_can_be_closed=False)
        self.breathing_dlg.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.breathing_dlg.initiate()
        br_dlg_details_ll = Label(
            "There are three ways to interact with the breathing dialog: <ul>"
            '<li>Hovering over the light green area in the middle while breathing in</li>'
            '<li>Hovering over the text for the in-breath while breathing in</li>'
            '<li>Pressing down shift while breathing in</li>'
            '<ul>'
        )
        self.br_dlg_page = IntroPage("The breathing dialog", br_dlg_description_ll,
            br_dlg_details_ll, self.breathing_dlg)
        self.wizard_qsw_w3.addWidget(self.br_dlg_page)

        settings_description_ll = Label(
            'The settings dialog can be reached by opening the systray menu and selecting '
            '"Settings" from there. (Please open it now if you want to follow along in the '
            'description below)'
        )
        settings_details_ll = Label(
            'Some of the settings that can be changed: <ul>'
            '<li>Amount of time before a breahitng notification is shown --- '
            'You may want to adjust this setting now (the default is '
            f'{matc.settings.BREATHING_BREAK_TIMER_DEFAULT_SECS // 60} minutes)</li>'
            '<li>Volume of the audio (bells)</li>'
            '<li>Breathing phrases (displayed at the bottom of the breathing dialog) '
            '--- It is possible to add new phrases and reorder them. The topmost phrase is '
            'always used at the start</li>'
            '<li>Whether or not to move the mouse cursor into the breathing dialog (useful'
            'if you are using a touchpad)</li>'
            '<ul>'
        )
        settings_page = IntroPage("Settings", settings_description_ll, settings_details_ll)
        self.wizard_qsw_w3.addWidget(settings_page)

        """
        "<p>In this dialog it's possible to hover over the words shown</p>"
        "<p><strong>Breathing in:</strong> Hover over the green box</p>"
        "<p><strong>Breathing out:</strong> Hover outside the green box</p>"
        """
        additional_setup_ll = Label(
            '<p>You may want to add a shortcut to the application. '
            'Also you may want to add the application to autostart.</p>'
        )
        relaunch_wizard_ll = Label(
            '<p>You can start this wizard again by choosing "Help" -> "Show intro wizard"'
            ' in the settings window (available from the system tray icon menu)</p>'
        )
        other_help_ll = Label(
            '<p>Other ways to get help:</p><ul>'
            '<li>The gitter chat: https://gitter.im/mindfulness-at-the-computer/community</li>'
            '<li>Email: sunyata.software@gmail.com</li>'
            '<li>Online user guide: ___tbd___</li>'
            '</ul>'
        )
        # more: feedback
        feedback_ll = Label(
            "We are grateful for any feedback you can give us. Please use the email "
            "address above to contact us with gratitudes or suggestions for improvements"
        )
        finish_text_ll = Label(
            "<p>When you click on finish and exit this wizard a breathing dialog will be shown.</p>"
        )

        finish_page = IntroPage("Finish", relaunch_wizard_ll, other_help_ll,
            feedback_ll, finish_text_ll)
        self.wizard_qsw_w3.addWidget(finish_page)


        self.setGeometry(300, 150, 650, 150)
        self.setLayout(vbox_l2)
        self.update_gui()
        self.show()

    def on_next_clicked(self):
        current_index_int = self.wizard_qsw_w3.currentIndex()
        if current_index_int >= self.wizard_qsw_w3.count() - 1:
            self.close_signal.emit(True)
            self.close()

        logging.debug("current_index_int = " + str(current_index_int))
        self.wizard_qsw_w3.setCurrentIndex(current_index_int + 1)
        self.update_gui()

    def on_prev_clicked(self):
        current_index_int = self.wizard_qsw_w3.currentIndex()
        if current_index_int <= 0:
            return
        logging.debug("current_index_int = " + str(current_index_int))
        self.wizard_qsw_w3.setCurrentIndex(current_index_int - 1)
        self.update_gui()

    def update_gui(self):
        current_index_int = self.wizard_qsw_w3.currentIndex()
        self.prev_qpb.setDisabled(current_index_int == 0)

        if current_index_int == self.wizard_qsw_w3.count() - 1:
            self.next_qpb.setText("Finish")  # "open breathing dialog"
        else:
            self.next_qpb.setText(NEXT)

        if self.wizard_qsw_w3.currentWidget() == self.br_dlg_page:
            self.breathing_dlg.setFocus()


class IntroPage(QtWidgets.QWidget):
    def __init__(self, i_title: str, *i_widgets):
        super().__init__()
        self.setSizePolicy(
            self.sizePolicy().horizontalPolicy(),
            QtWidgets.QSizePolicy.MinimumExpanding
        )

        self.vbox_l2 = QtWidgets.QVBoxLayout()
        (cm_left, cm_top, cm_right, cm_bottom) = self.vbox_l2.getContentsMargins()
        self.vbox_l2.setContentsMargins(50, cm_top, 0, cm_bottom)
        self.setLayout(self.vbox_l2)
        self.vbox_l2.addSpacing(MARGIN_TOP)
        self.title_qll = QtWidgets.QLabel(i_title)
        # self.title_qll.setAlignment(QtCore.Qt.AlignHCenter)
        self.title_qll.setFont(matc.globa.get_font(matc.globa.FontSize.xxlarge))
        self.vbox_l2.addWidget(self.title_qll)
        self.vbox_l2.addSpacing(WIDGET_SPACING)

        for widget in i_widgets:
            self.vbox_l2.addWidget(widget)
            self.vbox_l2.addSpacing(WIDGET_SPACING)

        self.vbox_l2.addStretch(1)
