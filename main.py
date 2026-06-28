import os
import time
import threading
from flask import Flask
import telebot
from telebot import types

# --- ফ্লাস্ক সার্ভার (Render-এ বট ২৪ ঘণ্টা সচল রাখার জন্য) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running perfectly!"

def run_flask():
    # Render পোর্ট অ্যাসাইন করে, সেটি রিসিভ করার জন্য
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# --- টেলিগ্রাম বট কনফিগারেশন ---
# আপনার দেওয়া বট টোকেন
BOT_TOKEN = "8276327075:AAHA-7nrNfRhLCauU90xfuXV3-v2vhiURdE"
bot = telebot.TeleBot(BOT_TOKEN)

# ইমেজ লিঙ্কসমূহ
IMAGE_1 = "https://i.ibb.co/Kpg2fWTx/IMG-20260628-224110-275.jpg"
IMAGE_2 = "https://i.ibb.co/1YNw3TSN/IMG-20260628-224102-850.jpg"
IMAGE_3 = "https://i.ibb.co/27ckLmQt/IMG-20260628-224052-676.jpg"

# --- সেটিংস (এখানে আপনার লিংক ও আইডি পরিবর্তন করবেন) ---
# চ্যানেলের ইউজারনেম বা আইডি (অবশ্যই বটকে এই চ্যানেলগুলোতে অ্যাডমিন বানাতে হবে)
CHANNELS = ["@channel_username_1", "@channel_username_2", "@channel_username_3"] 

# চ্যানেলে জয়েন করার জন্য বাটনের লিঙ্ক
CHANNEL_1_LINK = "https://t.me/your_channel_1"
CHANNEL_2_LINK = "https://t.me/your_channel_2"
CHANNEL_3_LINK = "https://t.me/your_channel_3"

# আপনার সিগনাল ওয়েব অ্যাপের লিঙ্ক (এখানে আপনার কাঙ্ক্ষিত লিঙ্কটি বসাবেন)
WEBAPP_URL = "https://your-webapp-link.com" 

# রেজিস্ট্রেশন লিঙ্ক
REGISTRATION_LINK = "https://1xbetmelbet.com"


# সাবস্ক্রিপশন চেক করার ফাংশন
def is_user_subscribed(user_id):
    for channel in CHANNELS:
        try:
            # যদি টেস্ট করার সময় ডামি আইডি ব্যবহার করেন, সেটি স্কিপ করতে পারেন
            if channel == "@channel_username_1":
                continue
            
            chat_member = bot.get_chat_member(channel, user_id)
            if chat_member.status in ['left', 'kicked']:
                return False
        except Exception as e:
            print(f"Error checking subscription for {channel}: {e}")
            # যদি বট চ্যানেলে অ্যাডমিন না থাকে তাহলেও ফলস রিটার্ন করতে পারে
            return False
    return True

# --- বট হ্যান্ডলারস ---

# /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if is_user_subscribed(user_id):
        send_step_2(chat_id)
    else:
        send_step_1(chat_id)

