import telebot
import requests
import time
import os

# توكن بوت Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHANNEL_USERNAME = '@djimi25'  # اسم القناة الخاصة بك
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    # التحقق من اشتراك المستخدم في القناة
    user_id = message.from_user.id
    chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)

    if chat_member.status in ['member', 'administrator', 'creator']:
        bot.send_message(message.chat.id, 'حط نيميرو🥷🏻🥶:')
        bot.register_next_step_handler(message, get_phone_number)
    else:
        # إرسال رسالة تطلب الاشتراك في القناة
        bot.send_message(message.chat.id, f'يرجى الاشتراك في القناة: {CHANNEL_USERNAME} ثم أرسل "/start" للاستمرار.')

@bot.message_handler(commands=['reset'])
def reset_bot(message):
    bot.send_message(message.chat.id, 'Bot has been reset.')

def get_phone_number(message):
    num = message.text
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'ibiza.ooredoo.dz',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.3',
    }

    data = {
        'client_id': 'ibiza-app',
        'grant_type': 'password',
        'mobile-number': num,
        'language': 'AR',
    }

    response = requests.post('https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token', headers=headers, data=data)

    if 'ROOGY' in response.text:
        bot.send_message(message.chat.id, 'وصلك رمز .دخل رمز لي وصلك🪩:')
        bot.register_next_step_handler(message, get_otp, num)
    else:
        bot.send_message(message.chat.id, 'Error, please try again later.')

def get_otp(message, num):
    otp = message.text
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'ibiza.ooredoo.dz',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.3',
    }

    data = {
        'client_id': 'ibiza-app',
        'otp': otp,
        'grant_type': 'password',
        'mobile-number': num,
        'language': 'AR',
    }

    response = requests.post('https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token', headers=headers, data=data)
    
    access_token = response.json().get('access_token')
    if access_token:
        url = 'https://ibiza.ooredoo.dz/api/v1/mobile-bff/users/mgm/info/apply'

        headers = {
            'Authorization': f'Bearer {access_token}',
            'language': 'AR',
            'request-id': 'ef69f4c6-2ead-4b93-95df-106ef37feefd',
            'flavour-type': 'gms',
            'Content-Type': 'application/json'
        }

        payload = {
            "mgmValue": "ABC"
        }

        for _ in range(12):
            response = requests.post(url, headers=headers, json=payload)
            
            if 'EU1002' in response.text:
                bot.send_message(message.chat.id, '💦🌚تم ارسال الانترنيت')
            else:
                bot.send_message(message.chat.id, 'تحقق من الانترنت🖤')

            time.sleep(5)  # تأخير 5 ثواني

    else:
        bot.send_message(message.chat.id, 'Error verifying OTP.')

@bot.message_handler(func=lambda message: message.text not in ['/start', '/reset'], content_types=['text'])
def handle_invalid_command(message):
    bot.send_message(message.chat.id, 'Invalid command. Please start with /start or /reset')

bot.polling(none_stop=True)
