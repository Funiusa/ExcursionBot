from aiogram import types, Dispatcher


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запуск бота"),
            types.BotCommand("about", "Знакомство с ботом"),
            types.BotCommand("help", "Что такое антиэкскурсия?"),
            types.BotCommand("anti_excursions", "Выбрать антиэкскурсию"),
            types.BotCommand("commands", "Список команд"),
            types.BotCommand("registration", "Регистрация"),
        ]
    )
