from App import config
from App.Controller.user_controller import User
from App.Controller import get_request
from App.Controller import send_request
from App.Controller import process
from App.Controller import db_postgres_controller as db
from datetime import datetime
from jdatetime import datetime as jdatetime
import json
import threading
import uuid
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, MessageHandler,  filters, ContextTypes
from re import match
import web_server



TOKEN = config.configs['BOT_TOKEN']
BASE_URL = config.configs['BASE_URL']
BASE_FILE_URL = config.configs['BASE_FILE_URL']
     

def get_datetime():
    jdate = jdatetime.fromgregorian(datetime=datetime.now())
    time = f'{jdate.hour+3}:{jdate.minute+30}:{jdate.second}'
    date = f'{jdate.year}-{jdate.month}-{jdate.day}'
    now_datetime = json.dumps({'date':date , 'time':time})
    return now_datetime

keyboard_start = [
    [
        InlineKeyboardButton("پنهان کردن در تصویر", callback_data="/hide-text-in-image"),
        InlineKeyboardButton("استخراج از تصویر", callback_data="/get-hidden-text-from-image"),
    ],
    [
        InlineKeyboardButton("پنهان کردن در صوت", callback_data="/hide-text-in-sound"),
        InlineKeyboardButton("استخراج از صوت", callback_data="/get-hidden-text-from-sound"),
    ],
    [
        InlineKeyboardButton("ارسال موقعیت مکانی", callback_data="/send-location"),
        InlineKeyboardButton("جمع دو عدد", callback_data="/add-two-numbers"),
    ],
    [InlineKeyboardButton("نتیجه درخواست ها", callback_data="/get-result")],
    [InlineKeyboardButton("راهنما", callback_data="/help")],
]
reply_markup_start = InlineKeyboardMarkup(keyboard_start)

keyboard_cancel = [[
            InlineKeyboardButton("بازگشت به صفحه اصلی", callback_data="/cancel")
        ]]
reply_markup_cancel = InlineKeyboardMarkup(keyboard_cancel)

keyboard_cancel_help = [[
            InlineKeyboardButton("بازگشت به صفحه اصلی", callback_data="/cancel"),
            InlineKeyboardButton("راهنمای ارسال فایل", callback_data="/help")
        ]]
reply_markup_cancel_help = InlineKeyboardMarkup(keyboard_cancel_help)

keyboard_cancel_getResult = [[
            InlineKeyboardButton("بازگشت به صفحه اصلی", callback_data="/cancel"),
            InlineKeyboardButton("نتیجه درخواست", callback_data="/get-result")
        ]]
reply_markup_cancel_getResult = InlineKeyboardMarkup(keyboard_cancel_getResult)


async def start(update, context, _text, _STEP, chat_id):
    try:
        username = update.callback_query.from_user.username
        first_name = update.callback_query.from_user.first_name
    except:
        username = update.message.from_user.username
        first_name = update.message.from_user.first_name
    user = User(username=username, id=chat_id)
    user.signup()    
    await context.bot.send_message(chat_id=chat_id, text='سلام {}\nبه ربات {} خوش آمدید\nبرای استفاده از ربات یکی از گزینه های زیر را انتخاب کنید : '.format(first_name, config.configs['SYSTEM_NAME']), reply_markup=reply_markup_start)
    db.db.changeUserSTEP('home', chat_id)
    
async def help(_update, context, _text, _STEP, chat_id):
    await context.bot.send_message(chat_id, text=' برای ارسال تصویر و صدا به صورت فایل ابتدا از سمت چپ و پایین بر روی آیکون + ضربه بزنید سپس بر روی ارسال به صورت فایل ضربه بزنید')

async def cancel(_update, context, _text, _STEP, chat_id):
    await context.bot.send_message(chat_id, text='صفحه اصلی \nبرای شروع یکی از گزینه های زیر را انتخاب کنید', reply_markup=reply_markup_start)
    db.db.changeUserSTEP('home', chat_id)
   

async def handle_get_result(_update, context, _text, _STEP, chat_id):
    db.db.changeUserSTEP('handle-get-result', chat_id)
    await context.bot.send_message(chat_id=chat_id, text='شناسه درخواست خود را ارسال کنید', reply_markup=reply_markup_cancel)
    
