# -*- coding: utf-8 -*-
# только парсер и его бек-энд
import requests  # для выполнения запросов к сайту
from lxml import html  #, etry  # необходимо для "расшифровки html"
from typing import Any, Optional, NoReturn
# дабы придерживаться стиля,
# указывая типы переменных (а-ля TypeScript) (жаль тут типы проверяются только ide)


def parse(title: str, author: str, pretty_flag: bool = False) -> Optional[int]:
    """
    обязательные аргументы-строки "название" и "автор",
    так же необязательный аргумент о "красивом" тексте песен
    если Истина -> будет только текст, иначе так же и объявления о переходах, припевах и т.д.
    """
    if not isinstance(author, str):
        raise TypeError(f"bad operand type for parse(): '{type(author)}'; expected: 'str'")
    if not isinstance(title, str):
        raise TypeError(f"bad operand type for parse(): '{type(title)}'; expected: 'str'")
    if not isinstance(pretty_flag, bool):
        raise TypeError(f"bad operand type for parse(): '{type(pretty_flag)}'; expected: 'bool'")
    # проверки на тип: если тип не подходит -> бросить исключение
    author: str = author.strip().lower()
    title: str = title.strip().lower()
    url: str = f"https://www.amalgama-lab.com/songs/{author[0]}/{author.replace(' ', '_')}/{title.replace(' ', '_')}.html"
    api: requests.Response = requests.get(url=url)
    tree: Any = html.document_fromstring(api.text)
    text_original: Any = tree.xpath('//*[@id="click_area"]/div//*[@class="original"]/text()')
    text_translate: Any = tree.xpath('//*[@id="click_area"]/div//*[@class="translate"]/text()')
    if len(text_original) == len(text_translate):
        with open('cache_origin.txt', 'w', encoding='utf-8') as cache_origin:
            with open('cache_trans.txt', 'w', encoding='utf-8') as cache_trans:
                for i in range(len(text_original)):
                    orig = text_original[i]
                    trans = text_translate[i]
                    if pretty_flag:
                        if ('[' in orig and '[' in trans) and (']' in orig and ']' in trans):
                            continue
                    print(
                        text_original[i],
                        file=cache_origin
                    )  # запись в файл для дальнейшего использования
                    print(
                        text_translate[i],file=cache_trans
                    )
        if len(text_original) == 0:
            return 1
    print('[parser] Парсер успешно получил текст и записал его в файлы кеша с заданными параметрами:\n{}={}\n{}={}\n{}={}'.format(
        'title',
        title,
        'author',
        author,
        'pretty_flag',
        pretty_flag
    ))           


def main() -> NoReturn:
    parse('Immortals', 'fall out boy')  # пример для теста


if __name__ == "__main__":
    main()
