from .. import Defines


def declined(word: str, *args, path=(), ask_func):
    return {
        Defines.default: case(word, *args, 'и.п.', path=path + ('Именительный падеж', ), ask_func=ask_func),
        'р.п.': case(word, *args, 'р.п.', path=path + ('Родительный падеж', ), ask_func=ask_func),
        'д.п.': case(word, *args, 'д.п.', path=path + ('Дательный падеж', ), ask_func=ask_func),
        'в.п.': case(word, *args, 'в.п.', path=path + ('Винительный падеж', ), ask_func=ask_func),
        'т.п.': case(word, *args, 'т.п.', path=path + ('Творительный падеж', ), ask_func=ask_func),
        'п.п.': case(word, *args, 'п.п.', path=path + ('Предложный падеж', ), ask_func=ask_func)
    }


def case(word: str, *args, path=(), ask_func):
    if 'ед.ч.' in args or 'мн.ч.' in args:
        return '+' if 'и.п.' in args else ask_func(word, path)

    return {
        Defines.default: '+' if 'и.п.' in args else ask_func(word, path + ('единственное число', )),
        'мн.ч.': ask_func(word, path + ('множественное число', ))
    }
