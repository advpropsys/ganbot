from get import get_image
from utils.hubstyle import style
import subprocess
import telebot
import os
import secrets
from telebot import types # для указание типов
from config import TOKEN
from telebot import apihelper

apihelper.API_URL = "http://api.telegram.org/bot{0}/{1}"

bot = telebot.TeleBot(str(TOKEN))


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🐹 Style (vgg19)")
    btn2 = types.KeyboardButton("🥵 Chainsawman art (Custom AnimeGAN2)")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Hi, {0.first_name}! Lets design something cool?".format(message.from_user), reply_markup=markup)
    

def loadphoto(message,nn:int=-1):
            raw = message.photo[nn].file_id
            name = secrets.token_urlsafe(16)+".jpg"
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(name,'wb') as new_file:
                new_file.write(downloaded_file)
            return name
back = types.KeyboardButton("Return")
state = None
@bot.message_handler(content_types=['text'])
def func(message):
    global state
    
    if(message.text == "🐹 Style (vgg19)"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(back)
        bot.send_message(message.chat.id, text="Send pic you want to style first! \nIn SAME message send style)",reply_markup=markup)
        
        state = 0
        
    elif(message.text == "🥵 Chainsawman art (Custom AnimeGAN2)"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, text="Send pic you want to CSM! ",reply_markup=markup)
        state = 1
        
        markup.add(back)
        
    elif (message.text == "Return"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("🐹 Style (vgg19)")
        button2 = types.KeyboardButton("🥵 Chainsawman art (Custom AnimeGAN2)")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="You have just returned, happy?", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text=f"Um idk, call Obama")
        
def send_image(botToken, imageFile, chat_id):
        command = 'curl -s -X POST https://api.telegram.org/bot' + botToken + '/sendPhoto -F chat_id=' + chat_id + " -F photo=@" + imageFile
        subprocess.call(command.split(' '))
        return
    
img=[]

@bot.message_handler(content_types=['photo'])
def csm(message):
    global state
    global img
    if state == 1:
        img2 = loadphoto(message)
        print('loaded')
        CSMstat=get_image(img2)
        print(CSMstat)
        if CSMstat:
            os.rename(f'{img2}_anime.jpg','send.jpg')
            # phot = open('send.jpg','rb')
            send_image(str(TOKEN),'send.jpg',f'{message.chat.id}')
            # os.remove('send.jpg')
            # os.remove(f'{img2}')
            # bot.send_photo(message.chat.id,phot)
        if CSMstat==0:
            bot.send_message(message.chat.id, text="Crashede💀, restart me")
            # os.remove(f'./{img2}')
        # if os.path.exists(f'./{img2}_anime.png'):
            # os.remove(f'./{img2}_anime.png')
    elif state == 0:
        img.append(loadphoto(message))
        if len(img)==2:
            transtate = style(img[0],img[1])
            if transtate:
                    # os.remove(f'{img[0]}')
                    # os.remove(f'{img[1]}')
                    send_image(str(TOKEN),f'{img[0]}_style.png',str(message.chat.id))
            if transtate==0:
                    bot.send_message(message.chat.id, text="Crashede💀, restart me")
                    # os.remove(f'{img[0]}')
                    # os.remove(f'{img[1]}')
            
            # if os.path.exists(f'{img[0]}_style.png'):
            #         os.remove(f'{img[0]}_style.png')
            img=[]
    else:
        bot.send_message(message.chat.id, text="Crashede💀, Select your styling first!")
        start(message)

bot.polling(none_stop=True)


# CSMstat=get_image('MG_1_1_New_York_City-1.jpg')
# #Transfer = style('YellowLabradorLooking_new.jpg','Vassily_Kandinsky,_1913_-_Composition_7.jpg')