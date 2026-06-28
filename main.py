import os
import time
import threading
from flask import Flask
import telebot
from telebot import types
from supabase import create_client, Client  # Supabase লাইব্রেরি ইমপোর্ট করা হলো

# --- ফ্লাস্ক সার্ভার (Render-এ বট ২৪ ঘণ্টা সচল রাখার জন্য) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# --- SUPABASE কনফিগারেশন (আপনার দেওয়া ক্রেডেনশিয়ালস যুক্ত করা হয়েছে) ---
SUPABASE_URL = "https://wgpoyvvzeswfuzrpckko.supabase.co" 
SUPABASE_KEY = "sb_publishable_atz0HT-PufBxiQIkNCIHVw_RPlPssgT" 

# Supabase ক্লায়েন্ট তৈরি করা
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- ডাটাবেজ ফাংশনসমূহ (Supabase API) ---

def add_user(user_id):
    try:
        # upsert ব্যবহার করলে ইউজার অলরেডি থাকলে নতুন করে সেভ হবে না এবং কোনো এররও দেবে না
        supabase.table("users").upsert({"user_id": user_id}).execute()
    except Exception as e:
        print(f"Error saving user to Supabase: {e}")

def get_all_users():
    try:
        response = supabase.table("users").select("user_id").execute()
        # সফল রেসপন্স থেকে ইউজার আইডিগুলোর লিস্ট বের করা
        users = [row["user_id"] for row in response.data]
        return users
    except Exception as e:
        print(f"Error fetching users from Supabase: {e}")
        return []

# --- টেলিগ্রাম বট কনফিগারেশন ---
BOT_TOKEN = "8276327075:AAHA-7nrNfRhLCauU90xfuXV3-v2vhiURdE"
bot = telebot.TeleBot(BOT_TOKEN)

ADMIN_1 = "SUNNY_BRO1"
ADMIN_2 = "SPECIAL_7_9"

# ইমেজ লিঙ্কসমূহ
IMAGE_1 = "https://i.ibb.co/Kpg2fWTx/IMG-20260628-224110-275.jpg"
IMAGE_2 = "https://i.ibb.co/1YNw3TSN/IMG-20260628-224102-850.jpg"
IMAGE_3 = "https://i.ibb.co/27ckLmQt/IMG-20260628-224052-676.jpg"

# --- সেটিংস ---
CHANNELS = [
    "@Free_Script_79", 
    "-1003941084913",  # <-- এখানে আপনার প্রাইভেট চ্যানেলের Numerical ID-টি বসাবেন (যেমন: "-1002187654321")
    "@APPLE_CRASH_HACK11"
] 

CHANNEL_1_LINK = "https://t.me/Free_Script_79"
CHANNEL_2_LINK = "https://t.me/+95pjdAhv0TtkYjc1"
CHANNEL_3_LINK = "https://t.me/APPLE_CRASH_HACK11"

# আপনার সিগনাল ওয়েব অ্যাপের লিঙ্ক
WEBAPP_URL = "https://ghostchannel.unaux.com/" 

# রেজিস্ট্রেশন লিঙ্ক
REGISTRATION_LINK = "https://1xbet-bangladesh.mobi"


# সাবস্ক্রিপশন চেক করার ফাংশন
def is_user_subscribed(user_id):
    for channel in CHANNELS:
        if channel == "-1003941084913":
            continue
        try:
            chat_member = bot.get_chat_member(channel, user_id)
            if chat_member.status in ['left', 'kicked']:
                return False
        except Exception as e:
            print(f"Error checking subscription for {channel}: {e}")
            return False
    return True

def is_admin_1(username):
    return username and username.lower() == ADMIN_1.lower()

def is_admin_2(username):
    return username and username.lower() == ADMIN_2.lower()

# --- বট হ্যান্ডলারস ---

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    add_user(user_id)  # Supabase-এ সেভ করা হচ্ছে

    if is_user_subscribed(user_id):
        send_step_2(chat_id)
    else:
        send_step_1(chat_id)