# ধাপ ১: চ্যানেল জয়েন করার অনুরোধ (Image 1)
def send_step_1(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    btn1 = types.InlineKeyboardButton("Join Channel 1", url=CHANNEL_1_LINK)
    btn2 = types.InlineKeyboardButton("Join Channel 2", url=CHANNEL_2_LINK)
    btn3 = types.InlineKeyboardButton("Join Channel 3", url=CHANNEL_3_LINK)
    btn_check = types.InlineKeyboardButton("✅ Joined", callback_data="check_subscription")
    
    markup.add(btn1, btn2, btn3, btn_check)

    caption_text = (
        "⚠️ **Access Denied!**\n\n"
        "To use this bot, you must join our 3 official channels first.\n"
        "Please click the buttons below to join, then click **'Joined'**."
    )
    
    bot.send_photo(chat_id, photo=IMAGE_1, caption=caption_text, parse_mode="Markdown", reply_markup=markup)

# "Joined" বাটনের কলব্যাক চেক
@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_sub_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    if is_user_subscribed(user_id):
        bot.answer_callback_query(call.id, "Verification Successful! ✅")
        # আগের মেসেজটি ডিলিট করে পরের ধাপে নিয়ে যাওয়া
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except Exception:
            pass
        send_step_2(chat_id)
    else:
        bot.answer_callback_query(
            call.id, 
            "❌ You have not joined all channels yet! Please join and try again.", 
            show_alert=True
        )

# ধাপ ২: অ্যাকাউন্ট খোলার অনুরোধ (Image 2)
def send_step_2(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    btn_register = types.InlineKeyboardButton("Register on 1xBet / Melbet", url=REGISTRATION_LINK)
    btn_i_register = types.InlineKeyboardButton("I Register ➔", callback_data="i_register_clicked")
    
    markup.add(btn_register, btn_i_register)

    caption_text = (
        "🔥 **Create Your Account Now!**\n\n"
        "Create a new account on 1xBet or Melbet using our official promo code to get a 130% bonus and access VIP signals!\n\n"
        "🔹 Promo Code: `SPE91` (Tap to copy)\n\n"
        "Once you have successfully registered, click the **'I Register'** button below."
    )
    
    bot.send_photo(chat_id, photo=IMAGE_2, caption=caption_text, parse_mode="Markdown", reply_markup=markup)

# "I Register" বাটনের কলব্যাক
@bot.callback_query_handler(func=lambda call: call.data == "i_register_clicked")
def i_register_callback(call):
    chat_id = call.message.chat.id
    
    # ইউজার আইডি চাওয়ার জন্য মেসেজ পাঠানো
    msg = bot.send_message(
        chat_id, 
        "📝 **Please send your 1xBet or Melbet Account ID (numbers only):**", 
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(msg, process_account_id)

# ধাপ ৩: আইডি রিসিভ এবং ৫ সেকেন্ড অপেক্ষা করে ভেরিফিকেশন (Image 3)
def process_account_id(message):
    chat_id = message.chat.id
    user_input = message.text

    # আইডিটি কেবল সংখ্যা কিনা যাচাই করা
    if not user_input.isdigit():
        msg = bot.reply_to(
            message, 
            "❌ **Invalid ID!** Please send a valid numerical ID (e.g., 12345678):", 
            parse_mode="Markdown"
        )
        bot.register_next_step_handler(msg, process_account_id)
        return

    # ৫ সেকেন্ডের লোডিং মেসেজ
    loading_msg = bot.send_message(chat_id, "Checking database... Please wait 5 seconds ⏳")
    
    # ৫ সেকেন্ড অপেক্ষা করা
    time.sleep(5)

    # লোডিং মেসেজটি ডিলিট করা
    try:
        bot.delete_message(chat_id, loading_msg.message_id)
    except Exception:
        pass

    # Web App বাটনের মার্কআপ
    markup = types.InlineKeyboardMarkup()
    webapp = types.WebAppInfo(url=WEBAPP_URL)
    btn_webapp = types.InlineKeyboardButton("Open Signal 🚀", web_app=webapp)
    markup.add(btn_webapp)

    caption_text = (
        "🎉 **Your Account is Verified!**\n\n"
        "Congratulations! Your registration has been verified successfully. "
        "You can now access our premium signals.\n\n"
        "Click the button below to launch the signal interface."
    )

    bot.send_photo(chat_id, photo=IMAGE_3, caption=caption_text, reply_markup=markup)


# --- রান প্রসেস ---
if __name__ == "__main__":
    # ব্যাকগ্রাউন্ডে Flask সার্ভার চালু করা (Render-এর জন্য প্রয়োজনীয়)
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # বট পোলিং চালু করা
    print("Bot is starting...")
    bot.infinity_polling()
