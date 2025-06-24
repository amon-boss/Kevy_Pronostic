import os
import time
import threading
from datetime import datetime
from telebot import TeleBot
from keep_alive import keep_alive  # Import du serveur Flask

BOT_TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = int(os.environ['CHANNEL_ID'])

bot = TeleBot(BOT_TOKEN)

# Citation motivante du matin (toujours la même)
MOTIVATION_MSG = (
    "🌞 *Bonjour champions !* 🌞\n\n"
    "💪 \"Le succès appartient à ceux qui se lèvent tôt et misent avec détermination!\"\n"
    "🔥 Prêt.e.s à gagner aujourd’hui ? 🚀"
)

# Message du soir
EVENING_MSG = (
    "🌙 *Bonsoir la team !* 🌙\n\n"
    "🎉 Comment s’est passée ta journée de paris ?\n"
    "📊 Dis-nous tout avec le sondage ci-dessous !"
)

def send_morning_message():
    try:
        bot.send_message(CHANNEL_ID, MOTIVATION_MSG, parse_mode='Markdown')
        bot.send_poll(CHANNEL_ID,
                      "🎯 Es-tu prêt(e) pour une nouvelle journée de gain ?",
                      ["✅ Oui, toujours prêt(e)!", "❌ Pas encore, mais j’y crois!"],
                      is_anonymous=False)
    except Exception as e:
        print(f"Erreur message du matin : {e}")

def send_evening_message():
    try:
        bot.send_message(CHANNEL_ID, EVENING_MSG, parse_mode='Markdown')
        bot.send_poll(CHANNEL_ID,
                      "📈 Ta journée a-t-elle été gagnante ou perdante ?",
                      ["🏆 Gagnante 💰", "😞 Perdante 😓"],
                      is_anonymous=False)
    except Exception as e:
        print(f"Erreur message du soir : {e}")

def scheduled_messages():
    already_sent_morning = False
    already_sent_evening = False
    while True:
        now = datetime.now()
        # Heure matin 6h30
        if now.hour == 6 and now.minute == 30:
            if not already_sent_morning:
                send_morning_message()
                already_sent_morning = True
                already_sent_evening = False
        # Heure soir 22h30
        elif now.hour == 22 and now.minute == 30:
            if not already_sent_evening:
                send_evening_message()
                already_sent_evening = True
                already_sent_morning = False
        else:
            # Reset les flags en dehors des horaires précis
            already_sent_morning = False
            already_sent_evening = False
        time.sleep(20)

@bot.message_handler(commands=['poll'])
def create_poll(message):
    if message.chat.id == CHANNEL_ID:
        question = "Quel est ton pronostic pour le prochain match ?"
        options = ["1️⃣ Victoire domicile", "2️⃣ Match nul", "3️⃣ Victoire extérieur"]
        try:
            bot.send_poll(CHANNEL_ID, question, options, is_anonymous=False)
        except Exception as e:
            bot.send_message(CHANNEL_ID, f"⚠️ Erreur création sondage : {e}")

if __name__ == "__main__":
    keep_alive()  # Lance le serveur web Flask pour Render
    threading.Thread(target=scheduled_messages, daemon=True).start()
    print("🤖 Bot paris sportifs fun et motivant actif ✅")
    bot.infinity_polling()