async def get_result(req_uuid, chat_id, update, context):
    res = process.result(req_uuid, chat_id)
    if res['status-code'] == 400:
        await context.bot.send_message(chat_id=chat_id, text='شناسه درخواست معتبر نمی باشد.', reply_markup=reply_markup_cancel)
        return
    elif res['status-code']  == 202:
        await context.bot.send_message(chat_id=chat_id, text=f' شناسه درخواست : { res["request_id"] } \n نتیجه درخواست: درخواست منتظر پردازش می باشد \n برای بررسی نتیجه بر روی نتیجه درخواست ها ضربه بزنید', reply_markup=reply_markup_cancel_getResult)
        
    # Done  
    
    elif res['type'] == '/add-two-numbers':  # add two numbers 
        
        await context.bot.send_message(chat_id=chat_id, text=f'شناسه درخواست : { res["request_id"] } \nنتیجه درخواست : \n حاصل جمع برابر { res["result"] } می باشد', reply_markup=reply_markup_cancel)
        
    elif res['type'] == '/hide-text-in-image': # hide text in image 
        img_path = res['result']['url']
        await context.bot.send_message(chat_id=chat_id, text=f' شناسه درخواست : { res["request_id"] } \n نتیجه درخواست: درخواست با موفقیت تکمیل شد. تصویر خروجی در حال ارسال می باشد')
        try:
            await context.bot.send_document(chat_id=chat_id, document=img_path, reply_markup=reply_markup_cancel)
        except:
            await context.bot.send_message(chat_id=chat_id, text=f'ارسال فایل با مشکل مواجه شده است. لطفا بر روی نتیجه درخواست ضربه بزنید', reply_markup=reply_markup_cancel_getResult)
        
    elif res['type'] == '/get-hidden-text-from-image': # get hidden text from image
        if res["result"] == "this images doesn't have any hidden text":
            await context.bot.send_message(chat_id=chat_id, text=f'شناسه درخواست : { res["request_id"] } \n نتیجه درخواست: این تصویر هیچ متن پنهان شده ای ندارد', reply_markup=reply_markup_cancel)
        else:
            await update.message.reply_text(f'شناسه درخواست : { res["request_id"] } \n نتیجه درخواست : \n متن خروجی : \n {res["result"]["extracted text"]}', reply_markup=reply_markup_cancel)
            
    elif res['type'] == '/hide-text-in-sound': # hidde text in sound
        sound_path = res['result']['url']
        await context.bot.send_message(chat_id=chat_id, text=f' شناسه درخواست : { res["request_id"] } \n نتیجه درخواست: درخواست با موفقیت تکمیل شد. فایل صوتی خروجی در حال ارسال می باشد')
        try:
            await context.bot.send_document(chat_id=chat_id, document=sound_path, reply_markup=reply_markup_cancel)
        except:
            await context.bot.send_message(chat_id=chat_id, text=f'ارسال فایل با مشکل مواجه شده است. لطفا بر روی نتیجه درخواست ضربه بزنید', reply_markup=reply_markup_cancel_getResult)
            
    
    elif res['type'] == '/get-hidden-text-from-sound': # get hidden text from image
        if res["result"] == "this sound doesn't have any hidden text":
            await context.bot.send_message(chat_id=chat_id, text=f'شناسه درخواست : { res["request_id"] } \n نتیجه درخواست: این فایل صوتی هیچ متن پنهان شده ای ندارد', reply_markup=reply_markup_cancel)
        else:
            await context.bot.send_message(chat_id=chat_id, text=f'شناسه درخواست : { res["request_id"] } \n نتیجه درخواست : \n متن خروجی : \n {res["result"]["secret text"]}', reply_markup=reply_markup_cancel)
        
    else:
        await context.bot.send_message(chat_id=chat_id, text='نامعتبر', reply_markup=reply_markup_cancel)
        return
    db.db.changeUserSTEP('home', chat_id)


async def get_first_number(_update, context, _text, _STEP, chat_id):
    db.db.changeUserSTEP('enter-num1', chat_id)
    await context.bot.send_message(chat_id=chat_id, text='عدد اول را وارد کنید', reply_markup=reply_markup_cancel)
    
async def get_second_number(_update, context, text, _STEP, chat_id):
    try:
        db.db.changeUserSecretMsg(int(text),chat_id)
        db.db.changeUserSTEP('enter-num2', chat_id)
        await context.bot.send_message(chat_id=chat_id, text='عدد دوم را وارد کنید', reply_markup=reply_markup_cancel)
    except:
        await context.bot.send_message(chat_id=chat_id, text='لطفا فقط عدد وارد کنید', reply_markup=reply_markup_cancel)
        
async def handle_numbers(update, context, text, _STEP, chat_id):
    try:
        num1 = int(db.db.getUserSecretMsg(chat_id))
        num2 = int(text)
        await add_two_numbers(num1, num2, update, context, chat_id)
    except:
        await context.bot.send_message(chat_id=chat_id, text='لطفا فقط عدد وارد کنید', reply_markup=reply_markup_cancel)
        db.db.changeUserSTEP('enter-num2', chat_id)
        
