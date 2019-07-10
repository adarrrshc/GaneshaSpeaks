import requests
from telegram.ext import Updater,CommandHandler
from lxml import html

import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup 



bot_token=''

updater=Updater(token='')
dispatcher = updater.dispatcher
jq = updater.job_queue

admin_id=00000000
users=['','']
user_data=[]

jq = updater.job_queue


def init_bknd():
    global users
    global user_data
    for t in users:
        user_data.append([int(t),"daily",0,0])




def start(bot, update):
    global user_data
    flag=0
    for ud in user_data:
        if(int(ud[0])==update.message.chat_id):
            flag=1
            break

    if(flag==0):
        user_data.append([update.message.chat_id,"daily",0,0])
                                                        #clicked,no of clicks 
    try:
        print("inside start\n")
        bot.send_message(chat_id=update.message.chat_id, text="Welcome To GaneshaSpeaks")
        
        bot.send_message(chat_id=update.message.chat_id, text="Choose Your Zodiac Sign", reply_markup=ReplyKeyboardMarkup(keyboard=[  ["/start"],["/timeframe"],
                                                                                                            ["/Aquarius (January 20 to February 18)"],
                                                                                                            ["/Pisces (February 19 to March 20)"],
                                                                                                            ["/Aries (March 21-April 19)"],
                                                                                                            ["/Taurus (April 20-May 20)"],
                                                                                                            ["/Gemini (May 21-June 20)"],
                                                                                                            ["/Cancer (June 21-July 22)"],
                                                                                                            ["/Leo (July 23-August 22)"],
                                                                                                            ["/Virgo (August 23-September 22)"],
                                                                                                            ["/Libra (September 23-October 22)"],
                                                                                                            ["/Scorpio (October 23-November 21)"],
                                                                                                            ["/Sagittarius (November 22-December 21)"],
                                                                                                            ["/Capricorn (December 22-January 19)",]
                                                                                                            ]))
    except Exception as e:
        print(e)    

def debug(bot,update):
    global user_data

    print("\ninside debug")
    try:
        out="Users:\n"
        for u in user_data:
            out+=str(u[0])+"\n"
        bot.send_message(chat_id=update.message.chat_id, text=out)
    except Exception as e:
        print(e)

def timeframe_chooser_bknd(bot,update):
    print("inside timeframe_chooser_bknd")
    global user_data
    flag=0
    for ud in user_data:
        if(update.message.chat_id==int(ud[0])):
            flag=1
            ud[1]=update.message.text
    if(flag==0):
        user_data.append([update.message.chat_id,update.message.text,0,0])

    bot.send_message(chat_id=update.message.chat_id,text=update.message.text +" choosen")

    bot.send_message(chat_id=update.message.chat_id, text="Choose sign", reply_markup=ReplyKeyboardMarkup(keyboard=[  ["/start"],["/timeframe"],
                                                                                                            ["/Aquarius (January 20 to February 18)"],
                                                                                                            ["/Pisces (February 19 to March 20)"],
                                                                                                            ["/Aries (March 21-April 19)"],
                                                                                                            ["/Taurus (April 20-May 20)"],
                                                                                                            ["/Gemini (May 21-June 20)"],
                                                                                                            ["/Cancer (June 21-July 22)"],
                                                                                                            ["/Leo (July 23-August 22)"],
                                                                                                            ["/Virgo (August 23-September 22)"],
                                                                                                            ["/Libra (September 23-October 22)"],
                                                                                                            ["/Scorpio (October 23-November 21)"],
                                                                                                            ["/Sagittarius (November 22-December 21)"],
                                                                                                            ["/Capricorn (December 22-January 19)",]
                                                                                                            ]))


def timeframe_chooser(bot,update):
    
    bot.send_message(chat_id=update.message.chat_id, text="Choose timeframe", reply_markup=ReplyKeyboardMarkup(keyboard=[  ["/daily"],
                                                                                                                              ["/weekly"],
                                                                                                                              ["/monthly"]],one_time_keyboard= False))


            


