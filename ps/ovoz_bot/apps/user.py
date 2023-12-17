# """
# login apps
# """
from loader import bot, dp
from buttons import *
from database import *
from states import *
from config import *
from .additional import *

from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.types import ReplyKeyboardRemove


async def user_region(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:await bot.delete_message(callback_query.from_user.id, data.get("_mid"))
    except Exception as _:pass
    await callback_query.answer()  # Yaqin kelgan so'rovni qabul qilish
    m = callback_query.data
    if m in regions_list:
        _mid = await bot.send_message(callback_query.from_user.id, "Universitet/Institut tanlang", reply_markup=create_inline_keyboard([{"text": i, "data": i} for i in read_candidates_short_names(m)]+[{"text":"Hududni o'zgartirish","data":"change_region"}]))
        await state.update_data(_mid=_mid.message_id)
        await state.update_data(selected_region=m)
        await User.condidate.set()

async def user_condidate(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:await bot.delete_message(callback_query.from_user.id, data.get("_mid"))
    except Exception as _:pass
    await callback_query.answer()  # Yaqin kelgan so'rovni qabul qilish
    m = callback_query.data
    region = data.get("selected_region")
    if m in read_candidates_short_names(region):
        get_condidate_data_ = get_candidate_data(region, m)
        _mid = await bot.send_message(callback_query.from_user.id, f"{get_candidate_full_name(region, m)} {region}da joylashgan.\n\nQuyida ta'lim muassasasi faoliyati bilan tanishib ushbu ta'lim muassasasiga ovoz berishingiz mumkin.\n\nHozirda ushbu ta'lim muassasasi uchun berilgan ovozlar soni {get_condidate_data_[1]} ga teng.", reply_markup=get_inline_keyboard(get_condidate_data_))
        await state.update_data(_mid=_mid.message_id)
        await User.voice.set()
    elif m == "change_region":
        _mid=await bot.send_message(callback_query.from_user.id, "Hududingizni tanlang.", reply_markup=create_inline_keyboard([{"text":i, "data":i} for i in read_regions()]))
        await state.update_data(_mid=_mid.message_id)
        await User.region.set()

async def user_voice(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:await bot.delete_message(callback_query.from_user.id, data.get("_mid"))
    except Exception as _:pass
    await callback_query.answer()  # Yaqin kelgan so'rovni qabul qilish
    m = callback_query.data
    region = data.get("selected_region")
    if m.split("_")[0] == "voice" and not check_exist_user(callback_query.from_user.id) and len(m.split("_"))==2:
        add_new_user(callback_query.from_user.id, callback_query.from_user.full_name,m.split("_")[1])
        add_a_voice_candidate(m.split("_")[1])
        get_condidate_data_ = get_candidate_data_id(m.split("_")[1])
        await bot.send_message(callback_query.from_user.id, f"{get_condidate_data_[2]} ga muvaffaqiyatli ovoz berdingiz. Endilikda ushbu ta'lim muassasasi uchun berilgan ovozlar soni {get_condidate_data_[1]} ga teng.")
        await state.finish()
    elif m == "change_condidate":
        m = data.get("selected_region")
        _mid = await bot.send_message(callback_query.from_user.id, "Universitet/Institut tanlang", reply_markup=create_inline_keyboard([{"text": i, "data": i} for i in read_candidates_short_names(m)]+[{"text":"Hududni o'zgartirish","data":"change_region"}]))
        await state.update_data(_mid=_mid.message_id)
        await User.condidate.set()
