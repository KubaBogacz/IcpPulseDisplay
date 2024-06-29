# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide6.QtCore import QObject, Property, Signal
from backend_test import Backend
from controller.controller import Controller
from controller.plotter import Plotter
    
backend = Backend()
controller = Controller()

CURRENT_DIRECTORY = Path(__file__).resolve().parent


if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    engine.rootContext().setContextProperty("backend", backend)
    qmlRegisterType(Controller, 'Controller', 1, 0, 'Controller')
    qmlRegisterType(Plotter, 'Plotter', 1, 0, 'Plotter')

    main_file = CURRENT_DIRECTORY / "frontend/Main.qml"
    engine.load(main_file)


    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())