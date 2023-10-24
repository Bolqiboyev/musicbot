import telebot
import os
import sqlite3
from mutagen.easyid3 import EasyID3
from telebot.types import *
from flask import *
from pydub import AudioSegment
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


#@BolqiboyevUz


MESSAGE_ID = []
CHATID = []
FILE_PATH = dict()
bot_user = "@mp3Tool_allbot"
ADMIN_ID = 5711448824

panel = InlineKeyboardMarkup(row_width=2)
panel.add(
InlineKeyboardButton('📥 Xabar yuborish', callback_data='reklama'),
    InlineKeyboardButton('📝 Forward Xabar', callback_data='forward')

    ).add(
    InlineKeyboardButton('📊 Statistika', callback_data='stat'))
key = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("🚫 Bekor qilish"))
back = InlineKeyboardMarkup(row_width=1)
back.add(
    InlineKeyboardButton('⬅️ Orqaga', callback_data='back1'),

    )
rek = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Music editor",url="https://t.me/mp3Tool_allbot"))
conn = sqlite3.connect('database.db',
                       check_same_thread=False,
                       isolation_level=None)
cursor = conn.cursor()

cursor.execute(
  "CREATE TABLE IF NOT EXISTS userdata(id INTEGER PRIMARY KEY,chat_id INTIGER UNIQUE)"
)
conn.commit()


app = Flask(__name__)

bot = telebot.TeleBot("6513925334:AAFLym7BbAizrNiG5CJYifS_WrxvB0M8t0Q",parse_mode='html')

def tool_menu(path):
  key = InlineKeyboardMarkup()
  key.add(
    InlineKeyboardButton(text="👤 Set name",callback_data=f'setname-{path}'),
    InlineKeyboardButton(text="🎸 Set artist",callback_data=f'setartist-{path}')
  )
  key.add(
    InlineKeyboardButton(text="🎧 Voice 10s",callback_data=f'format-{path}'),
    InlineKeyboardButton(text="🎧 Voice 15s",callback_data=f'format1-{path}')
    # InlineKeyboardButton(text="Set teg",callback_data=f'setteg-{path}'),
  ).add(
    InlineKeyboardButton(text="✉️ Feedback",callback_data=f'feedback'),
  )
  return key

@app.route('/', methods=['POST', 'GET'])
def webhook():
  if request.method == 'POST':
    data = request.get_json()
    bot.process_new_updates([telebot.types.Update.de_json(data)])
    return "OK"
  else:
    return "Hello, this is your Telegram bot's webhook!"


@bot.message_handler(commands=['start'])
def welcome(msg):
  try:
    cursor.execute(f"INSERT INTO userdata(chat_id) VALUES({msg.chat.id})")
    print(cursor.fetchall())
    conn.commit()
    bot.send_message(ADMIN_ID,f"<b>👤 Yangi <a href='tg://user?id={msg.chat.id}'>{msg.from_user.first_name}</a> qo'shildi!</b>")
  except Exception as e:
    print(e)
  dta = f"""
<b>👋 Assalomu alaykum hurmatli {msg.from_user.first_name}

🤖 Telegram bot orqali siz !

📝Musiqani Author o'zgartirishingiz!
📝Musiqani Nomi ni o'zgartirishingiz!

🎧 Musiqani 10s va 15s voice(galos) tayorlashingiz mumkun!

📥 Foydalanish uchun musiqani botga yuboring!</b>
  """
  bot.send_photo(chat_id=msg.chat.id,photo="https://img.freepik.com/premium-vector/mp3-file-download-icon-web-apps_116137-8843.jpg",reply_to_message_id=msg.id,caption=dta)

@bot.message_handler(content_types=['text'])
def custom(msg):
  if msg.text == '/panel' and msg.chat.id == ADMIN_ID:
    bot.send_message(msg.chat.id,"<b>🧑‍💻 Admin panelga Xush-kelibsiz!</b>",reply_markup=panel)

