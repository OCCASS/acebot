from service.forms._form import BaseForm, FormField
from data.types import ProfileTypes, WhoLookingForTypes, GenderTypes
from loader import _


class ProfileTypeForm(BaseForm):
    person_in_real_life = FormField(_('Человека из реальной жизни'), id_=ProfileTypes.PERSON_IRL)
    just_play = FormField(_('Просто поиграть'), id_=ProfileTypes.JUST_PLAY)
    team = FormField(_('Команду для праков'), id_=ProfileTypes.TEAM)


class GenderForm(BaseForm):
    male = FormField(_('Парень'), id_=GenderTypes.GUY)
    female = FormField(_('Девушка'), id_=GenderTypes.GIRL)


class WhoLookingForForm(BaseForm):
    guys = FormField(_('Друзей'), id_=WhoLookingForTypes.GUYS)
    girls = FormField(_('Подруг'), id_=WhoLookingForTypes.GIRLS)
    guys_and_girls = FormField(_('Друзей и Подруг'), id_=WhoLookingForTypes.GUYS_AND_GIRLS)


class ConfirmForm(BaseForm):
    yes = FormField(_('Да'))
    no = FormField(_('Нет'))


class ProfileForm(BaseForm):
    edit_profile = FormField('1')
    edit_profile_photo = FormField('2')
    create_profile = FormField('3')
    start_searching = FormField(_('Начать поиск 🔍'))


class TeammateCountryTypeForm(BaseForm):
    cis_countries = FormField(_('Страны СНГ'))
    select_country = FormField(_('Выбрать страну'))
    random_country = FormField(_('Любая страна'))


class PlayLevelForm(BaseForm):
    beginner = FormField(_('Новичок'))
    middle = FormField(_('Средний'))
    high = FormField(_('Высокий'))
    esports = FormField(_('Киберспорт'))


class ProfileViewingForm(BaseForm):
    like = FormField('💗')
    next = FormField('👎️')
    send_message = FormField('💌')
    sleep = FormField('💤')


class AdmirerProfileViewingForm(BaseForm):
    like = FormField('💗')
    next = FormField('👎️')
    complain = FormField('⚠️')
    sleep = FormField('💤')


class EditSearchModificationForm(BaseForm):
    __name__ = 'edit_search_modifier'

    set_target_gender = FormField(_('Найти друзей или подруг'))
    set_target_games = FormField(_('Поискать людей из другой игры из моего города'))


class ReestablishProfileForm(BaseForm):
    reestablish = FormField(_('Восстановить'))
    delete = FormField(_('Удалить'))


class ReestablishManyProfilesForm(BaseForm):
    choose = FormField(_('Выбрать конкретную'))
    all = FormField(_('Восстановить все'))
    delete_all = FormField(_('Удалить все'))


class ShowFrom(BaseForm):
    show = FormField(_('Показать'))


class AgreeForm(BaseForm):
    agree = FormField(_('Хорошо'))


class ComplainTypeForm(BaseForm):
    __name__ = 'complain_type'

    material_for_adults = FormField(_('🔞 Материал для взрослых'))
    sale_of_goods = FormField(_('🛒 Продажа товаров и услуг'))
    does_not_answer = FormField(_('🔇 Не отвечает'))
    other = FormField(_('❓ Другое'))
    cancel = FormField(_('✖️ Отмена'))


class BanDurationForm(BaseForm):
    __name__ = 'ban_duration'

    one_day = FormField(_('На день'))
    one_month = FormField(_('На месяц'))
    forever = FormField(_('Навсегда'))
    null = FormField(_('Не банить'))


class OkForm(BaseForm):
    ok = FormField(_('Принять!'))


class LanguageForm(BaseForm):
    ru = FormField('🇷🇺 Русский')
    en = FormField('🇬🇧 English')
    uk = FormField('🇺🇦 Українська мова')


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
admirer_profile_viewing_form = AdmirerProfileViewingForm()
show_form = ShowFrom()
agree_form = AgreeForm()
complain_type_form = ComplainTypeForm()
ban_duration_form = BanDurationForm()
ok_form = OkForm()
language_form = LanguageForm()
