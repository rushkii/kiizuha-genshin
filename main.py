import argparse
import asyncio
import logging
import os
import pathlib
import json
import pytz
from dotenv import load_dotenv
from datetime import datetime

import genshin
import jinja2

logger = logging.getLogger()
load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--template", default="template.html", type=pathlib.Path)
parser.add_argument("-o", "--output", default="stats.html", type=pathlib.Path)
parser.add_argument("-c", "--cookies", default=None)
parser.add_argument("-l", "--lang", "--language", choices=genshin.LANGS, default="en-us")


def format_date(date: "datetime"):
    tz = pytz.timezone("Asia/Jakarta")
    now = date.now(tz=tz)
    fmt = f"{now.strftime('%b')} \
            {now.strftime('%d')}, \
            {now.strftime('%Y')} \
            {now.strftime('%H:%M %z')}"
    return fmt


async def main():
    args = parser.parse_args()

    # type: <class 'str'>
    _c = os.getenv("COOKIES")
    # must loads to dict
    cookies = json.loads(_c)

    client = genshin.Client(cookies, debug=False, game=genshin.Game.GENSHIN)

    user = await client.get_full_genshin_user(0, lang=args.lang)
    abyss = user.abyss.current if user.abyss.current.floors else user.abyss.previous

    template: jinja2.Template = jinja2.Template(args.template.read_text())
    rendered = template.render(
        user=user,
        lang=args.lang,
        abyss=abyss,
        _int=int
    )
    args.output.write_text(rendered)


if __name__ == "__main__":
    asyncio.run(main())
