# -*- coding: utf-8 -*-
# window class
from typing import Any, Optional
from time import sleep

from PyQt5.QtWidgets import QMainWindow

from connector import DataBaseConnector
from design import Ui_MainWindow
from backend import parse


class Window(Ui_MainWindow, QMainWindow):
    def __init__(self, connector: DataBaseConnector) -> None:
        super().__init__()
        if not isinstance(connector, DataBaseConnector):
            raise TypeError(f"bad operand type for __init__() in class Window: '{type(connector)}'; expected: 'DataBaseConnector'")
        self.connector: DataBaseConnector = connector
        self.initUI()
        print('[PyQt] построено главное окно приложения')
    
    def initUI(self) -> None:
        self.setupUi(self)
        self.get_text.clicked.connect(self._click)
    
    def _warning(self) -> None:
        print('[PyQt] окном приложения брошено предупреждение')
        self.info.setText(
            "Что-то пошло не так с поиском песни. Пожалуйста, проверьте введённые данные"
        )
        self.info.setStyleSheet("background-color: orange")
    
    def _good_job(self) -> None:
        self.info.setText("По вашему запросу успешно показана песня и её перевод")
        self.info.setStyleSheet("background-color: cyan")
    
    def _error(self, error: Any) -> None:
        print('[PyQt] окном приложения брошена ошибка')
        self.error_text.setText(f"{type(error)}{error}")
        self.error_text.setStyleSheet("background-color: red")
    
    def _click(self) -> None:
        print('[PyQt] окном приложения выполнены нажатие кнопки и запрос к базе данных/парсеру')
        self.info.setStyleSheet("background-color: white")
        sleep(1)
        title: str = self.song_title.text()
        author: str = self.song_author.text()
        pretty_flag: bool = self.pretty_flag.isChecked()
        error: Optional[Exception] = None
        result: Optional[int] = None
        data: dict = {}
        sleep(1)
        try:
            data = self.connector.get_song(title, author, pretty_flag)
            text_origin = data['origin']
            text_trans = data['translate']
        except Exception:
            try:
                sleep(1)
                result: Optional[int] = parse(
                    title=title,
                    author=author,
                    pretty_flag=pretty_flag
                )
            except Exception as error:
                error = error
            with open('cache_origin.txt', 'r', encoding='utf-8') as file:
                text_origin = file.read()
            with open('cache_trans.txt', 'r', encoding='utf-8') as file:
                text_trans = file.read()
            sleep(1)
            self.connector.write_song(
                title,
                author,
                text_origin,
                text_trans,
                pretty_flag
            )
        self.orig_text.setPlainText(text_origin)
        self.trans_text.setPlainText(text_trans)
        sleep(1)
        if result:
            self._warning()
        else:
            self._good_job()
        sleep(1)
        if error:
            self._error(error)
    
    def __del__(self) -> None:
        print('[PyQt] оконное приложение обработано сборщиком мусора и закрыто')
