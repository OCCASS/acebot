from loader import db, _
from data.config import COMPLAINS_COUNT_TO_NOTIFY_ADMINS, ADMINS
from utils.send import send_message
from keyboards.inline.keyboard import get_show_intruder_profile_keyboard


async def notify_complain_admins(profile_id: int):
    complains_count = await db.get_profile_complains_count(profile_id)
    if complains_count >= COMPLAINS_COUNT_TO_NOTIFY_ADMINS:
        for admin_id in ADMINS:
            keyboard = await get_show_intruder_profile_keyboard(profile_id)
            await send_message(_('Есть жалобы на профиль...'), user_id=admin_id, reply_markup=keyboard)
