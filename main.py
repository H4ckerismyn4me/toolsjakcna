import telebot
import requests
import re
import random
import time
from telebot import types

# Inicializar el bot de Telegram
bot = telebot.TeleBot('6242455677:AAG_ppRXmKX35-gFcgF73Ibh-NNuz5IEbZA')

# Obtener el ID del chat del grupo donde se enviarán los mensajes
desired_group_id = -1001705921036
# Obtener el ID del chat del grupo
chat_id = -847232369

emoji_list = ['🌌','🌃', '🏙', '🎇', '🌅', '🌉', ' 🏞', '🎆']

# Definir el mensaje personalizado con la información de la tarjeta de crédito
message_template = 'Approved 𝘾𝘾𝙉/𝘾𝙑𝙑 ✅\n' \
                   '╭══════════ ♤ ══════════╮\n' \
                   '<b>[ {random_emoji} ]</b> <code>{tarjeta}|{mes}|{año}|{cvv}</code>\n' \
                   ' ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄\n' \
                   '• <b>𝗧𝘆𝗽𝗲:</b> <code>{scheme} - {type}</code>\n' \
                   '• <b>𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {pais}</b>\n' \
                   '• <b>𝗕𝗮𝗻𝗸: {banco}</b>\n' \
                   '╰══════════ ♤ ══════════╯\n' \
                   '𝙀𝙭𝙩𝙧𝙖: <code>{tarjeta_x}|{mes}|{año}</code>'
# Función para obtener la información de BIN utilizando la API de binlist.net
def get_bin_info(bin_number):
    response = requests.get(f'https://lookup.binlist.net/{bin_number}')
    data = response.json()
    country = data.get('country', {}).get('name', 'Unknown').upper()
    bank = data.get('bank', {}).get('name', 'Unknown')
    card_type = data.get('type', 'Unknown').upper()
    scheme = data.get('scheme', 'Unknown').upper()
    return country, bank, card_type, scheme



# ID de chat del usuario permitido
allowed_chat_id = 1787128910

# Configurar el bot para recibir y procesar mensajes
@bot.message_handler(func=lambda message: True, content_types=['text'])

def send_to_group(message):
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text="o w n e r 🧸", url="https://t.me/hackerismyname")
    markup.add(itembtn1)
    # Verificar si el mensaje proviene del ID de chat permitido
    if message.chat.type == 'private' and message.chat.id != allowed_chat_id:
        # Enviar un mensaje de error al usuario
        bot.reply_to(message, 'Lo siento, no estás autorizado para usar este bot 🧸.')
        return

    # Si el mensaje fue enviado por privado o en el grupo deseado, buscar la línea que contiene la información de la tarjeta de crédito
    if message.chat.type == 'private' or message.chat.id == desired_group_id:
        # Separar el mensaje en líneas
        lines = message.text.split('\n')

        # Buscar la línea que contiene la información de la tarjeta de crédito utilizando una expresión regular
        card_info = None
        pattern = re.compile(r'\d{16}\|\d{2}\|\d{4}\|\d{3}')
        for line in lines:
            match = pattern.search(line)
            if match:
                card_info = match.group(0)
                break

        # Si se encontró la línea con la información de la tarjeta de crédito, enviarla al grupo correspondiente
        if card_info:
            # Separar la información de la tarjeta de crédito utilizando el separador '|'
            card_fields = card_info.split('|')

            # Obtener la información de BIN utilizando los primeros 6 dígitos de la tarjeta de crédito
            bin_number = card_fields[0][:6]
            country, bank, card_type, scheme = get_bin_info(bin_number)
            card_info_x = card_fields[0][:-4] + 'xxxx'
            # Crear el mensaje personalizado utilizando la plantilla y los valores correspondientes
            custom_message = message_template.format(tarjeta=card_fields[0],
                                                      mes=card_fields[1],
                                                      año=card_fields[2],
                                                      cvv=card_fields[3],
                                                      pais=country,
                                                      banco=bank,
                                                      type=card_type,
                                                      scheme=scheme,
                                                      random_emoji=random.choice(emoji_list),
                                                      tarjeta_x=card_info_x)

            

            # Enviar el mensaje personalizado al chat del grupo correspondiente
            bot.send_message(chat_id, custom_message, parse_mode='HTML', reply_markup=markup)
                
            # Si el mensaje proviene de un chat privado, enviar un mensaje al usuario indicando que el mensaje se ha reenviado al grupo
            if message.chat.type == 'private':
                bot.reply_to(message, 'Mensaje enviado.')

bot.polling()
