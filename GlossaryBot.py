# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 15:06:58 2020

@author: rivanov
"""
import telebot;
from telebot import apihelper
from telebot import types
import json 
import pandas as pd

bot = telebot.TeleBot('1236642776:AAGoFWsiXX5qrLQOTyYlzklWIeAFR-0J16A');
#apihelper.proxy = {'https':'https:#159.203.44.177:3128'}


#class File:
#    def __init__(self, Name):
#        self.file = None
#        self.id = None
#        self.name = Name
#        self.path = None

knownUsers = []  
try:
    with open('users.json', 'r', encoding="utf-8") as f:
        knownUsers = json.load(f)
except Exception as e:
    
    pass

print(knownUsers)    
    
#userStep = {}  
#try:
#    with open('userSteps.json', 'r', encoding="utf-8") as f:
#        userStep = json.load(f)
#except Exception as e:
    #print(e)
#    pass

#print(userStep) 
rus_words = []
eng_words = []
rus2eng = {}
eng2rus = {} 

try:
#    with open('glossary.json', 'r', encoding="utf-8") as f:
        #glossary = json.load(f)
        #words = glossary.keys()
    glossary = pd.read_csv('glossary.csv', sep=';', encoding='utf-8')
    rus_words = glossary['rus']
    eng_words = glossary['eng']
    
    for i in range(glossary.shape[0]):
        eng2rus[glossary.iloc[i].eng] = glossary.iloc[i].rus
        rus2eng[glossary.iloc[i].rus] = glossary.iloc[i].eng
        
except Exception as e:
    print(e)
    pass


hideBoard = types.ReplyKeyboardRemove()


def save_users(uid):
    if uid not in knownUsers:
        knownUsers.append(uid)
#        save_steps(uid, 0)
        bot.send_message(492524329, u'Добавлен новый пользователь '+str(uid))
    
    #print(u'сохранение пользователя', userStep) 
    
    try:
        with open('users.json', 'w', encoding="utf-8") as uf:
            json.dump(knownUsers, uf)
    except Exception as e:
        #print(e)
        pass


def cut_slash(text):
    if '/' in text:
        text = text[1:]
    return text.lower()        
#def save_steps(uid, step):
#    userStep[str(uid)] = step
#    print('сохранение шага', userStep)
#    try:
#        with open('userSteps.json', 'w', encoding="utf-8") as usf:
#            json.dump(userStep, usf)
#    except Exception as e:
#        #print(e)
#        pass    

#def get_user_step(uid):
#    if uid in knownUsers:
#        return userStep[str(uid)]
#    else:
        #print("New user "+ str(uid) + " detected, who hasn't used \/start\ yet")
        #print(knownUsers)
#        save_users(uid)
        #save_steps(uid, 0)        
#    return 0

def message4all(text):
    for user in knownUsers: bot.send_message(user, text)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    word = cut_slash(message.text)
    if word in eng_words:
        bot.reply_to(message, eng2rus[word])
 #       bot.send_message(message.chat.id,glossary[word])

#        if get_user_step(message.from_user.id) == 1:
#            try:
#                save_steps(message.from_user.id, 0)
#                with open('hometask.jpg', 'wb') as htf:
#                    htf.write(file.file)
#                bot.reply_to(message, "Сохранил")
#                htf.close()
#                message4all(u'Поступило домашнее задание')
#            except Exception as e:
#                bot.reply_to(message, e) 
#        else:
#            try:
        #uis_pdf = open('files/' + uis_login + '.pdf', 'rb')
#                htf = open('hometask.jpg', 'rb')
#                bot.send_photo(message.chat.id, htf)
#                htf.close()
#            except Exception as e:
#                bot.reply_to(message, u'Домашнее задание не найдено')
#                bot.send_message(492524329, u'Домашнее задание не найдено')
                

            
     
    elif message.text == "/start":
        save_users(message.from_user.id)
 #       save_steps(message.from_user.id, 0)
#        markup = types.ReplyKeyboardMarkup( one_time_keyboard=True, selective=True, row_width=3 )
#        markup.add(u'Домашнее задание', u'Задание по английскому Михалюк', u'Задание по английскому Трубецкая', u'Обьявление', u'Расписание')
        bot.send_message(message.chat.id, 'С Вами авиационный глоссарий! Введите термин для перевода.')#, reply_markup=markup)
    elif message.text == "/help":
        bot.send_message(message.chat.id, str(message.from_user.first_name)+', введи авиационный термин на английском или русских языках.')
    elif message.text == "/users":
        if message.from_user.id == 492524329:
            try:
                uf = open('users.json', 'rb')
                bot.send_document(message.from_user.id, uf)
                uf.close()
            except Exception as e:
                bot.send_message(message.from_user.id, u'База пользователей не найдена')
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю, "+str(message.from_user.first_name)+". Напиши /help.")
    

#@bot.message_handler(content_types=['photo'])
#def handle_file(message):
#    try:
#        chat_id = message.chat.id
#        global file
#        file = File(bot.get_file(message.photo[0].file_id))
#        file.file = bot.download_file(file.name.file_path)
#        if chat_id not in knownUsers: save_users(chat_id)
#        save_steps(chat_id, 1)
#        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
#        markup.add(u'Домашнее задание', u'Задание по английскому Михалюк', u'Задание по английскому Трубецкая', u'Обьявление', u'Расписание')
#        bot.reply_to(message, u'Что это?', reply_markup=markup)
        
 #   except Exception as e:
 #       bot.reply_to(message, e)       

#try: bot.polling(none_stop=True, interval=10)
#except Exception as e: print(e)

if __name__ == '__main__':
   bot.polling(none_stop=True)

