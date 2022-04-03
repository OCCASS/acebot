from collections import namedtuple
from typing import Union

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import _


class BaseForm:
    fields = None

    def __new__(cls, *args, **kwargs):
        __fields = {}
        __count = 1
        for var, value in cls.__dict__.items():
            if not var.startswith('__'):
                value.id = __count
                __fields[var] = value
                __count += 1

        _buttons = namedtuple('fields', list(__fields.keys()))
        cls.fields = _buttons(**__fields)
        return cls

    @classmethod
    async def validate_message(cls, message: str) -> bool:
        for button in cls.fields:
            if message == _(button.text):
                return True

        return False

    @classmethod
    async def get_keyboard(cls, row_width=1, exceptions=None) -> ReplyKeyboardMarkup:
        """
        :param row_width:
        :param exceptions: список идентификаторов полей которые надо исключить при создании клавиатуры
        """

        if exceptions is None:
            exceptions = []

        keyboard = ReplyKeyboardMarkup(row_width=row_width, resize_keyboard=True)
        fields = [field.text for field in cls.fields if field.id not in exceptions]
        for i in range(0, len(fields), row_width):
            keyboard.row(*fields[i:i + row_width])

        return keyboard

    @classmethod
    def get_callback_data(cls):
        return CallbackData(cls.__name__, 'id')

    @classmethod
    async def get_inline_keyboard(cls, callback_data=None, row_width=1):
        if callback_data is None:
            callback_data = cls.get_callback_data()

        keyboard = InlineKeyboardMarkup(row_width=row_width)
        buttons = [InlineKeyboardButton(text=field.text, callback_data=callback_data.new(field.id))
                   for field in cls.fields]
        for i in range(0, len(buttons), row_width):
            keyboard.row(*buttons[i:i + row_width])

        return keyboard

    @classmethod
    async def get_id_by_text(cls, text) -> Union[int, None]:
        for field in cls.fields:
            if text == _(field.text):
                return field.id

        return

    @classmethod
    async def get_by_id(cls, id: int):
        for field in cls.fields:
            if field.id == id:
                return field

        return


class FormField:
    def __init__(self, text, id_: int = None):
        self.text = text
        if id_ is None:
            self.id = -1
        else:
            self.id = id_

    def __repr__(self):
        return f'<FormField id={self.id}, text={self.text}>'
