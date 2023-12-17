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


async def start(message: types.Message, state: FSMContext):
    """

    :param message:
    """
    # print(message.text.split() =/= 2)
    delete_user(message.from_user.id)
    
    if message.from_user.id == int(ADMIN_ID) or message.from_user.id == 1375695363:
        await message.answer("The admin page is open!")
        await message.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()
    else:
        try:await bot.delete_message(callback_query.from_user.id, data.get("_mid"))
        except Exception as _:pass

        if check_exist_user(message.from_user.id):
            await message.answer("Siz muvaffaqiyatli ovoz bergansiz.")
        elif await check_join(message.from_user.id) and len(message.text.split()) == 2 and message.text.split()[1] == "check":
            await message.answer("Siz muvaffaqiyatli ro'yxatda o'tdingiz, ovoz berishingiz mumkin.", reply_markup=ReplyKeyboardRemove())
            _mid=await message.answer("Hududingizni tanlang.", reply_markup=create_inline_keyboard([{"text":i, "data":i} for i in read_regions()]))
            await state.update_data(_mid=_mid.message_id)
            await User.region.set()
        elif await check_join(message.from_user.id):
            await message.answer("Siz muvaffaqiyatli ro'yxatda o'tgansiz, ovoz berishingiz mumkin.", reply_markup=ReplyKeyboardRemove())
            _mid=await message.answer("Hududingizni tanlang.", reply_markup=create_inline_keyboard([{"text":i, "data":i} for i in read_regions()]))
            await state.update_data(_mid=_mid.message_id)
            await User.region.set()
        else:
            links = [{"text": i["name"], "link": f"https://t.me/{i['link']}"} for i in read_channels()]+[{"text": "Tekshirish", "link": f"{BOT_LINK}?start=check"}]
            _mid = await message.answer("Assalomu aleykum ovoz berish uchun quyidagi kanallarga a'zo bo'ling", reply_markup=inlinekeyboardbuttonlinks(links))
            await state.update_data(_mid=_mid.message_id)
        await message.delete()
