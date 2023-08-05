"""A Russian text generator based on templating texts and word picking"""

__version__ = "0.5.0"

from WordProcessing.WordDict import WordDict
import stdio_rutext as IO


def main():
    db = WordDict()

    IO.db_init(db)

    try:
        IO.user_interact(db)
    finally:
        IO.db_save(db)


if __name__ == '__main__':
    main()
