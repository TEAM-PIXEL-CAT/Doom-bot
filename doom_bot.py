"""
TIPO DOOM: a 3D shooter inside a Telegram HTML widget (Bot API 10.4).

    pip install "git+https://github.com/aiogram/aiogram@refs/pull/2004/head"
    BOT_TOKEN=123:ABC python doom_bot.py

Commands: /start or /doom sends the intro message and the game.

The widget is only code. Its art comes from the bot (themes.py):
- level 1 travels with the message as public_data;
- when the player walks into the exit door, the widget asks the bot "lv:N"
  and the bot answers with that level's pack (palette, monster, wall colours,
  monster stats, name). If the bot does not answer, the level keeps the old theme.

Edit the game in src/doom.html, the art in themes.py, then run:
    python minify.py && python check_widgets.py
"""
import asyncio
import logging
import os
import re
import zlib
from pathlib import Path

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message, WidgetQuery

from themes import pack

HTML = (Path(__file__).parent / "widgets" / "doom.html").read_text(encoding="utf-8")
assert len(HTML.encode()) <= 32768 and len(zlib.compress(HTML.encode(), 9)) <= 4096, "widget exceeds the size limit"

INTRO = (
    "<b>🔥 TIPO DOOM</b>\n"
    "A tiny first-person shooter that lives right inside the next message.\n\n"
    "<b>Your goal:</b> find the <b>green door</b> on each level and walk into it. "
    "Every level is a fresh random maze, and the world changes as you go: "
    "the catacombs, then a tech base, then hell itself, and round again, harder each time.\n\n"
    "<b>Watch out:</b> monsters wake up the moment you see them and come for you. "
    "Shoot them before they get close. "
    "Pick up medkits and ammo boxes along the way. Barrels and pillars block your path.\n\n"
    "<b>Controls</b>\n"
    "▲ ▼ move forward / back\n"
    "◀ ▶ step sideways\n"
    "⟲ ⟳ turn\n"
    "FIRE shoot (hold for auto-fire)\n\n"
    "Slide your finger from button to button, and use both thumbs at once.\n"
    "Press <b>FIRE</b> to start 👇"
)

router = Router()


@router.message(Command("start", "doom"))
async def doom(message: Message, bot: Bot) -> None:
    await message.answer(INTRO, parse_mode="HTML")
    # allow_queries: the widget may ask for the next level's pack
    await bot.send_widget(chat_id=message.chat.id, html=HTML, public_data=pack(1), allow_queries=True)


@router.widget_query()
async def next_level(query: WidgetQuery) -> None:
    m = re.fullmatch(r"lv:(\d{1,4})", query.data or "")
    await query.answer(data=pack(int(m.group(1))) if m else None)


async def main() -> None:
    bot = Bot(os.environ["BOT_TOKEN"])
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
