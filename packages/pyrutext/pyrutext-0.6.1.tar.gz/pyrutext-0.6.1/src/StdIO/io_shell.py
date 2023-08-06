from WordProcessing.WordDict import *
import asyncio


def confirm_word(response: InsertResponse) -> bool:
    print(f'Базовая форма слова: "{response.word}".')
    print('Часть речи: ', end='')
    if 'гл.' in response.tags:
        print('глагол.')
    elif 'пр.' in response.tags:
        print('прилагательное/причастие.')
    elif 'сущ.' in response.tags:
        print('существительное.')
    else:
        print('другое (наречие/деепричастие/...)')
    print(f'Теги: {response.tags}.')

    auto_cancel = True
    if response.status == Status.REFERENCE_ALREADY_SET:
        print(f'!! Нельзя ставить более одного указателя.')
        print(f'   Есть конфликт тегов: {response.supplement}.')
    elif response.status == Status.INVALID_REFERENCE:
        print(f'!! Тег \'{response.supplement}\' указывает на отсутствующее в словаре слово.')
    elif response.status == Status.WORD_ALREADY_EXISTS:
        print(f'!! Это слово уже есть в списке.')
        print(f'   Его теги: {response.supplement}.')
    elif response.status == Status.VERB_NO_PERFECTNESS:
        print('!! Пожалуйста, укажите завершённость глагола: совершённый "сов." или несовершённый "несов."')
    elif response.status == Status.NO_TAGS:
        print('!! Теги добавляются при вводе. Например, "любить гл. несов."; "человек сущ. м.р."')
    elif response.status == Status.NOUN_NO_GENDER:
        print('! Вы не указали род существительного (м.р.|с.р.|ж.р.|безл.).')
        print('  Выборка в тексте в основном требует род, что значит, ваше слово практически не будет показываться.')
        auto_cancel = False
    elif response.status == Status.GOT_PHRASE:
        print('! Крайне не рекомендуем добавлять словосочетания.')
        auto_cancel = False
    elif response.status == Status.OK:
        auto_cancel = False
    else:
        print(f'!! Неизвестный статус "{response.status.name}".')
        print(f'   Дополнительная информация: "{response.supplement}".')

    if auto_cancel:
        return False
    print('Добавлять слово? (пустой ввод, если да) ', end='')
    return False if len(input()) != 0 else True


def ask_form(word: str, path=()) -> str:
    print(path[0], end='')
    for dir in path[1:]:
        print(f', {dir}', end='')
    print(f' для слова "{word}": ', end='')
    return input()


async def interact(db: WordDict):
    print('Введите слова:')
    while True:
        word = input()
        if len(word) == 0:
            break
        tokens = word.split()
        word = tokens[0]
        tags = tokens[1:] if len(tokens) > 1 else []

        await asyncio.to_thread(db.insert, word, tags)
        print()

    print('Введите теги:')
    while True:
        tags = input()
        if len(tags) == 0:
            break
        tags_set = set(tags.split())
        print(db.get(*tags_set))
        print()


def init(db: WordDict):
    db.set_confirm_func(confirm_word)
    db.set_ask_func(ask_form)
