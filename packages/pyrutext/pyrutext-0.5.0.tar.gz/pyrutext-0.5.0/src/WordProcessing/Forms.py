from .FormConstructors import Adj, Noun, Verb, Defines


def lookup(self, *args):
    if type(self) is not dict:
        return self

    default_key = Defines.default if Defines.default_key not in self else self[Defines.default_key]

    for arg in args:
        if arg in self:
            return lookup(self[arg], *args)

    value = self[default_key]
    return lookup(value, *args)


def tags(self: dict, word: str):
    if Defines.tags_key in self[word]:
        return self[word][Defines.tags_key]
    return []


def construct_forms(word: str, *args, path=()):
    if len(args) == 0:
        return '+'

    origin = {
        Defines.tags_key: list(args)
    }

    if 'гл.' in args:
        return {
            **origin,
            Defines.default: Verb.conjugable(word, *args, path=path),
            'пов.': Verb.imperative(word, path=path + ('Повелительное наклонение', )),
            'инф.': '+'
        }
    elif 'сущ.' in args:
        return {
            **origin,
            Defines.default: '+' if 'нескл.' in args else Noun.declined(word, *args, path=path)
        }
    elif 'пр.' in args:
        return {
            **origin,
            Defines.default: Adj.singular(word, path=path + ('Единственное число', )),
            'мн.ч.': Adj.plural(word, path=path + ('Множественное число', ))
        }
    else:
        return {
            **origin,
            Defines.default: '+'
        }
