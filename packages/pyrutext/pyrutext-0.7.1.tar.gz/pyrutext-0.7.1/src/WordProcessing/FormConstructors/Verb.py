from .. import Defines


def imperative(word: str, *, path=(), ask_func):
    imperative_form = ask_func(word, path)
    return {
        Defines.default: imperative_form,
        'мн.ч.': imperative_form + 'те'
    }


def conjugable(word: str, *args, path=(), ask_func):
    forms = {}

    forms[Defines.default] = '+'
    forms['п.в.'] = time_past(word, path=path + ('Прошедшее время', ), ask_func=ask_func)
    forms['б.в.'] = time(word, *args, 'б.в.', path=path + ('Будущее время', ), ask_func=ask_func)
    if 'несов.' in args:
        forms['н.в.'] = time(word, *args, 'н.в.', path=path + ('Настоящее время', ), ask_func=ask_func)

    return forms


def time_past(word: str, *, path=(), ask_func):
    forms = {}

    standard_form = ask_func(word, path)

    forms[Defines.default] = standard_form  # мужской род
    if standard_form[-1] != 'л':
        standard_form = standard_form + 'л'
    forms['ж.р.'] = standard_form + 'а'
    forms['с.р.'] = standard_form + 'о'
    forms['мн.ч.'] = standard_form + 'и'

    return forms


def time(word: str, *args, path=(), ask_func):
    return {
        Defines.default: '+',
        '1л': person(word, *args, '1л', path=path + ('первое лицо', ), ask_func=ask_func),
        '2л': person(word, *args, '2л', path=path + ('второе лицо', ), ask_func=ask_func),
        '3л': person(word, *args, '3л', path=path + ('третье лицо', ), ask_func=ask_func)
    }


def person(word: str, *args, path=(), ask_func):
    if 'б.в.' in args and 'несов.' in args:
        return {
            Defines.default: 'буду +',
            'мн.ч.': 'будем +'
        } if '1л' in args else {
            Defines.default: 'будешь +',
            'мн.ч.': 'будете +'
        } if '2л' in args else {
            Defines.default: 'будет +',
            'мн.ч.': 'будут +'
        }

    return {
        Defines.default: ask_func(word, path=path + ('единственное число', )),
        'мн.ч.': ask_func(word, path=path + ('множественное число', ))
    }
