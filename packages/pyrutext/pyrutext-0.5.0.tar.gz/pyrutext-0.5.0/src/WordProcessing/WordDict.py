from .Util.Util import extract_all, rel_format
from . import Forms
from dataclasses import dataclass, field
import enum
import random


class Status(enum.Enum):
    OK = enum.auto()
    WORD_ALREADY_EXISTS = enum.auto()
    NO_TAGS = enum.auto()
    GOT_PHRASE = enum.auto()
    NOUN_NO_GENDER = enum.auto()
    VERB_NO_PERFECTNESS = enum.auto()
    NO_WORD_FOUND = enum.auto()


@dataclass
class Response:
    word: str
    tags: list[str] = field(default_factory=list)
    status: Status = Status.OK
    supplement: str = ''


class WordDict():

    __word_types = ('безл.', )
    __word_traits = ('абр', 'пинг', 'перс')

    def __init__(self):
        self.__words = dict()
        self.__floating_words = dict()
        self.__cache = []

    def delete(self, *args):
        for name in args:
            del self.__words[name]

    def get(self, *args):
        tags = list(args)

        forms = extract_all(tags, 'ед.ч.', 'мн.ч.', 'и.п.', 'р.п.', 'д.п.', 'в.п.', 'т.п.', 'п.п.', 'п.в.', 'н.в.', 'б.в.', '1л', '2л', '3л', to_pop=True)

        if 'гл.' in args:
            forms.extend(extract_all(tags, 'инф.', 'пов.', 'м.р.', 'с.р.', 'ж.р.', to_pop=True))
        elif 'пр.' in args:
            forms.extend(extract_all(tags, 'одуш.', 'неодуш.', 'м.р.', 'с.р.', 'ж.р.', to_pop=True))

        tag_correlations = tuple(filter(
            lambda word: all(tag in Forms.tags(self.__words, word) for tag in tags), self.__words.keys()
            )) if len(tags) > 0 else tuple(self.__words.keys())

        if len(tag_correlations) == 0:
            return

        word = random.choice(tag_correlations)

        return rel_format(word, Forms.lookup(self.__words[word], *forms))

    def input(self, extension: dict):
        self.__words.update(extension)

    def flush(self):
        if len(self.__cache) == 0:
            return

        cached_words = {}
        for key in self.__cache:
            cached_words[key] = self.__words[key]

        self.__cache.clear()

        return cached_words

    def output(self):
        return self.__words

    def insert(self, name: str, tags) -> Response:
        types = extract_all(tags, *self.__word_types, to_pop=True)
        for word_type in types:
            match word_type:
                case 'безл.':
                    tags.extend(('м.р.', 'ж.р.'))

        traits = extract_all(tags, *self.__word_traits, to_pop=False)
        for word_trait in traits:
            match word_trait:
                case 'абр' | 'пинг':
                    tags.append('нескл.')
                case 'перс':
                    tags.append('ед.ч.')

        tags = list(set(tags))
        self.__floating_words[name] = tags

        if name in self.__words:
            return Response(name, tags,
                            status=Status.WORD_ALREADY_EXISTS,
                            supplement=str(Forms.tags(self.__words, name)))

        if 'гл.' in tags:
            if 'сов.' not in tags and 'несов.' not in tags:
                return Response(name, tags, status=Status.VERB_NO_PERFECTNESS)

        if 'сущ.' in tags:
            if 'м.р.' not in tags and 'с.р.' not in tags and 'ж.р.' not in tags:
                return Response(name, tags, status=Status.NOUN_NO_GENDER)

        if len(name.split()) > 1:
            return Response(name, tags, status=Status.GOT_PHRASE)

        if len(tags) == 0:
            return Response(name, tags, status=Status.NO_TAGS)

        return Response(name, tags)

    def insert_accept(self, word: str):
        if word in self.__floating_words:
            self.__words[word] = Forms.construct_forms(word, *self.__floating_words[word])
            self.__cache.append(word)
            del self.__floating_words[word]
            return Response(word)

        return Response(word, status=Status.NO_WORD_FOUND)

    def insert_cancel(self, word: str):
        if word in self.__floating_words:
            del self.__floating_words[word]
            return Response(word)

        return Response(word, status=Status.NO_WORD_FOUND)
