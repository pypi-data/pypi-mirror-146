import logging
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
try:
    # noinspection PyUnresolvedReferences
    from PyQt5 import QtMultimedia
except ImportError:
    logging.debug("ImportError for QtMultimedia - maybe because there's no sound card available")
    # -If the system does not have a sound card (as for example Travis CI)
    # -An alternative to this approach is to use this: http://doc.qt.io/qt-5/qaudiodeviceinfo.html#availableDevices
import matc.constants
import matc.globa
import matc.settings
import matc.gui.breathing_dlg
import matc.gui.settings_win
import matc.gui.intro_dlg


class MainObject(QtCore.QObject):
    """
    We are using this QObject as the core of the application (rather than using a QMainWindow)
    Areas of responsibility:
    * Breathing timer
    * Holds the settings window
    * Holds the breathing-and-rest dialog
    * Handles audio
    * Holds the systray

    """
    def __init__(self):
        super().__init__()
        self.bp_action_list = []
        self.circle_count: int = 1

        # System tray and menu setup
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_menu = QtWidgets.QMenu()  # self
        self.tray_menu.aboutToShow.connect(self.on_tray_menu_about_to_show)
        self.update_systray_menu()
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.messageClicked.connect(self.on_tray_icon_message_clicked)
        self.tray_icon.show()
        self.update_systray_image()

        # System info (more is available in main.py)
        systray_available_str = "No"
        if self.tray_icon.isSystemTrayAvailable():
            systray_available_str = "Yes"
        matc.globa.sys_info_telist.append(("System tray available", systray_available_str))
        notifications_supported_str = "No"
        if self.tray_icon.supportsMessages():
            notifications_supported_str = "Yes"
        matc.globa.sys_info_telist.append(("System tray notifications supported", notifications_supported_str))
        logging.info("##### System Information #####")
        for (descr_str, value) in matc.globa.sys_info_telist:
            logging.info(descr_str + ": " + str(value))
        logging.info("#####")

        # Audio setup
        self.sound_effect = None
        try:
            self.sound_effect = QtMultimedia.QSoundEffect(self)
            # -PLEASE NOTE: A parent has to be given here, otherwise we will not hear anything
        except NameError:
            logging.debug("NameError - Cannot play audio since QtMultimedia has not been imported")

        # Timer setup
        self.breathing_reminder_timer = Timer()
        self.breathing_reminder_timer.timeout_signal.connect(self.on_breathing_timer_timeout)
        """
        self.systray_breathing_timer = Timer(i_continuous=True)
        self.systray_breathing_timer.timeout_signal.connect(self.on_systray_breathing_timeout)
        self.systray_breathing_timer.start(0.32)
        """

        # Window setup
        self.settings_win = None
        self.br_and_rest_dlg = matc.gui.breathing_dlg.BreathingAndRestDlg()
        self.br_and_rest_dlg.breathing_gv.first_breathing_gi_signal.connect(self.on_first_breathing_gi)
        self.br_and_rest_dlg.close_signal.connect(self.on_br_and_rest_closed)

        # Initialization for the user
        ################# self.breathing_reminder_timer.stop()
        if not matc.globa.settings_file_exists():
            if not matc.globa.testing_bool:
                self.show_intro_dialog()
        else:
            self.br_and_rest_dlg.show_breathing_only()

        """
        # Startup actions
        if not matc.globa.db_file_exists_at_application_startup_bl and not matc.globa.testing_bool:
            self.show_intro_dialog()
        # self.open_breathing_prepare()

        settings = matc.model.SettingsM.get()
        if settings.nr_times_started_since_last_feedback_notif != matc.globa.FEEDBACK_DIALOG_NOT_SHOWN_AT_STARTUP:
            if (settings.nr_times_started_since_last_feedback_notif
            >= matc.globa.NR_OF_TIMES_UNTIL_FEEDBACK_SHOWN_INT - 1):
                self.show_feedback_dialog()
                settings.nr_times_started_since_last_feedback_notif = 0
            else:
                settings.nr_times_started_since_last_feedback_notif += 1
        else:
            pass
        """

    """
            matc.globa.rest_reminder_minutes_passed_int += 1


    def on_systray_activated(self, i_reason):
        # LXDE:
        # XFCE:
        # MacOS:
        logging.debug("===== on_systray_activated entered =====")
        logging.debug("i_reason = " + str(i_reason))
        logging.debug("mouseButtons() = " + str(QtWidgets.QApplication.mouseButtons()))
        self.tray_icon.activated.emit(i_reason)

        if i_reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.restore_window()
        else:
            self.tray_icon.activated.emit(i_reason)

        logging.debug("===== on_systray_activated exited =====")
        
    """

    def show_intro_dialog(self):
        self.intro_dlg = matc.gui.intro_dlg.IntroDlg()
        self.intro_dlg.close_signal.connect(self.on_intro_dialog_closed)
        self.intro_dlg.exec()

    def on_intro_dialog_closed(self, i_open_breathing_dialog: bool):
        self._open_br_dlg()

    def _open_br_dlg(self):
        self.br_and_rest_dlg.show_breathing_only()
        matc.globa.is_breathing_reminder_shown = False
        self.update_systray_image()
        self.breathing_reminder_timer.stop()

    def on_tray_br_phrase_triggered(self, i_action: QtWidgets.QAction):
        if i_action.data():
            matc.globa.active_phrase_id = int(i_action.data())
            self._open_br_dlg()

    def on_tray_quit_triggered(self):
        QtWidgets.QApplication.quit()

    def on_br_and_rest_closed(self):
        br_timer_secs: int = matc.settings.settings.get(matc.settings.SK_BREATHING_BREAK_TIMER_SECS)
        self.breathing_reminder_timer.start(br_timer_secs)
        matc.globa.is_breathing_reminder_shown = False
        self.update_systray_image()

    def play_audio(self, i_audio_filename: str, i_volume: int) -> None:
        """
        Please note that the important variable sound_effect is setup at the beginning of the init for settings_win.py
        The reason is that to create this variable we need to send a "self" variable (of which type?)
        :param i_audio_filename:
        :param i_volume:
        :return:
        """
        if self.sound_effect is None:
            logging.warning("play_audio: sound_effect is None")
            return
        audio_path_str = matc.globa.get_user_audio_path(i_audio_filename)
        audio_source_qurl = QtCore.QUrl.fromLocalFile(audio_path_str)
        self.sound_effect.setSource(audio_source_qurl)
        self.sound_effect.setVolume(float(i_volume / 100))
        self.sound_effect.play()

    def on_tray_icon_message_clicked(self):
        print("on_tray_icon_message_clicked")
        """
        Doesn't work on XUbuntu, not sure about other systems
        https://forum.qt.io/topic/115121/qsystemtrayicon-not-sending-messageclicked-signal-on-linux/6
        """

    def on_breathing_timer_timeout(self):
        # audio_path_str = matc.globa.get_user_audio_path("small_bell_short[cc0].wav")
        volume: int = matc.settings.get_breathing_volume()
        self.play_audio(matc.globa.SMALL_BELL_SHORT_FILENAME, volume)
        matc.globa.is_breathing_reminder_shown = True
        self.update_systray_image()
        ######### self.prepare_timer.start(3)

        phrase = matc.settings.get_breathing_phrase(matc.globa.active_phrase_id)
        phrase_text: str = f"{phrase.in_breath}\n{phrase.out_breath}"

        # "Mindfulness at the Computer"
        self.tray_icon.showMessage(matc.constants.APPLICATION_PRETTY_NAME,
            phrase_text, QtWidgets.QSystemTrayIcon.NoIcon, 5000)

    def on_systray_breathing_timeout(self):
        self.update_systray_image(i_increment=True)

    def on_first_breathing_gi(self):
        # audio_path_str = matc.globa.get_user_audio_path("big_bell[cc0].wav")
        volume: int = matc.settings.get_breathing_volume()
        self.play_audio(matc.globa.BIG_BELL_FILENAME, volume)

    def update_systray_menu(self):
        self.tray_open_breathing_dialog_qaction = QtWidgets.QAction(self.tr("Breathing Dialog"))
        self.tray_menu.addAction(self.tray_open_breathing_dialog_qaction)
        self.tray_open_breathing_dialog_qaction.triggered.connect(self.on_tray_open_breathing_dialog_triggered)
        self.tray_menu.addSeparator()
        self.tray_open_settings_action = QtWidgets.QAction(self.tr("Settings"))
        self.tray_menu.addAction(self.tray_open_settings_action)
        self.tray_open_settings_action.triggered.connect(self.on_tray_open_settings_triggered)
        self.tray_quit_action = QtWidgets.QAction(self.tr("Quit"))
        self.tray_menu.addAction(self.tray_quit_action)
        self.tray_quit_action.triggered.connect(self.on_tray_quit_triggered)

        self.tray_menu.setDefaultAction(self.tray_open_breathing_dialog_qaction)

        self.tray_br_phrases_qmenu = QtWidgets.QMenu("Phrases")
        self.tray_br_phrases_qmenu.triggered.connect(self.on_tray_br_phrase_triggered)

        self.tray_menu.addMenu(self.tray_br_phrases_qmenu)
        phrases: list[matc.settings.BreathingPhrase] = matc.settings.settings[matc.settings.SK_BREATHING_PHRASES]
        self.bp_action_list.clear()
        for p in phrases:
            self._add_bp_to_submenu(p.id)

    def _add_bp_to_submenu(self, i_id: int):
        if i_id == matc.globa.BREATHING_PHRASE_NOT_SET:
            logging.error("Breathing phrase not set. This should not be possible")
            phrase_text: str = "nothing"
        else:
            phrase = matc.settings.get_breathing_phrase(i_id)
            phrase_text: str = f"{phrase.in_breath}"
        # qlwi = QtWidgets.QListWidgetItem(phrase_text)
        bp_qaction = QtWidgets.QAction(phrase_text)
        bp_qaction.setData(i_id)
        self.bp_action_list.append(bp_qaction)
        self.tray_br_phrases_qmenu.addAction(bp_qaction)

    def update_systray_image(self, i_increment=False):
        """
        if i_increment:
            self.circle_count += 1
            if self.circle_count >= 33:
                self.circle_count = 1
        icon_file_name_str = f"{int(self.circle_count)}.png"
        """

        icon_file_name_str = "icon.png"
        if matc.globa.is_breathing_reminder_shown:
            icon_file_name_str = f"icon-b.png"
        systray_icon_path = matc.globa.get_app_icon_path(icon_file_name_str)
        self.tray_icon.setIcon(QtGui.QIcon(systray_icon_path))

    def on_tray_menu_about_to_show(self):
        logging.debug("on_tray_menu_about_to_show")
        # self.rest_progress_qaction.setText("TBD - time since last rest")

    def on_tray_open_settings_triggered(self):
        self.settings_win = matc.gui.settings_win.SettingsWin()
        self.settings_win.show_intro_dialog_signal.connect(self.on_settings_show_intro_dialog)
        self.settings_win.show()

    def on_settings_show_intro_dialog(self):
        self.show_intro_dialog()

    def on_tray_open_breathing_dialog_triggered(self):
        self._open_br_dlg()


class Timer(QtCore.QObject):
    timeout_signal = QtCore.pyqtSignal()

    def __init__(self, i_continuous: bool = False):
        super().__init__()
        # self.minutes_elapsed: int = 0
        self.timeout_secs = -1
        self.timer = None
        self.end_after_next_timeout: bool = not i_continuous

    def stop(self):
        if self.timer is not None and self.timer.isActive():
            self.timer.stop()
        # self.minutes_elapsed = 0

    def start(self, i_timeout_secs: float):
        self.stop()
        self.timeout_secs = i_timeout_secs
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.timeout)
        self.timer.start(int(self.timeout_secs * 1000))

    def timeout(self):
        # self.minutes_elapsed += 1
        self.timeout_signal.emit()
        print("self.update_signal.emit(True)")
        if self.end_after_next_timeout:
            self.timer.stop()
