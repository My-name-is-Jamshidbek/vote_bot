# """
# admin apps
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

async def admin_main(message: types.Message, state: FSMContext):
    """
    :param message:
    :param state:
    """
    if message.text == 'Channels':
        channels = read_channels()
        if channels:
            ch = ""
            for i in channels: ch+='Name: ' + i['name'] + ' Link: ' + i['link'] + '\n'
            await message.answer(f"List of available channels:", reply_markup=keyboardbutton(['Add', 'Remove', 'Back']))
            await message.answer(ch)
        else:
            await message.answer("No channels available!", reply_markup=keyboardbutton(['Add', 'Back']))
        await Admin.channels_menu.set()
    elif message.text == "Candidates":
        regions = read_regions()
        if regions:
            await message.answer(f"Select an region", reply_markup=keyboardbutton(regions+['Add', 'Back']))
        else:
            await message.answer("No candidates available!", reply_markup=keyboardbutton(['Add', 'Back']))
        await Admin.candidates_menu.set()

async def admin_candidates_menu(m: types.Message, state: FSMContext):
    if m.text == "Back":
        await m.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()
    elif m.text == "Add":
        await m.answer("Select a region", reply_markup=keyboardbutton(regions_list))
        await Admin.candidates_add1.set()

async def admin_candidates_add1(m: types.Message, state: FSMContext):
    if m.text == "Back":
        await m.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()
    elif m.text in regions_list:
        await state.update_data(selected_region=m.text)
        await m.answer("Enter the short name of the candidate", reply_markup=keyboardbutton(["Back"]))
        await Admin.candidates_add2.set()
    

async def admin_candidates_add2(m: types.Message, state: FSMContext):
    if m.text == "Back":
        await m.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()
    elif len(m.text) < 20:
        await state.update_data(selected_short_name=m.text)
        await m.answer("Enter the full name of the candidate", reply_markup=keyboardbutton(["Back"]))
        await Admin.candidates_add3.set()
    else:
        await m.answer("Please enter the short name of the condidates! len < 20")    

async def admin_candidates_add3(m: types.Message, state: FSMContext):
    if m.text == "Back":
        await m.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()
    elif len(m.text) > 5:
        await state.update_data(selected_full_name=m.text)
        await m.answer("Enter the video url for introduction of the candidate", reply_markup=keyboardbutton(["Back"]))
        await Admin.candidates_add4.set()
    else:
        await m.answer("Please enter the short name of the condidates! len < 20")    

async def admin_candidates_add4(m: types.Message, state: FSMContext):
    if m.text == "Back":
        await m.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()
    elif len(m.text) < 200:
        try:
            data = await state.get_data()
            _r = data.get("selected_region")
            _sh = data.get("selected_short_name")
            _f = data.get("selected_full_name")
            create_candidate(_sh, _f, _r, m.text)
            await m.answer("The candidate has successfully joined!")
            await m.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
            await Admin.main.set()
        except Exception as e:
            print(e) 
            await m.answer("The candidate did not join successfully!")
            await m.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
            await Admin.main.set()
    else:
        await m.answer("Please enter the full name of the condidates! len < 20")    
    

async def admin_channels_menu(message: types.Message, state: FSMContext):
    """
    :param message:
    :param state:
    """
    if message.text == 'Add':
        await message.answer("Enter a channel name", reply_markup=keyboardbutton(['Back']))
        await Admin.channels_create.set()
    if message.text == 'Remove':
        await message.answer("Select one of the channels", reply_markup=keyboardbutton([i["name"] for i in read_channels()]+["Back"]))
        await Admin.channels_delete.set()
    if message.text == 'Back':
        await message.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()

async def admin_channels_delete(message: types.Message, state: FSMContext):
    """
    :param message:
    :param state:
    """
    if message.text == 'Back':
        await message.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()
    elif message.text in [i["name"] for i in read_channels()]:
        delete_channel(message.text)
        await message.answer("Channel removed successfully")
        await message.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()

async def admin_channels_create(message: types.Message, state: FSMContext):
    """
    :param message:
    :param state:
    """
    if message.text == 'Back':
        await message.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()
    else:
        await state.update_data(channel_add=message.text)
        await message.answer("Enter the channel address", reply_markup=keyboardbutton(['Back']))
        await Admin.channels_create1.set()        

async def admin_channels_create1(message: types.Message, state: FSMContext):
    """
    :param message:
    :param state:
    """
    if message.text == 'Back':
        await message.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()
    elif await check_join_a(channel_id=message.text, user_id=str(message.from_user.id)):
        data = await state.get_data()
        create_channel(name=data["channel_add"],link=message.text)
        await message.answer("Channel added successfully")
        await message.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()
    else:
        await message.answer("Please resend the channel link, the bot is full admin and you have joined the channel and the link")        
