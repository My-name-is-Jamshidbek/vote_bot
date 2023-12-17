"""
app file
"""
from aiogram.types import ContentType as ct, PreCheckoutQuery
from loader import dp

from apps.admin import *
from apps.user import *
from apps.login import *

from states import *

# cmd start
dp.register_message_handler(start)

# USER
# region
dp.register_callback_query_handler(user_region, state=User.region)

# condidate
dp.register_callback_query_handler(user_condidate, state=User.condidate)

# voice
dp.register_callback_query_handler(user_voice, state=User.voice)

# ADMIN APPS
dp.register_message_handler(admin_main, content_types=[ct.TEXT], state=Admin.main)

dp.register_message_handler(admin_channels_menu, content_types=[ct.TEXT], state=Admin.channels_menu)

dp.register_message_handler(admin_channels_delete, content_types=[ct.TEXT], state=Admin.channels_delete)

dp.register_message_handler(admin_channels_create, content_types=[ct.TEXT], state=Admin.channels_create)

dp.register_message_handler(admin_channels_create1, content_types=[ct.TEXT], state=Admin.channels_create1)

# ADMIN CANDIDATES
dp.register_message_handler(admin_candidates_menu, content_types=[ct.TEXT], state=Admin.candidates_menu)

dp.register_message_handler(admin_candidates_add1, content_types=[ct.TEXT], state=Admin.candidates_add1)

dp.register_message_handler(admin_candidates_add2, content_types=[ct.TEXT], state=Admin.candidates_add2)

dp.register_message_handler(admin_candidates_add3, content_types=[ct.TEXT], state=Admin.candidates_add3)

dp.register_message_handler(admin_candidates_add4, content_types=[ct.TEXT], state=Admin.candidates_add4)