async def add_two_numbers(num1, num2, update, context, chat_id):
    j_date_time = get_datetime()
    params = json.dumps({"num1": num1,
                        "num2": num2
                        })
    # Add request to database
    req_uuid = db.db.addReqToDb(chat_id, '/add-two-numbers', params, j_date_time, uuid.uuid4().hex)
    
    
    send_request.send(req_uuid)  # Send request to queue
    await context.bot.send_message(chat_id=chat_id, text='درخواست در صف انجام قرار دارد. \nلطفا چند لحظه صبر کنید')
    time.sleep(5)
    db.db.changeUserSTEP('home', chat_id)
    await get_result(req_uuid, chat_id, update, context)


async def send_location(_update, context, _text, _STEP, chat_id):
    db.db.changeUserSTEP('handle-send-location', chat_id)
    await context.bot.send_message(chat_id=chat_id, text='لطفا موقعیت مکانی خودتان را ارسال کنید', reply_markup=reply_markup_cancel)
    
async def handle_send_location(update, context, _text, _STEP, chat_id):
    try :
        latitude = update.message.location.latitude
        longitude = update.message.location.longitude
    except:
        await context.bot.send_message(chat_id=chat_id, text='لطفا موقعیت مکانی خودتان را ارسال کنید', reply_markup=reply_markup_cancel)
        return
    
    db.db.changeUserSTEP('home', chat_id)
    params = json.dumps({
                        "latitude": latitude ,
                        "longitude": longitude
                        })
    db.db.addUserLocation(chat_id, params)
    await context.bot.send_message(chat_id=chat_id, text='موقعیت مکانی شما با موفقیت ارسال شد', reply_markup=reply_markup_cancel)


async def handle_hide_text_in_image(_update, context, _text, _STEP, chat_id):
    db.db.changeUserSTEP('msg-hide-text-in-image', chat_id)
    await context.bot.send_message(chat_id=chat_id, text='متن مورد نظر را به انگلیسی وارد کنید', reply_markup=reply_markup_cancel)
    
async def msg_hide_text_in_image(_update, context, text, _STEP, chat_id):
    pattern = r'^[a-zA-Z0-9\s\W]+$'
    if text == '/none' or not match(pattern,text) :
        await context.bot.send_message(chat_id=chat_id, text='لطفا فقط یک متن انگلیسی وارد کنید',reply_markup=reply_markup_cancel)
        return
    
    db.db.changeUserSecretMsg(text,chat_id)
    db.db.changeUserSTEP('handle-hide-text-in-image', chat_id)
    await context.bot.send_message(chat_id=chat_id, text='تصویر مورد نظر را به صورت فایل ارسال کنید.\nاگر نمی دانید چگونه باید به صورت فایل ارسال کنید بر روی دکمه راهنمای ارسال فایل بزنید',reply_markup=reply_markup_cancel_help)

async def hide_text_in_image(update, context, text, _STEP, chat_id):
    message = db.db.getUserSecretMsg(chat_id)

    # Check the user sent image or not
    if text != '/none' or update.message.document.mime_type.split('/')[0] != 'image':
        await context.bot.send_message(chat_id=chat_id, text='لطفا فقط تصویر ارسال کنید',reply_markup=reply_markup_cancel)
        return
    
    # Check the image sent as file or sent as image. must send as file
    if update.message.photo != ():
        await context.bot.send_message(chat_id=chat_id, text='لطفا تصویر را به صورت فایل ارسال کنید.\nاگر نمی دانید چگونه باید به صورت فایل ارسال کنید بر روی دکمه راهنمای ارسال فایل بزنید',reply_markup=reply_markup_cancel_help)
        return
        
    file = await context.bot.get_file(update.message.document)
    
    j_date_time = get_datetime()
    params = json.dumps({"url" : file.file_path , 
                        "text" : message})
    
    # Add request to database
    req_uuid = db.db.addReqToDb(chat_id, '/hide-text-in-image', params, j_date_time, uuid.uuid4().hex)
    send_request.send(req_uuid)  # Send request to queue
    await context.bot.send_message(chat_id=chat_id, text='درخواست در صف انجام قرار دارد. \nلطفا چند لحظه صبر کنید')
    time.sleep(5)
    await get_result(req_uuid, chat_id, update, context)
    db.db.changeUserSTEP('home', chat_id)


