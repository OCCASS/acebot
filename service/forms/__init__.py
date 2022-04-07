from service.forms._form import BaseForm, FormField
from data.types import ProfileTypes, WhoLookingForTypes, GenderTypes


class ProfileTypeForm(BaseForm):
    person_in_real_life = FormField('Человека из реальной жизни', id_=ProfileTypes.PERSON_IRL)
    just_play = FormField('Просто поиграть', id_=ProfileTypes.JUST_PLAY)
    team = FormField('Команду для праков', id_=ProfileTypes.TEAM)


class GenderForm(BaseForm):
    male = FormField('Парень', id_=GenderTypes.GUY)
    female = FormField('Девушка', id_=GenderTypes.GIRL)


class WhoLookingForForm(BaseForm):
    guys = FormField('Парней', id_=WhoLookingForTypes.GUYS)
    girls = FormField('Девушек', id_=WhoLookingForTypes.GIRLS)
    guys_and_girls = FormField('Парней и девушек', id_=WhoLookingForTypes.GUYS_AND_GIRLS)


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


class ProfileViewingForm(BaseForm):
    like = FormField('💗')
    next = FormField('👎️')
    send_message = FormField('💌')
    sleep = FormField('💤')


class EditSearchModificationForm(BaseForm):
    __name__ = 'edit_search_modifier'

    set_target_gender = FormField('Поискать парней и девушек из моего города')
    set_target_games = FormField('Поискать людей из другой игры из моего города')


class ReestablishProfileForm(BaseForm):
    reestablish = FormField('Восстановить')
    delete = FormField('Удалить')


class ReestablishManyProfilesForm(BaseForm):
    choose = FormField('Выбрать конкретную')
    all = FormField('Восстановить все')
    delete_all = FormField('Удалить все')


who_search_form = ProfileTypeForm()
gender_form = GenderForm()
who_looking_for_form = WhoLookingForForm()
confirm_form = ConfirmForm()
profile_form = ProfileForm()
teammate_country_type_form = TeammateCountryTypeForm()
play_level_form = PlayLevelForm()
profile_viewing_form = ProfileViewingForm()
edit_search_modification_form = EditSearchModificationForm()
reestablish_form = ReestablishProfileForm()
reestablish_many_from = ReestablishManyProfilesForm()
