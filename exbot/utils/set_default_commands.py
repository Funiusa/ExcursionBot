from aiogram import Dispatcher, types


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запуск бота"),
            types.BotCommand("help", "Инструкция"),
            types.BotCommand("anti_excursions", "Антиэкскурсии"),
            types.BotCommand("commands", "Список команд"),
            types.BotCommand("registration", "Регистрация"),
        ]
    )
