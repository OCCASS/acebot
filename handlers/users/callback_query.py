from aiogram.dispatcher import FSMContext

from loader import dp, db, _
from states import States
from keyboards.inline.laguage import callback
from keyboards.default.keyboard import get_good_keyboard
from aiogram import types
from utils.send import send_message


@dp.callback_query_handler(callback.filter(), state=States.language)
async def process_language_keyboard(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    locale = callback_data.get('locale')
    await db.set_user_locale(query.from_user.id, locale)

    keyboard = await get_good_keyboard()
    await send_message(
        _('Данный бот создан энтузиастами, у нас нету многолетнего опыта в программирование и создание ботов - '
          'мы просто любим игры и хотели бы найти кого-то из наших городов. В боте никогда не придется платить, '
          'что бы увидеть кто вам поставил лайк и найти взаимную симпатию, все будет абсолютно бесплатно и '
          'ограничиваться только железом что бы не было спамеров, но за это будем у вас просить поддержать наши '
          '“возможных” будущих спонсоров и возможно будем держаться на донатах! '
          'На данный момент лучшей поддержкой для нас будет заказать буст у @boost_ace'), reply_markup=keyboard)
    await state.set_state(States.introduction)
