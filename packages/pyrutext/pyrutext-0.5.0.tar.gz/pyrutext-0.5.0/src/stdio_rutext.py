from WordProcessing.WordDict import *
import os.path
import yaml

__words_file = "words.yaml"


def db_init(db: WordDict):
    if os.path.isfile(__words_file):
        with open(__words_file, mode='r', encoding='utf-8') as wordsin:
            saved_words = yaml.load(wordsin, yaml.Loader)
            if type(saved_words) == dict:
                db.input(saved_words)


def db_save(db: WordDict):
    with open(__words_file, mode='a', encoding='utf-8') as wordsout:
        yaml.dump(db.flush(), wordsout, indent=2, allow_unicode=True)


def user_interact(db: WordDict):
    print('Введите слова:')
    while True:
        word = input()
        if len(word) == 0:
            break
        tokens = word.split()
        word = tokens[0]
        tags = tokens[1:] if len(tokens) > 1 else []

        response = db.insert(word, tags)
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

        auto_cancel = False
        match response.status:
            case Status.WORD_ALREADY_EXISTS:
                print(f'!! Это слово уже есть в списке.')
                print(f'   Его теги: {response.supplement}.')
                auto_cancel = True
            case Status.VERB_NO_PERFECTNESS:
                print('!! Пожалуйста, укажите завершённость глагола: совершённый "сов." или несовершённый "несов."')
                auto_cancel = True
            case Status.NO_TAGS:
                print('!! Теги добавляются при вводе. Например, "любить гл. несов."; "человек сущ. м.р."')
                auto_cancel = True
            case Status.NOUN_NO_GENDER:
                print('! Вы не указали род существительного (м.р.|с.р.|ж.р.|безл.).')
                print('  Выборка в тексте в основном требует род, что значит, ваше слово практически не будет показываться.')
            case Status.GOT_PHRASE:
                print('! Крайне не рекомендуем добавлять словосочетания.')

        if not auto_cancel:
            print('Добавлять слово? (пустой ввод, если да) ', end='')
            if len(input()) != 0:
                db.insert_cancel(word)
            else:
                db.insert_accept(word)
        else:
            db.insert_cancel(word)
        print()

    print('Введите теги:')
    while True:
        tags = input()
        if len(tags) == 0:
            break
        tags_set = set(tags.split())
        print(db.get(*tags_set))
        print()