@bot.message_handler(content_types=['audio'])
def audio_handler(msg):
  tag = msg.audio
  txt = f"""<b>
#Tags<code>
Album Artist: {tag.performer}
Music title: {tag.title}
File name: {tag.file_name}
</code>

⏰ Time: {tag.duration / 60:.02f}
📄 File size: {tag.file_size/(1024*1024):.02f} mb
</b>
  """
  path = bot.get_file(tag.file_id).file_path+f"-{tag.file_name}"
  
  bot.send_photo(chat_id=msg.chat.id,photo="https://img.freepik.com/premium-vector/mp3-file-download-icon-web-apps_116137-8843.jpg",reply_to_message_id=msg.id,caption=txt,reply_markup=tool_menu(path))

def for_send(message):
    text = message.text
    if text == "🚫 Bekor qilish":
        bot.send_message(message.chat.id, "🚫 Xabar yuborish bekor qilindi!", reply_markup=back)
    else:
        cursor.execute("SELECT chat_id FROM userdata")
        rows = cursor.fetchall()
        for row in rows:
            try:
                chat_id = row[0]
                print(chat_id)
                bot.forward_message(chat_id, ADMIN_ID, message.message_id)
            except Exception as e:
                print(e)
        bot.send_message(ADMIN_ID, "<b>✅ Xabar hamma foydalanuvchiga yuborildi!</b>", reply_markup=back)
def ads_send(message):
    try:
        text = message.text
        if text=="🚫 Bekor qilish":
            bot.send_message(message.chat.id,"<b>🚫 Xabar yuborish bekor qilindi !</b>",reply_markup=back)
        else:
            cursor.execute("SELECT chat_id FROM userdata")
            rows = cursor.fetchall()
            for i in rows:
                chat_id = (i[0])
                try:
                  bot.send_message(chat_id,message.text)
                except:
                  pass
            bot.send_message(ADMIN_ID,"<b>✅ Xabar hamma foydalanuvchiga yuborildi!</b>",reply_markup=back)
    except Exception as e:
        print(e)

def contacts(message):
    text = message.text
    if text == "🚫 Bekor qilish":
        bot.send_message(message.chat.id, "<b>🚫 Xabar yuborish bekor qilindi!</b>")
    else:
        keymenu = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Javob berish",callback_data=f"javob-{message.chat.id}-{message.message_id}"))
        a = bot.forward_message(ADMIN_ID, message.chat.id, message.message_id).message_id
        bot.send_message(ADMIN_ID,reply_to_message_id=a,text="<b>Javob berish</b>", reply_markup=keymenu)
        bot.send_message(message.chat.id,reply_to_message_id=message.message_id,text="<b>✅ Xabaringiz adminga yetkazildi!</b>")


def javob_def(msg):
  try:
    bot.send_message(CHATID[-1],msg.text,reply_to_message_id=MESSAGE_ID[-1])
    # bot.send_message(ADMIN_ID,"Yuborildi",reply_to_message_id=msg.message_id)
  except:
    pass

def set_name(msg):
  try:
    audio = EasyID3(f"music/{msg.chat.id}.mp3")
    audio["title"] = f"{msg.text}"
    audio.save()
  except Exception as e:
    print(e)
  bot.send_audio(chat_id=msg.chat.id,audio=open(f"music/{msg.chat.id}.mp3",'rb'),caption=f"<b>\n👉 Tools: {bot_user}</b>",reply_markup=rek)
  os.remove(f"music/{msg.chat.id}.mp3")