def send_step_1(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    btn1 = types.InlineKeyboardButton("Join Channel 1 📢", url=CHANNEL_1_LINK)
    btn2 = types.InlineKeyboardButton("Join Channel 2 🔒", url=CHANNEL_2_LINK)
    btn3 = types.InlineKeyboardButton("Join Channel 3 📢", url=CHANNEL_3_LINK)
    btn_check = types.InlineKeyboardButton("✅ Joined", callback_data="check_subscription")
    
    markup.add(btn1, btn2, btn3, btn_check)

    caption_text = (
        "⚠️ **Access Denied!**\n\n"
        "To use this bot, you must join our 3 official channels first.\n"
        "Please click the buttons below to join, then click **'Joined'**."
    )
    
    bot.send_photo(chat_id, photo=IMAGE_1, caption=caption_text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_sub_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    add_user(user_id)

    if is_user_subscribed(user_id):
        bot.answer_callback_query(call.id, "Verification Successful! ✅")
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

@bot.callback_query_handler(func=lambda call: call.data == "i_register_clicked")
def i_register_callback(call):
    chat_id = call.message.chat.id
    
    msg = bot.send_message(
        chat_id, 
        "📝 **Please send your 1xBet or Melbet Account ID (numbers only):**", 
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(msg, process_account_id)

def process_account_id(message):
    chat_id = message.chat.id
    user_input = message.text

    if not user_input.isdigit():
        msg = bot.reply_to(
            message, 
            "❌ **Invalid ID!** Please send a valid numerical ID (e.g., 12345678):", 
            parse_mode="Markdown"
        )
        bot.register_next_step_handler(msg, process_account_id)
        return

    loading_msg = bot.send_message(chat_id, "Checking database... Please wait 5 seconds ⏳")
    
    time.sleep(5)

    try:
        bot.delete_message(chat_id, loading_msg.message_id)
    except Exception:
        pass

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


# ==========================================
#         🛠️ অ্যাডমিন প্যানেল কন্ট্রোল 🛠️
# ==========================================

@bot.message_handler(commands=['admin'])
def admin_panel_cmd(message):
    username = message.from_user.username
    chat_id = message.chat.id

    if is_admin_1(username):
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_broadcast = types.InlineKeyboardButton("📢 Broadcast to Users", callback_data="admin_broadcast")
        btn_channel = types.InlineKeyboardButton("📤 Post to Channel", callback_data="admin_post_channel")
        btn_stats = types.InlineKeyboardButton("📊 Bot Stats", callback_data="admin_stats")
        markup.add(btn_broadcast, btn_channel, btn_stats)
        
        bot.send_message(chat_id, "👑 **Welcome Admin 1 (Full Controls)**\nSelect an option below:", parse_mode="Markdown", reply_markup=markup)
        
    elif is_admin_2(username):
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_broadcast = types.InlineKeyboardButton("📢 Broadcast to Users", callback_data="admin_broadcast")
        markup.add(btn_broadcast)
        
        bot.send_message(chat_id, "👤 **Welcome Admin 2 (Broadcast Only)**\nSelect an option below:", parse_mode="Markdown", reply_markup=markup)
        
    else:
        bot.send_message(chat_id, "❌ **Access Denied.** You are not authorized to use this command.")

# --- ১. স্ট্যাটাস চেক (Admin 1 Only) ---
@bot.callback_query_handler(func=lambda call: call.data == "admin_stats")
def show_stats_callback(call):
    username = call.from_user.username
    if not is_admin_1(username):
        bot.answer_callback_query(call.id, "Unauthorized!")
        return
        
    users = get_all_users()
    bot.send_message(call.message.chat.id, f"📊 **Bot Stats:**\n\nTotal Users in database: **{len(users)}**", parse_mode="Markdown")
    bot.answer_callback_query(call.id)

# --- ২. ব্রডকাস্ট প্রসেস (Admin 1 & Admin 2 Both) ---
@bot.callback_query_handler(func=lambda call: call.data == "admin_broadcast")
def start_broadcast_callback(call):
    username = call.from_user.username
    if not (is_admin_1(username) or is_admin_2(username)):
        bot.answer_callback_query(call.id, "Unauthorized!")
        return

    msg = bot.send_message(call.message.chat.id, "💬 Please send the post (Text, Photo, or Video) you want to broadcast to all users:")
    bot.register_next_step_handler(msg, process_broadcast)
    bot.answer_callback_query(call.id)

def process_broadcast(message):
    username = message.from_user.username
    if not (is_admin_1(username) or is_admin_2(username)):
        return

    users = get_all_users()
    if not users:
        bot.send_message(message.chat.id, "❌ No users found in database!")
        return

    status_msg = bot.send_message(message.chat.id, f"🚀 Broadcasting to {len(users)} users. Please wait...")
    
    sent_count = 0
    fail_count = 0

    for user_id in users:
        try:
            if message.content_type == 'text':
                bot.send_message(user_id, message.text, entities=message.entities)
            elif message.content_type == 'photo':
                bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption, caption_entities=message.caption_entities)
            elif message.content_type == 'video':
                bot.send_video(user_id, message.video.file_id, caption=message.caption, caption_entities=message.caption_entities)
            else:
                bot.copy_message(user_id, message.chat.id, message.message_id)
            sent_count += 1
        except Exception:
            fail_count += 1

    bot.edit_message_text(
        f"✅ **Broadcast Completed!**\n\nSuccessful: {sent_count}\nFailed/Blocked: {fail_count}",
        message.chat.id,
        status_msg.message_id,
        parse_mode="Markdown"
    )

# --- ৩. সরাসরি চ্যানেলে পোস্ট করার প্রসেস (Admin 1 Only) ---
@bot.callback_query_handler(func=lambda call: call.data == "admin_post_channel")
def select_channel_callback(call):
    username = call.from_user.username
    if not is_admin_1(username):
        bot.answer_callback_query(call.id, "Unauthorized! Admin 1 only.")
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    for idx, channel in enumerate(CHANNELS):
        label = f"Post to Channel {idx+1} ({channel})"
        btn = types.InlineKeyboardButton(label, callback_data=f"post_to_ch_{idx}")
        markup.add(btn)
        
    bot.send_message(call.message.chat.id, "Select the target channel where you want to publish the post:", reply_markup=markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("post_to_ch_"))
def ask_post_content_callback(call):
    username = call.from_user.username
    if not is_admin_1(username):
        return

    channel_idx = int(call.data.split("_")[-1])
    target_channel_id = CHANNELS[channel_idx]

    msg = bot.send_message(call.message.chat.id, f"📝 Send the content (Text, Photo, or Video) you want to post directly in **{target_channel_id}**:")
    bot.register_next_step_handler(msg, lambda message: process_channel_post(message, target_channel_id))
    bot.answer_callback_query(call.id)

def process_channel_post(message, channel_id):
    username = message.from_user.username
    if not is_admin_1(username):
        return

    try:
        if message.content_type == 'text':
            bot.send_message(channel_id, message.text, entities=message.entities)
        elif message.content_type == 'photo':
            bot.send_photo(channel_id, message.photo[-1].file_id, caption=message.caption, caption_entities=message.caption_entities)
        elif message.content_type == 'video':
            bot.send_video(channel_id, message.video.file_id, caption=message.caption, caption_entities=message.caption_entities)
        else:
            bot.copy_message(channel_id, message.chat.id, message.message_id)
            
        bot.send_message(message.chat.id, f"✅ Successfully posted to **{channel_id}**!", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(
            message.chat.id, 
            f"❌ **Failed to send post to {channel_id}!**\n\n**Error Details:** `{e}`",
            parse_mode="Markdown"
        )


# --- রান প্রসেস ---
if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    print("Bot is starting with Supabase Database...")
    bot.infinity_polling()
