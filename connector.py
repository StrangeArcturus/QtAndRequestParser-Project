import sqlite3


class DataBaseConnector:
    def __init__(self, path: str) -> None:
        self.__name = self.__class__.__name__
        if not isinstance(path, str):
            raise TypeError(
                f"bad operand type for __init__() in {self.__name}: '{type(path)}'; expected: 'str'"
            )
        self.connect: sqlite3.Connection = sqlite3.connect(path)
        cursor: sqlite3.Cursor = self.connect.cursor()
        print(f'[SQLite3] получено соединение к базе данных по пути {path}')
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS songs
            (title TEXT, author TEXT, text_original TEXT, text_translated TEXT)
        """)
    
    def write_song(self, song_title: str, song_author: str, text_original: str, text_translated: str, pretty_flag: bool) -> None:
        if not isinstance(song_title, str):
            raise TypeError(
                f"bad operand type for write_song() in {self.__name}: '{type(song_title)}'; expected: 'str'"
            )
        if not isinstance(song_author, str):
            raise TypeError(
                f"bad operand type for write_song() in {self.__name}: '{type(song_author)}'; expected: 'str'"
            )
        if not isinstance(text_original, str):
            raise TypeError(
                f"bad operand type for write_song() in {self.__name}: '{type(text_original)}'; expected: 'str'"
            )
        if not isinstance(text_translated, str):
            raise TypeError(
                f"bad operand type for write_song() in {self.__name}: '{type(text_translated)}'; expected: 'str'"
            )
        if not isinstance(pretty_flag, bool):
            raise TypeError(
                f"bad operand type for write_song() in {self.__name}: '{type(pretty_flag)}'; expected: 'bool'"
            )
        if pretty_flag:
            song_title += '_pretty'
        cursor: sqlite3.Cursor = self.connect.cursor()
        data: tuple = (
            song_title,
            song_author,
            text_original,
            text_translated
        )
        cursor.execute("""
            INSERT INTO songs (title, author, text_original, text_translated)
            VALUES (?, ?, ?, ?)
        """, data)
        self.connect.commit()
        print('[SQLite3] успешно занесена в базу данных песня с параметрами:\n{}={}\n{}={}\n{}{}\n{}\n{}'.format(
            'song_title',
            song_title,
            'song_author',
            song_author,
            'text_original',
            text_original,
            'text_translated',
            text_translated,
            'pretty_flag',
            pretty_flag
        ))
    
    def get_song(self, song_title: str, song_author: str, pretty_flag: bool) -> dict:
        if not isinstance(song_title, str):
            raise TypeError(f"bad operand type for get_song() in {self.__name}: '{type(song_title)}'; expected: 'str'")
        if not isinstance(song_author, str):
            raise TypeError(f"bad operand type for get_song() in {self.__name}: '{type(song_author)}'; expected: 'str'")
        if not isinstance(pretty_flag, bool):
            raise TypeError(f"bad operand type for get_song() in {self.__name}: '{type(pretty_flag)}'; expected: 'bool'")
        if pretty_flag:
            song_title += '_pretty'
        cursor: sqlite3.Cursor = self.connect.cursor()
        data: tuple = (
            song_title,
            song_author
        )
        _exec = cursor.execute("""
            SELECT text_original, text_translated FROM songs
            WHERE title = ? AND author = ?
        """, data).fetchone()
        if _exec:
            print('[SQLite3] успешно получена запись из базы данных по параметрам:\n{}={}\n{}={}\n{}={}'.format(
                'song_title',
                song_title,
                'song_author',
                song_author,
                'pretty_flag',
                pretty_flag
            ))
        output: dict = {
            'origin': _exec[0],
            'translate': _exec[1]
        } if _exec else {}
        return output
    
    def __del__(self):
        self.connect.close()
        print('[SQLite3] подключение к базе данных упешно разорвано')
