from WordProcessing.WordDict import *
import os.path
import yaml

__words_file = "words.yaml"


def yaml_compress():
    if os.path.isfile(__words_file):
        saved_words = dict()
        with open(__words_file, mode='r', encoding='utf-8') as wordsin:
            saved_words = yaml.load(wordsin, yaml.Loader)
            if saved_words is not dict:
                return
            hashed = dict()
            hashed_sub = dict()
            for key, value in saved_words.items():
                if type(value) is not dict:
                    continue
                hash_full = hash(str(value))
                if hash_full in hashed:
                    saved_words[key] = saved_words[hashed[hash_full]]
                    continue
                hashed[hash_full] = key

                for subkey, subvalue in value.items():
                    if type(subvalue) is str:
                        continue
                    hash_sub = hash(str(subvalue))
                    if hash_sub in hashed_sub:
                        saved_words[key][subkey] = saved_words[hashed_sub[hash_sub][0]][hashed_sub[hash_sub][1]]
                        continue
                    hashed_sub[hash_sub] = (key, subkey)

        with open(__words_file, mode='w', encoding='utf-8') as wordsout:
            yaml.dump(saved_words, wordsout, indent=2, allow_unicode=True)


def init(db: WordDict):
    if os.path.isfile(__words_file):
        with open(__words_file, mode='r', encoding='utf-8') as wordsin:
            saved_words = yaml.load(wordsin, yaml.Loader)
            if type(saved_words) == dict:
                db.input(saved_words)


def save(db: WordDict, *, to_compress: bool = True):
    with open(__words_file, mode='a', encoding='utf-8') as wordsout:
        cache = db.flush()
        if cache is not None:
            yaml.dump(cache, wordsout, indent=2, allow_unicode=True)
    if to_compress:
        yaml_compress()