def set_artist(msg):
  try:
    audio = EasyID3(f"music/{msg.chat.id}.mp3")
    audio["artist"] = f"{msg.text}"
    audio.save()
  except Exception as e:
    print(e)
  bot.send_audio(chat_id=msg.chat.id,audio=open(f"music/{msg.chat.id}.mp3",'rb'),caption=f"\n<b>👉 Tools: {bot_user}</b>",reply_markup=rek)
  os.remove(f"music/{msg.chat.id}.mp3")

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
  text = call.data
  cid = call.message.chat.id
  if 'format-' in text:
    bot.answer_callback_query(call.id,"Iltimos biroz kuting!",show_alert=True)
    path = text.split("-")[1]
    caption = "<b>"+text.split("-")[2]+"</b>"
    b = bot.download_file(path)
    with open(f"music/{cid}.mp3",'wb') as f:
      f.write(b)
    org = AudioSegment.from_file(f"music/{cid}.mp3", format="mp3")
    cute = org[:10000] 
    cute.export(f"music/{cid}.ogg", format="ogg")
    bot.send_voice(cid,voice=open(f"music/{cid}.ogg",'rb'),caption=caption,reply_markup=rek)
    os.remove(f"music/{cid}.ogg")
  if 'format1-' in text:
    bot.answer_callback_query(call.id,"Iltimos biroz kuting!",show_alert=True)
    path = text.split("-")[1]
    caption = "<b>"+text.split("-")[2]+"</b>"
    b = bot.download_file(path)
    with open(f"music/{cid}.mp3",'wb') as f:
      f.write(b)
    org = AudioSegment.from_file(f"music/{cid}.mp3", format="mp3")
    cute = org[:15000] 
    cute.export(f"music/{cid}.ogg", format="ogg")
    bot.send_voice(cid,voice=open(f"music/{cid}.ogg",'rb'),caption=caption,reply_markup=rek)
    os.remove(f"music/{cid}.ogg")
  elif 'setname-' in text:
    a = bot.send_message(cid,'<b>📄 File nomini yuboring!\n\nℹ️Namuna: <code>music</code> </b>')
    bot.register_next_step_handler(a,set_name)
    path = text.split("-")[1]
    FILE_PATH[str(cid)]=path
    b = bot.download_file(path)
    with open(f"music/{cid}.mp3",'wb') as f:
      f.write(b)
  elif 'setartist-' in text:
    a = bot.send_message(cid,'<b>🎸 Artist nomini yuboring!\n\nℹ️ Namuna: <code>Eminem</code> </b>')
    bot.register_next_step_handler(a,set_artist)
    path = text.split("-")[1]
    FILE_PATH[str(cid)]=path
    b = bot.download_file(path)
    with open(f"music/{cid}.mp3",'wb') as f:
      f.write(b)
  try:
    callback_data = text
    user_id = cid
    if callback_data == 'stat' and user_id == ADMIN_ID:
      cursor.execute("SELECT COUNT(chat_id) FROM userdata")
      rows = cursor.fetchall()
      bot.edit_message_text(f"<b>📊 Bot obunachilari soni: {rows[0][0]}</b>",
                            user_id,
                            call.message.id,
                            reply_markup=back)
    if callback_data == 'back1' and user_id == ADMIN_ID:
      bot.edit_message_text(f"<b>Admin panelga xush kelibsiz! </b>",
                            user_id,
                            call.message.id,
                            reply_markup=panel)
    if callback_data == 'reklama' and user_id == ADMIN_ID:
      bot.delete_message(user_id, call.message.id)
      adver = bot.send_message(user_id,
                               "<b>✍️ Xabar matnini kiritng !</b>",
                               reply_markup=key)
      bot.register_next_step_handler(adver, ads_send)
    if callback_data == 'forward' and user_id == ADMIN_ID:
      bot.delete_message(user_id, call.message.id)
      adver = bot.send_message(user_id,
                               "<b>✍️ Xabar matnini kiritng !</b>",
                               reply_markup=key)
      bot.register_next_step_handler(adver, for_send)
    if callback_data=='feedback':
      bot.delete_message(chat_id=user_id, message_id=call.message.id)
      a = bot.send_message(chat_id=user_id,
                           text=f"<b>❓ Savolingizni yozing!</b>",
                           parse_mode='html',
                           reply_markup=key)
      bot.register_next_step_handler(a, contacts)
    print(text)
    if "javob" in text:
      a = data.split("-")
      print(a)
      chatid = a[1]
      mid = a[2]
      CHATID.append(chatid)
      MESSAGE_ID.append(mid)
      b  = bot.send_message(chat_id=user_id,
                   text=f"<b>❓ Javobingiz ni  yozing!</b>",
                   reply_markup=key)
      bot.register_next_step_handler(b, javob_def)
  except:
    pass
app.run(host='0.0.0.0')
