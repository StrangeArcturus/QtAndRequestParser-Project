# -*- coding: utf-8 -*-
# main.py

from typing import NoReturn
from sys import argv, exit as _exit

from PyQt5.QtWidgets import QApplication

from connector import DataBaseConnector
from window import Window


def main() -> NoReturn:
    connector: DataBaseConnector = DataBaseConnector('songs.db')
    app: QApplication = QApplication(argv)
    window: Window = Window(connector)
    window.show()
    _exit(app.exec())


if __name__ == "__main__":
    main()