async def handle_get_hidden_text_from_image(_update, context, _text, _STEP, chat_id):
    db.db.changeUserSTEP('handle-get-hidden-text-from-image', chat_id)
    await context.bot.send_message(chat_id=chat_id, text='تصویر مورد نظر را به صورت فایل ارسال کنید.\nاگر نمی دانید چگونه باید به صورت فایل ارسال کنید بر روی دکمه راهنمای ارسال فایل بزنید',reply_markup=reply_markup_cancel_help)

async def get_hidden_text_from_image(update, context, text, _STEP, chat_id):
    # Check the user sent image or not
    if text != '/none' or update.message.document.mime_type.split('/')[0] != 'image':
        await context.bot.send_message(chat_id=chat_id, text='لطفا فقط تصویر ارسال کنید',reply_markup=reply_markup_cancel)
        return
    
    # Check the image sent as file or sent as image. must send as file
    if update.message.photo != ():
        await context.bot.send_message(chat_id=chat_id, text='تصویر مورد نظر را به صورت فایل ارسال کنید.\nاگر نمی دانید چگونه باید به صورت فایل ارسال کنید بر روی دکمه راهنمای ارسال فایل بزنید',reply_markup=reply_markup_cancel_help)
        return        
        
    file = await context.bot.get_file(update.message.document)
    j_date_time = get_datetime()
    params = json.dumps({"url" : file.file_path })
    
    req_uuid = db.db.addReqToDb(chat_id, '/get-hidden-text-from-image', params, j_date_time, uuid.uuid4().hex)
    send_request.send(req_uuid)  # Send request to queue
    await context.bot.send_message(chat_id=chat_id, text='درخواست در صف انجام قرار دارد. \nلطفا چند لحظه صبر کنید')
    time.sleep(5)
    await get_result(req_uuid, chat_id, update, context)
    db.db.changeUserSTEP('home', chat_id)


async def handle_hide_text_in_sound(_update, context, _text, _STEP, chat_id):
    db.db.changeUserSTEP('msg-hide-text-in-sound', chat_id)
    await context.bot.send_message(chat_id=chat_id, text='متن مورد نظر را به انگلیسی وارد کنید',reply_markup=reply_markup_cancel)

async def msg_hide_text_in_sound(_update, context, text, _STEP, chat_id):
    pattern = r'^[a-zA-Z0-9\s\W]+$'
    if text == '/none' or not match(pattern,text):
        await context.bot.send_message(chat_id=chat_id, text='لطفا فقط یک متن انگلیسی وارد کنید',reply_markup=reply_markup_cancel)
        return

    db.db.changeUserSecretMsg(text,chat_id)
    db.db.changeUserSTEP('handle-hide-text-in-sound', chat_id)
    await context.bot.send_message(chat_id=chat_id, text='صوت مورد نظر را به صورت فایل ارسال کنید.\nاگر نمی دانید چگونه باید به صورت فایل ارسال کنید بر روی دکمه راهنمای ارسال فایل بزنید',reply_markup=reply_markup_cancel_help)

async def hide_text_in_sound(update, context, text, _STEP, chat_id):
    message = db.db.getUserSecretMsg(chat_id)
    
    # Check the user sent audio or not
    if text != '/none' or update.message.document.mime_type.split('/')[0] != 'audio':
        await context.bot.send_message(chat_id=chat_id, text='لطفا فقط فایل صوتی ارسال کنید',reply_markup=reply_markup_cancel)
        return
    
    # Check the audio sent as file or sent as audio. must send as file
    if update.message.voice is not None:
        await context.bot.send_message(chat_id=chat_id, text='صوت مورد نظر را به صورت فایل ارسال کنید.\nاگر نمی دانید چگونه باید به صورت فایل ارسال کنید بر روی دکمه راهنمای ارسال فایل بزنید',reply_markup=reply_markup_cancel_help)
        return
    
    file = await context.bot.get_file(update.message.document)
    j_date_time = get_datetime()
    params = json.dumps({"url" : file.file_path , 
                        "text" : message})
    
    # Add request to database
    req_uuid = db.db.addReqToDb(chat_id, '/hide-text-in-sound', params, j_date_time, uuid.uuid4().hex)
    send_request.send(req_uuid)  # Send request to queue
    await context.bot.send_message(chat_id=chat_id, text='درخواست در صف انجام قرار دارد. \nلطفا چند لحظه صبر کنید')
    time.sleep(5)
    await get_result(req_uuid, chat_id, update, context) 
    db.db.changeUserSTEP('home', chat_id)


