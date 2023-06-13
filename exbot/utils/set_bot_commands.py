from aiogram import types, Dispatcher


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Greetings"),
            types.BotCommand("help", "Help"),
            types.BotCommand("excursions", "List of all excursions"),
            types.BotCommand("registration", "Registration on the site"),
        ]
    )