def send_horoscope(bot,update,sunsign):
    global user_data

    for ud in user_data:
      if(update.message.chat_id==int(ud[0])):
            timeFrame=ud[1]
            break


    print("inside send_horoscope")
    try:
        url = "http://www.ganeshaspeaks.com/horoscopes/" + timeFrame.lower() + "-horoscope/"+ sunsign.lower()
        response = requests.get(url)
        tree = html.fromstring(response.content)
        date = str(tree.xpath(
                "//*[@id=\"daily\"]/div/div[1]/div[1]/div[2]/div/p/text()"))
        date = date.replace("']", "").replace("['", "")
        horoscope = str(tree.xpath(
                "//*[@id=\"daily\"]/div/div[1]/div[2]/p[1]/text()"))
        horoscope = horoscope.replace("\\n", "").replace("  ", "").replace("[\"", "").replace("\"]", "")
        horoscope=str(horoscope.replace("\']", "").replace("[\'","").replace("[u\'","").replace("[u\"",""))
        #print(horoscope)
        bot.send_message(chat_id=ud[0],text="*"+timeFrame.upper().replace("/","")+"-HOROSCOPE*\n"+horoscope,parse_mode='Markdown')
    except Exception as e:
        print(e)





def choose_sign_bknd(bot,update):
        
    global sunsign
    global user_data
    t=""
    flag=0
    for ud in user_data:
        if(int(ud[0])==update.message.chat_id):
            t="Bump!\nOldUser!"+"\n*"+str(update.message.from_user.full_name)+"*\n@"+str(update.message.from_user.username)
            flag=1
            break

    if(flag==0):
        t="Bump!\nNewUser!"+"\n*"+str(update.message.from_user.full_name)+"*\n@"+str(update.message.from_user.username)
        user_data.append([update.message.chat_id,"daily",0,0])

    bot.send_message(chat_id=admin_id,text=t,parse_mode='Markdown', disable_web_page_preview=True)

    print("inside choose_sign_bknd\n")
    if(update.message.text=='/Aquarius (January 20 to February 18)' or update.message.text=='/Aquarius'):
        sunsign="aquarius"
        
    elif(update.message.text=="/Pisces (February 19 to March 20)" or update.message.text=='/Pisces'):
          sunsign="Pisces"
    elif(update.message.text=="/Aries (March 21-April 19)" or update.message.text=='/Aries'):
         sunsign="Pisces"
    elif(update.message.text=="/Taurus (April 20-May 20)" or update.message.text=='/Taurus'):
          sunsign="Aries"
    elif(update.message.text=="/Gemini (May 21-June 20)" or update.message.text=='/Gemini'):
         sunsign="Gemini"
    elif(update.message.text=="/Cancer (June 21-July 22)" or update.message.text=='/Cancer'):
          sunsign="Cancer"
    elif(update.message.text=="/Leo (July 23-August 22)" or update.message.text=='/Leo'):
          sunsign="Leo"
    elif(update.message.text=="/Virgo (August 23-September 22)" or update.message.text=='/Virgo'):
          sunsign="Virgo"
    elif(update.message.text=="/Libra (September 23-October 22)" or update.message.text=='/Libra'):
          sunsign="Libra"
    elif(update.message.text=="/Scorpio (October 23-November 21)" or update.message.text=='/Scorpio'):
          sunsign="Scorpio"
    elif(update.message.text=="/Sagittarius (November 22-December 21)" or update.message.text=='/Sagittarius'):
          sunsign="Sagittarius"
    elif(update.message.text=="/Capricorn (December 22-January 19)" or update.message.text=='/Capricorn'):
          sunsign="Capricorn"

    update_clicks(update.message.chat_id)
    jq.run_once(send_horoscope(bot,update,sunsign), 0)   
    













#handlers
start_handler = CommandHandler('start', start)
debug_handler=CommandHandler('debug',debug)


#dispatchers
dispatcher.add_handler(start_handler)
dispatcher.add_handler(CommandHandler(["daily","weekly","monthly"], timeframe_chooser_bknd) )
dispatcher.add_handler(CommandHandler(["Aquarius",
                                       "Pisces", 
                                       "Aries", 
                                       "Taurus",
                                       "Gemini",
                                       "Cancer", 
                                       "Leo", 
                                       "Virgo" ,
                                       "Libra" ,
                                       "Scorpio",
                                       "Sagittarius" ,
                                       "Capricorn"], 
                                        choose_sign_bknd))


dispatcher.add_handler(CommandHandler("timeframe",timeframe_chooser))
dispatcher.add_handler(CommandHandler("analytics",analytics_bknd))
dispatcher.add_handler(debug_handler)


updater.start_polling()

if __name__ == "__main__":
    init_bknd()