async def handle_get_hidden_text_from_sound(_update, context, _text, _STEP, chat_id):
    db.db.changeUserSTEP('handle-get-hidden-text-from-sound', chat_id)
    await context.bot.send_message(chat_id=chat_id, text='صوت مورد نظر را به صورت فایل ارسال کنید.\nاگر نمی دانید چگونه باید به صورت فایل ارسال کنید بر روی دکمه راهنمای ارسال فایل بزنید',reply_markup=reply_markup_cancel_help)

async def get_hidden_text_from_sound(update, context, text, _STEP, chat_id):
    # Check the user sent audio or not
    if text != '/none' or update.message.document.mime_type.split('/')[0] != 'audio':
        await context.bot.send_message(chat_id=chat_id, text='لطفا فقط فایل صوتی ارسال کنید',reply_markup=reply_markup_cancel)
        return
    
    # Check the audio sent as file or sent as audio. must send as file
    if update.message.voice is not None:
        await context.bot.send_message(chat_id=chat_id, text='صوت مورد نظر را به صورت فایل ارسال کنید.\nاگر نمی دانید چگونه باید به صورت فایل ارسال کنید بر روی دکمه راهنمای ارسال فایل بزنید',reply_markup=reply_markup_cancel_help)
        return

    file = await context.bot.get_file(update.message.document)
    j_date_time = get_datetime()
    params = json.dumps({"url" : file.file_path })
    
    req_uuid = db.db.addReqToDb(chat_id, '/get-hidden-text-from-sound', params, j_date_time, uuid.uuid4().hex)
    send_request.send(req_uuid)  # Send request to queue
    await context.bot.send_message(chat_id=chat_id, text='درخواست در صف انجام قرار دارد. \nلطفا چند لحظه صبر کنید')
    time.sleep(5)
    await get_result(req_uuid, chat_id, update, context)
    db.db.changeUserSTEP('home', chat_id)


# text - step - callback
commands = [
    [r"/start", r".+", start], # text - step - callback
    [r"/help", r".+", help],
    [r"/cancel", r".+", cancel],
    
    [r"/get-result", r".+", handle_get_result],
    [r"/add-two-numbers", r".+", get_first_number],
    [r"/send-location", r".+", send_location],
    [r"/hide-text-in-image", r".+", handle_hide_text_in_image],
    [r"/get-hidden-text-from-image", r".+", handle_get_hidden_text_from_image],
    [r"/hide-text-in-sound", r".+", handle_hide_text_in_sound],
    [r"/get-hidden-text-from-sound", r".+", handle_get_hidden_text_from_sound],
    
    [r".+", r"enter-num1", get_second_number],
    [r".+", r"enter-num2", handle_numbers],
    
    [r".+", r"handle-send-location", handle_send_location],
    
    [r".+", r"msg-hide-text-in-image", msg_hide_text_in_image],
    [r".+", r"handle-hide-text-in-image", hide_text_in_image],
    
    [r".+", r"handle-get-hidden-text-from-image", get_hidden_text_from_image],
    
    [r".+", r"msg-hide-text-in-sound", msg_hide_text_in_sound],
    [r".+", r"handle-hide-text-in-sound", hide_text_in_sound],
    
    [r".+", r"handle-get-hidden-text-from-sound", get_hidden_text_from_sound],        
]


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.callback_query.data
        chat_id = update.effective_chat.id
    except:
        text = update.message.text
        chat_id = update.message.chat_id
        
    try:
        text,STEP = db.db.changeUserTextMessage(text, chat_id)    
    except: # Save user info in the database
        await start(update, context, None, None, chat_id)
        return
        
    if text is None:
        text = '/none' # It means sent media or location, not a text
        
    if STEP == 'handle-get-result' and not text.startswith('/'):
        await get_result(text, update.message.chat_id, update, context)
        return

    for command in commands:
        valid_command = False
        pattern, step, callback = command 
        if match(pattern, text) and match(step, STEP):
            valid_command = True
            await callback(update,context,text,STEP,chat_id)
            break
        
    if not valid_command:
        await context.bot.send_message(chat_id=chat_id, text='لطفا یک دستور معتبر وارد کنید!')
                

def main():
    # time.sleep(20)
    
    # Run web server
    t = threading.Thread(None, web_server.main, None, ())
    t.start()    
    
    # Get requests from queue
    t = threading.Thread(None, get_request.get_requests_from_queue, None, ())
    t.start()

    app = Application.builder().token(TOKEN).base_url(BASE_URL).base_file_url(BASE_FILE_URL).read_timeout(10).build()
    
    # Messages
    app.add_handler(MessageHandler(filters=filters.ALL, callback=message))
    # Inline Keyboard
    app.add_handler(CallbackQueryHandler(message))

    # Polls the bot
    print('Polling...')
    app.run_polling(allowed_updates=Update.ALL_TYPES)

main()