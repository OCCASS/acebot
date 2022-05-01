import datetime
import logging

from data.types import BanDurationTypes
from data.config import DAYS_IN_MONTH
import asyncio

from service.database.api import DatabaseApi
from service.database.create import create_database

db = DatabaseApi()


async def main():
    await create_database()
    while True:
        bans = await db.get_all_users_bans()
        for ban in bans:
            ban_at = ban.from_date
            ban_duration = None
            if ban.type == BanDurationTypes.ONE_DAY:
                ban_duration = datetime.timedelta(days=1)
            elif ban.type == BanDurationTypes.ONE_MONTH:
                ban_duration = datetime.timedelta(days=DAYS_IN_MONTH)

            if ban_duration:
                ban_ended = datetime.datetime.now() > ban_at + ban_duration
                if ban_ended:
                    await ban.delete()
                    logging.info(f'{ban.to_user_id} user deleted ban started at {ban_at}')

        await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(main())
