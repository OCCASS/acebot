import datetime

from loader import db
from data.types import BanDurationTypes
from data.config import DAYS_IN_MONTH
import asyncio


async def main():
    while True:
        bans = await db.get_all_users_bans()
        for ban in bans:
            ban_at = ban.from_date
            ban_duration = None
            if ban.ban_type == BanDurationTypes.ONE_DAY:
                ban_duration = datetime.timedelta(days=1)
            elif ban.ban_type == BanDurationTypes.ONE_MONTH:
                ban_duration = datetime.timedelta(days=DAYS_IN_MONTH)

            if ban_duration:
                ban_ended = datetime.datetime.now() > ban_at + ban_duration
                if ban_ended:
                    await ban.delete()

        await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(main())
