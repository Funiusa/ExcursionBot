import asyncio

import quick_commands as commands
from db_utils import db
from config import POSTGRES_URI


async def db_test():
    await db.set_bind(POSTGRES_URI)
    await db.gino.drop_all()
    await db.gino.create_all()

    await commands.add_user(1, "Demos", "Oleg")
    await commands.add_user(345, "Denis", "Den")
    await commands.add_user(64565, "Mary", "Mariia")
    await commands.add_user(645663, "Gary", "Bob")

    users = await commands.select_all_users()
    print(users)

    count_users = await commands.count_users()
    print(count_users)

    user = await commands.select_user(1)
    print(user)

    await commands.update_user_name(1, "Demis")

    user = await commands.select_user(1)
    print(user)


loop = asyncio.get_event_loop()
loop.run_until_complete(db_test())
