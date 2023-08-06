#!/usr/bin/env python3
import logging
import logging.handlers
import os
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import matc.constants
import matc.globa
import matc.settings
import matc.main_object

# The following import looks like it isn't used, but it is necessary for importing the images.
import matc.matc_rc  # pylint: disable=unused-import

LOG_FILE_NAME_STR = "matc.log"


def on_about_to_quit():
    logging.debug("on_about_to_quit --- saving settings to json file (in the user config dir)")
    matc.settings.save_settings_to_json_file()


def main():
    # db_filepath: str = matc.globa.get_database_path()
    # matc.globa.db_file_exists_at_application_startup_bl = os.path.isfile(db_filepath)
    # -settings this variable before the file has been created

    logger = logging.getLogger()
    # -if we set a name here for the logger the file handler will no longer work, unknown why
    logger.handlers = []  # -removing the default stream handler first
    # logger.propagate = False
    log_path_str = matc.globa.get_config_path(LOG_FILE_NAME_STR)
    rfile_handler = logging.handlers.RotatingFileHandler(log_path_str, maxBytes=8192, backupCount=2)
    rfile_handler.setLevel(logging.WARNING)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    rfile_handler.setFormatter(formatter)
    logger.addHandler(rfile_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    matc_qapplication = QtWidgets.QApplication(sys.argv)

    # Application information
    matc.globa.sys_info_telist.append(("Application name", matc.constants.APPLICATION_NAME))
    matc.globa.sys_info_telist.append(("Application version", matc.constants.APPLICATION_VERSION))
    matc.globa.sys_info_telist.append(("Config path", matc.globa.get_config_path()))
    matc.globa.sys_info_telist.append(("Module path", matc.globa.get_module_path()))
    matc.globa.sys_info_telist.append(("Python version", sys.version))
    matc.globa.sys_info_telist.append(("Qt version", QtCore.qVersion()))
    matc.globa.sys_info_telist.append(("PyQt (Python module) version", QtCore.PYQT_VERSION_STR))
    sys_info = QtCore.QSysInfo()
    matc.globa.sys_info_telist.append(("OS name and version", sys_info.prettyProductName()))
    matc.globa.sys_info_telist.append(
        ("Kernel type and version", sys_info.kernelType() + " " + sys_info.kernelVersion()))
    matc.globa.sys_info_telist.append(("buildCpuArchitecture", sys_info.buildCpuArchitecture()))
    matc.globa.sys_info_telist.append(("currentCpuArchitecture", sys_info.currentCpuArchitecture()))

    # set stylesheet
    stream = QtCore.QFile(os.path.join(matc.globa.get_module_path(), "matc.qss"))
    stream.open(QtCore.QIODevice.ReadOnly)
    matc_qapplication.setStyleSheet(QtCore.QTextStream(stream).readAll())

    desktop_widget = matc_qapplication.desktop()
    matc.globa.sys_info_telist.append(("Virtual desktop", str(desktop_widget.isVirtualDesktop())))
    matc.globa.sys_info_telist.append(("Screen count", str(desktop_widget.screenCount())))
    matc.globa.sys_info_telist.append(("Primary screen", str(desktop_widget.primaryScreen())))

    system_locale = QtCore.QLocale.system().name()
    logging.info('System Localization: ' + system_locale)
    matc_qapplication.setQuitOnLastWindowClosed(False)
    matc_qapplication.aboutToQuit.connect(on_about_to_quit)

    matc_main_object = matc.main_object.MainObject()

    sys.exit(matc_qapplication.exec_())


if __name__ == "__main__":
    main()
