from ._form import BaseForm, FormField


class WhoSearchForm(BaseForm):
    person_in_real_life = FormField('Человека из реальной жизни')
    just_play = FormField('Просто поиграть')
    team = FormField('Команду для праков')


class GenderForm(BaseForm):
    male = FormField('Парень')
    female = FormField('Девушка')


class WhoLookingForForm(BaseForm):
    guys = FormField('Парней')
    girls = FormField('Девушек')
    guys_and_girls = FormField('Парней и девушек')


class ConfirmForm(BaseForm):
    yes = FormField('Да')
    no = FormField('Нет')


class ProfileForm(BaseForm):
    edit_profile = FormField('1')
    edit_profile_photo = FormField('2')
    create_profile = FormField('3')
    start_searching = FormField('Начать поиск 🔍')


class TeammateCountryTypeForm(BaseForm):
    cis_countries = FormField('Страны СНГ')
    select_country = FormField('Выбрать страну')
    random_country = FormField('Любая страна')


class PlayLevelForm(BaseForm):
    beginner = FormField('Новичок')
    middle = FormField('Средний')
    high = FormField('Высокий')
    esports = FormField('Киберспорт')


who_search_form = WhoSearchForm()
gender_form = GenderForm()
who_looking_for_form = WhoLookingForForm()
confirm_form = ConfirmForm()
profile_form = ProfileForm()
teammate_country_type_form = TeammateCountryTypeForm()
play_level_form = PlayLevelForm()
