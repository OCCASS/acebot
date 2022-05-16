from aiogram.dispatcher import FSMContext

from loader import dp, _
from aiogram import types

from utils.send import send_message


@dp.message_handler(state='*', content_types=types.ContentTypes.ANY)
async def process_all_messages(message: types.Message, state: FSMContext):
    await send_message(
        _('Вы зачем бота ломаете -_-. Не ломайте его пожалуйста, а если что-то сработало некорректно, '
          f'то отправьте пожалуйста скрин @ace_virtu.'))
