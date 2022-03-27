from ._menu import BaseMenu, MenuItem


class WhoSearchMenu(BaseMenu):
    person_in_real_life = MenuItem('Человека из реальной жизни')
    team = MenuItem('Команду для праков')
    just_play = MenuItem('Просто поиграть')


class GenderMenu(BaseMenu):
    male = MenuItem('Парень')
    female = MenuItem('Девушка')


class WhoLookingForMenu(BaseMenu):
    guys = MenuItem('Парней')
    girls = MenuItem('Девушек')
    guys_and_girls = MenuItem('Парней и девушек')


class IsCorrectMenu(BaseMenu):
    yes = MenuItem('Да')
    no = MenuItem('Нет')


class ProfileMenu(BaseMenu):
    edit_profile = MenuItem('1')
    edit_profile_photo = MenuItem('2')
    create_profile = MenuItem('3')
    start_searching = MenuItem('Начать поиск 🔍')


who_search_menu = WhoSearchMenu()
gender_menu = GenderMenu()
who_looking_for_menu = WhoLookingForMenu()
is_correct_menu = IsCorrectMenu()
profile_menu = ProfileMenu()
