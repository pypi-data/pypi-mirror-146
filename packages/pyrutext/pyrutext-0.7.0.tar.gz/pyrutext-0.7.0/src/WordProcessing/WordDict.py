from .Util.Util import extract_all, rel_format
from . import Forms, Defines
from dataclasses import dataclass, field
from typing import Callable
import enum
import random


class Status(enum.Enum):
    OK = enum.auto()
    INVALID_REFERENCE = enum.auto()
    REFERENCE_ALREADY_SET = enum.auto()
    WORD_ALREADY_EXISTS = enum.auto()
    NO_TAGS = enum.auto()
    GOT_PHRASE = enum.auto()
    NOUN_NO_GENDER = enum.auto()
    VERB_NO_PERFECTNESS = enum.auto()
    NO_WORD_FOUND = enum.auto()


@dataclass
class InsertResponse:
    word: str
    tags: list[str] = field(default_factory=list)
    status: Status = Status.OK
    supplement: str = ''


class WordDict():

    __word_types = ('безл.', )
    __word_traits = ('абр', 'пинг', 'перс')

    def __init__(self):
        self.__words = dict()
        self.__cache = []
        self.__confirm_func = Callable[[InsertResponse], bool]
        self.__ask_func = Callable[[str, list], str]

    def set_confirm_func(self, confirm_func=Callable[[InsertResponse], bool]):
        self.__confirm_func = confirm_func

    def set_ask_func(self, ask_func=Callable[[str, list], str]):
        self.__ask_func = ask_func

    def delete(self, *args):
        for name in args:
            del self.__words[name]

    def get(self, *args, to_format=True):
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
            return None

        word = random.choice(tag_correlations)

        return rel_format(word, Forms.lookup(self.__words[word], *forms)) if to_format else word

    def get_form(self, word: str, *args):
        return rel_format(word, Forms.lookup(self.__words[word], *args))

    def input(self, extension: dict):
        self.__words.update(extension)

    def flush(self):
        if len(self.__cache) == 0:
            return None

        cached_words = {}
        for key in self.__cache:
            cached_words[key] = self.__words[key]

        self.__cache.clear()

        return cached_words

    def output(self):
        return self.__words

    def insert(self, word: str, tags):
        types = extract_all(tags, *self.__word_types, to_pop=True)
        for word_type in types:
            if word_type == 'безл.':
                tags.extend(('м.р.', 'ж.р.'))

        traits = extract_all(tags, *self.__word_traits, to_pop=False)
        for word_trait in traits:
            if word_trait in ('абр', 'пинг'):
                tags.append('нескл.')
            elif word_trait == 'перс':
                tags.append('ед.ч.')

        tags = list(set(tags))

        reference = None
        for tag in tags:
            if tag[0] == '&':
                reference_to = tag[1:]
                if reference_to not in self.__words:
                    self.__confirm_func(InsertResponse(word, tags, Status.INVALID_REFERENCE, reference_to))
                    return
                else:
                    if reference is not None:
                        self.__confirm_func(InsertResponse(word, tags, Status.REFERENCE_ALREADY_SET, str((reference, reference_to))))
                        return
                    reference = reference_to

        response = InsertResponse(word, tags)
        if word in self.__words:
            response.status = Status.WORD_ALREADY_EXISTS
            response.supplement = str(Forms.tags(self.__words, word))
        elif 'гл.' in tags:
            if 'сов.' not in tags and 'несов.' not in tags:
                response.status = Status.VERB_NO_PERFECTNESS
        elif 'сущ.' in tags:
            if 'м.р.' not in tags and 'с.р.' not in tags and 'ж.р.' not in tags:
                response.status = Status.NOUN_NO_GENDER
        elif len(word.split()) > 1:
            response.status = Status.GOT_PHRASE
        elif len(tags) == 0:
            response.status = Status.NO_TAGS

        to_proceed = self.__confirm_func(response)
        if to_proceed:
            if reference is None:
                self.__words[word] = Forms.construct_forms(word, *tags, ask_func=self.__ask_func)
            else:
                if len(tags) == 1:
                    self.__words[word] = self.__words[reference]
                else:
                    tags.remove('&' + reference)
                    self.__words[word] = dict(self.__words[reference])
                    self.__words[word][Defines.tags_key] = tags
            self.__cache.append(word)
