"""
config variables
"""
import os
from dotenv import load_dotenv


# .env faylidagi o'zgaruvchilarni yuklash
load_dotenv()

# TOKEN, ADMIN_ID, va KEY o'zgaruvchilarini .env faylidan yuklash
# TOKEN = os.getenv('TOKEN')
TOKEN = "6875613027:AAE_eJsTB_IHmvNri_kzwaXPrCgW7DHZBas"
ADMIN_ID = "2081653869"
# ADMIN_ID = os.getenv('ADMIN_ID')
# KEY = os.getenv('KEY')
vote_text = "So'rovnoma !\n\nO'zbekiston yoshlar ittifoqi Xorazm viloyati Kengashi tomonidan tanlov e'lon qilinadi.\n\nJoriy yilda Xorazm viloyatidagi qaysi Oliy ta'lim muassasalari yoshlar ittifoqi boshlang'ich tashkiloti jamoasi faol, tashabbuskor va samarali faoliyat olib borgan?\n\nTanlovda sizning ovozingiz muhim o'z jamoangiz uchun ovoz bering\n\nSo'rovnomada g'olib bo'lgan yetakchilar qimmatbaho sovg'alar bilan taqdirlanadi.\n\nOvoz berish 20-dekabr soat 20:00 gacha davom etadi.\n\nBizning sahifalarimiz"
# BOT_LINK = os.getenv('BOT_LINK')
BOT_LINK = "https://t.me/vooter_xorezm_urgench_bot"
ERRORS_SEND = False
ADMIN_USER = 'https://t.me/mal_un'
WEB_SAYT = 'https://github.com/My-name-is-Jamshidbek'
msg_id = 469
chat_id = 2081653869
