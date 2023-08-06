"""A Russian text generator based on templating texts and word picking"""

__version__ = "0.6.1"

from WordProcessing.WordDict import WordDict
import StdIO.db_yaml as DB
import StdIO.io_shell as IO
import asyncio


async def main():
    word_manager = WordDict()

    DB.init(word_manager)
    IO.init(word_manager)

    try:
        await IO.interact(word_manager)
    finally:
        DB.save(word_manager)


if __name__ == '__main__':
    asyncio.run(main())
