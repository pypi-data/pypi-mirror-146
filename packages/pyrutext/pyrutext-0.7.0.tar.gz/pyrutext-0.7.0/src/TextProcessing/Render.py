from dataclasses import dataclass, field
import enum
import re
from WordProcessing.WordDict import WordDict


class ErrorGrade(enum.Enum):
    WARNING = enum.auto()
    ERROR = enum.auto()


class ErrorType(enum.Enum):
    VAR_INVALID_FORMAT = enum.auto()
    VAR_REDEFINED = enum.auto()
    WORD_NONE_FOUND = enum.auto()


@dataclass
class RenderException:
    grade: ErrorGrade
    type: ErrorType
    supplement: list[str] = field(default_factory=list)


class Renderer:
    def __init__(self, db: WordDict):
        self.__db = db
        self.__vars = dict()
        self.__exceptions = list()

    def __token_paste(self, matchobj):
        content = matchobj.group(0)[2:-2].split()
        if content[0] in self.__vars:
            if len(content) != 1:
                word_to_put = self.__db.get_form(self.__vars[content[0]], *content[1:])
            else:
                word_to_put = self.__db.get_form(self.__vars[content[0]])
        else:
            word_to_put = self.__db.get(*content)

        if word_to_put is None:
            self.__exceptions.append(RenderException(ErrorGrade.ERROR, ErrorType.WORD_NONE_FOUND, content))
        return word_to_put

    def render(self, text: str):
        self.__exceptions.clear()
        self.__vars.clear()

        if '\\' in text:
            vars_str, template = (part.strip() for part in text.split('\\', 1))
            for line in vars_str.splitlines():
                if '=' not in text:
                    self.__exceptions.append(RenderException(ErrorGrade.ERROR, ErrorType.VAR_INVALID_FORMAT, [line]))
                    continue
                var_id, var_val = (part.strip() for part in line.split('=', 1))
                if var_id in self.__vars:
                    self.__exceptions.append(RenderException(ErrorGrade.WARNING, ErrorType.VAR_REDEFINED, [var_id, self.__vars[var_id]]))
                word = self.__db.get(*var_val.split(), to_format=False)
                if word is None:
                    self.__exceptions.append(RenderException(ErrorGrade.ERROR, ErrorType.WORD_NONE_FOUND, [var_val]))
                    continue
                self.__vars[var_id] = word
        else:
            template = text.strip()

        result = re.sub(r'--[^-]+--', self.__token_paste, template)

        return result, self.__exceptions
