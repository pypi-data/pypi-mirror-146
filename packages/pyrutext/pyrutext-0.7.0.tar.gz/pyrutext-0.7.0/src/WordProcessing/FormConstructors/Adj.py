from .. import Defines


def singular(word: str, *, path=(), ask_func):
    mascul_neu_preset = {
        'р.п.': ask_func(word, path=path + ('мужской/средний род', 'родительный падеж')),
        'д.п.': ask_func(word, path=path + ('мужской/средний род', 'дательный падеж')),
        'т.п.': ask_func(word, path=path + ('мужской/средний род', 'творительный падеж')),
        'п.п.': ask_func(word, path=path + ('мужской/средний род', 'предложный падеж'))
    }

    mascul_preset = mascul_neu_preset.copy()
    mascul_preset[Defines.default] = '+'
    mascul_preset['в.п.'] = {
        Defines.default: mascul_preset[Defines.default],
        'одуш.': mascul_preset['р.п.']
    }

    neu_preset = mascul_neu_preset.copy()
    neu_preset[Defines.default] = ask_func(word, path=path + ('средний род', 'именительный падеж'))
    neu_preset['в.п.'] = {
        Defines.default: neu_preset[Defines.default],
        'одуш.': neu_preset['р.п.']
    }

    fem_case = ask_func(word, path=path + ('женский род', 'родительный/дательный/творительный/предложный падеж'))

    return {
        Defines.default: mascul_preset,
        'с.р.': neu_preset,
        'ж.р.': {
            Defines.default: ask_func(word, path=path + ('женский род', 'именительный падеж')),
            'р.п.': fem_case,
            'д.п.': fem_case,
            'в.п.': ask_func(word, path=path + ('женский род', 'винительный падеж')),
            'т.п.': fem_case,
            'п.п.': fem_case
        }
    }


def plural(word: str, *, path=(), ask_func):
    nominative = ask_func(word, path=path + ('именительный падеж', ))
    genitive = ask_func(word, path=path + ('родительный падеж', ))
    return {
        Defines.default: nominative,
        'р.п.': genitive,
        'д.п.': ask_func(word, path=path + ('дательный падеж', )),
        'в.п.': {
            Defines.default: nominative,
            'одуш.': genitive
        },
        'т.п.': ask_func(word, path=path + ('творительный падеж', )),
        'п.п.': ask_func(word, path=path + ('предложный падеж', )),
    }
