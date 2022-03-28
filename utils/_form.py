from collections import namedtuple
from typing import Union

from aiogram.types import ReplyKeyboardMarkup

from loader import _


class BaseForm:
    buttons = None

    def __new__(cls, *args, **kwargs):
        __buttons = {}
        __count = 1
        for var, value in cls.__dict__.items():
            if not var.startswith('__'):
                value.id = __count
                __buttons[var] = value
                __count += 1

        _buttons = namedtuple('buttons', list(__buttons.keys()))
        cls.buttons = _buttons(**__buttons)
        return cls

    @classmethod
    async def validate_message(cls, message: str) -> bool:
        for button in cls.buttons:
            if message == _(button.text):
                return True

        return False

    @classmethod
    async def get_as_keyboard(cls, row_width=1, exceptions=None) -> ReplyKeyboardMarkup:
        """
        :param row_width:
        :param exceptions: список идентификаторов полей которые надо исключить при создании клавиатуры
        """

        if exceptions is None:
            exceptions = []

        keyboard = ReplyKeyboardMarkup(row_width=row_width, resize_keyboard=True)
        buttons = [button.text for button in cls.buttons if button.id not in exceptions]
        for i in range(0, len(buttons), row_width):
            keyboard.row(*buttons[i:i + row_width])

        return keyboard

    @classmethod
    async def get_id_by_text(cls, text) -> Union[int, None]:
        for button in cls.buttons:
            if text == _(button.text):
                return button.id

        return

    @classmethod
    async def get_by_id(cls, id: int):
        for button in cls.buttons:
            if button.id == id:
                return button

        return


class FormField:
    def __init__(self, text):
        self.text = text
        self.id = -1

    def __repr__(self):
        return f'<MenuItem id={self.id}, text={self.text}>'
