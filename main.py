import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


REMOVEBG_API = os.environ.get("REMOVEBG_API", "")
UNSCREEN_API = os.environ.get("UNSCREEN_API", "")
PATH = "./DOWNLOADS/"

Bot = Client(
    "Remove Background Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

START_TEXT = """Hello {},
I am a media background remover bot. Send me a photo I will send the photo without background.
Made by @Oxyver_Owner"""
HELP_TEXT = """**More Help**
- Just send me a photo
- I will download it
- I will send the photo without background
Made by @Oxyver_Owner"""
ABOUT_TEXT = """
- **Bot :** `Backround Remover Bot`
- **Creator :** [꧁𒆜🅻🆄🅲🅺🆈𒆜꧂](https://telegram.me/Oxyver_Owner)
- **Channel :** [Click](https://telegram.me/B4U_movies_in_hindi)
- **Source :** [Contact here](https://telegram.me/Oxyver_Owner)
- **Language :** [Python3](https://python.org)
- **Library :** [Pyrogram](https://pyrogram.org)"""
START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Channel', url='https://telegram.me/B4U_movies_in_hindi'),
            InlineKeyboardButton('Feedback', url='https://telegram.me/Oxyver_Support')
        ],
        [
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)
HELP_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)
ABOUT_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)
ERROR_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)
BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Join Updates Channel', url='https://telegram.me/TeluguDubbedHorrorMovies2')
        ]
    ]
)


@Bot.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.message.delete()


@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS
    )


@Bot.on_message(filters.private & (filters.photo | filters.video | filters.document))
async def remove_background(bot, update):
    if not REMOVEBG_API:
        await update.reply_text(
            text="Error :- Remove BG Api is error",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=ERROR_BUTTONS
        )
        return
    await update.reply_chat_action("typing")
    message = await update.reply_text(
        text="Processing",
        quote=True,
        disable_web_page_preview=True
    )
    new_file = PATH + str(update.from_user.id) + "/"
    new_file_name = new_file + "no_bg."
    if update.photo or (update.document and "image" in update.document.mime_type):
        new_file_name += "png"
        file = await update.download(PATH+str(update.from_user.id))
        await message.edit_text(
            text="Photo downloaded successfully. Now removing background.",
            disable_web_page_preview=True
        )
        new_document = removebg_image(file)
    elif update.video or (update.document and "video" in update.document.mime_type):
        new_file_name += "webm"
        file = await update.download(PATH+str(update.from_user.id))
        await message.edit_text(
            text="Photo downloaded successfully. Now removing background.",
            disable_web_page_preview=True
        )
        new_document = removebg_video(file)
    else:
        await message.edit_text(text="Media not supported", disable_web_page_preview=True, reply_markup=ERROR_BUTTONS)
    if new_document.status_code == 200:
        with open(new_file_name, "wb") as file:
            file.write(new_document.content)
        await update.reply_chat_action("upload_document")
    else:
        await message.edit_text(text="API is error.", reply_markup=ERROR_BUTTONS)
        return
    try:
        await update.reply_document(document=new_file_name, quote=True)
        try:
            os.remove(file)
        except:
            pass
    except Exception as error:
        await message.edit_text(
            text=f"Error:- `{error}`",
            disable_web_page_preview=True,
            reply_markup=ERROR_BUTTONS
        )


def removebg_image(file):
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": open(file, "rb")},
        data={"size": "auto"},
        headers={"X-Api-Key": REMOVEBG_API}
    )


def removebg_video(file):
    return requests.post(
        "https://api.unscreen.com/v1.0/videos",
        files={"video_file": open(file, "rb")},
        headers={"X-Api-Key": UNSCREEN_API}
    )


Bot.run()
