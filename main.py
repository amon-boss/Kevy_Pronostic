import os
import time
import threading
from datetime import datetime
from telebot import TeleBot
from keep_alive import keep_alive  # Lance un serveur Flask pour Render

BOT_TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = int(os.environ['CHANNEL_ID'])

bot = TeleBot(BOT_TOKEN)

# ✅ Message motivant du matin
MOTIVATION_MSG = (
    "🌞 *Bonjour champions !* 🌞\n\n"
    "💪 \"Le succès appartient à ceux qui se lèvent tôt et misent avec détermination!\"\n"
    "🔥 Prêt.e.s à gagner aujourd’hui ? 🚀"
)

# ✅ Message de clôture du soir
EVENING_MSG = (
    "🌙 *Bonsoir la team !* 🌙\n\n"
    "🎉 Comment s’est passée ta journée de paris ?\n"
    "📊 Dis-nous tout avec le sondage ci-dessous !"
)

# 🔁 Envoi automatique le matin
def send_morning_message():
    try:
        bot.send_message(CHANNEL_ID, MOTIVATION_MSG, parse_mode='Markdown')
        bot.send_poll(
            CHANNEL_ID,
            "🎯 Es-tu prêt(e) pour une nouvelle journée de gain ?",
            ["✅ Oui, toujours prêt(e)!", "❌ Pas encore, mais j’y crois!"],
            is_anonymous=False
        )
    except Exception as e:
        print(f"Erreur message du matin : {e}")

# 🔁 Envoi automatique le soir
def send_evening_message():
    try:
        bot.send_message(CHANNEL_ID, EVENING_MSG, parse_mode='Markdown')
        bot.send_poll(
            CHANNEL_ID,
            "📈 Ta journée a-t-elle été gagnante ou perdante ?",
            ["🏆 Gagnante 💰", "😞 Perdante 😓"],
            is_anonymous=False
        )
    except Exception as e:
        print(f"Erreur message du soir : {e}")

# ⏰ Horaires programmés
def scheduled_messages():
    already_sent_morning = False
    already_sent_evening = False
    while True:
        now = datetime.now()
        if now.hour == 6 and now.minute == 30:
            if not already_sent_morning:
                send_morning_message()
                already_sent_morning = True
                already_sent_evening = False
        elif now.hour == 22 and now.minute == 30:
            if not already_sent_evening:
                send_evening_message()
                already_sent_evening = True
                already_sent_morning = False
        else:
            already_sent_morning = False
            already_sent_evening = False
        time.sleep(20)

# 📲 Commande /poll manuelle
@bot.message_handler(commands=['poll'])
def create_poll(message):
    if message.chat.id == CHANNEL_ID:
        try:
            bot.send_poll(
                CHANNEL_ID,
                "📊 Quel est ton pronostic pour le prochain match ?",
                ["1️⃣ Victoire domicile", "2️⃣ Match nul", "3️⃣ Victoire extérieur"],
                is_anonymous=False
            )
        except Exception as e:
            bot.send_message(CHANNEL_ID, f"⚠️ Erreur création sondage : {e}")

# 🎉 Message de bienvenue
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        name = new_member.first_name
        bot.send_message(message.chat.id, f"🎉 Bienvenue {name} dans le groupe ! Prêt.e à gagner ? 💸🔥")

# 👋 Message d'au revoir
@bot.message_handler(content_types=['left_chat_member'])
def goodbye_member(message):
    name = message.left_chat_member.first_name
    bot.send_message(message.chat.id, f"👋 {name} vient de quitter le groupe. À bientôt... ou pas 😅")

# ▶️ Lancement du bot
if __name__ == "__main__":
    keep_alive()  # Pour Render
    threading.Thread(target=scheduled_messages, daemon=True).start()
    print("🤖 Bot paris sportifs fun, motivant et social actif ✅")
    bot.infinity_polling()
