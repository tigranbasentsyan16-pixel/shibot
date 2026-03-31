from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import datetime

from config import BOT_TOKEN
from users import set_user_group, get_user_group
from sheets import get_schedule_for_group
from reminders import add_reminder, get_all_reminders


# 🔹 helper (վաղվա text)
def build_tomorrow_text(group, data):
    days = list(data.keys())
    lessons = ["1-2", "3-4", "5-6", "7-8"]

    today_index = datetime.datetime.today().weekday()
    tomorrow_index = today_index + 1

    if tomorrow_index >= 5:
        tomorrow_index = 0

    day = days[tomorrow_index]
    subjects = data[day]

    text = f"📅 Վաղվա դասացուցակ — {group}\n\n"
    text += f"📘 {day}\n"

    for i in range(len(lessons)):
        subject = subjects[i] if i < len(subjects) else ""
        text += f"{lessons[i]} → {subject}\n"

    return text


# 🔹 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📅 Այսօրվա դասերը", "📅 Վաղվա դասերը"],
        ["📊 Ամբողջ դասացուցակ"],
        ["⏰ Reminder դնել"],
        ["⚙️ Սահմանել խումբ"],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Բարև 👋 Ընտրիր գործողություն",
        reply_markup=reply_markup
    )


# 🔹 /group
async def set_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Օգտագործում՝ /group ###")
        return

    group = context.args[0]
    user_id = update.effective_user.id

    set_user_group(user_id, group)

    await update.message.reply_text(f"✅ Քո խումբը պահպանվեց՝ {group}")


# 🔹 /schedule
async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    group = get_user_group(user_id)

    if not group:
        await update.message.reply_text("❗ Նախ գրիր քո խումբը՝ /group ###")
        return

    data = get_schedule_for_group(group)

    if not data:
        await update.message.reply_text("❌ Տվյալներ չգտնվեցին")
        return

    lessons = ["1-2", "3-4", "5-6", "7-8"]

    text = f"📅 Դասացուցակ — {group}\n\n"

    for day, subjects in data.items():
        text += f"📘 {day}\n"

        for i in range(len(lessons)):
            subject = subjects[i] if i < len(subjects) else ""
            text += f"{lessons[i]} → {subject}\n"

        text += "\n"

    await update.message.reply_text(text)


# 🔹 /today
async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    group = get_user_group(user_id)

    if not group:
        await update.message.reply_text("❗ Նախ գրիր քո խումբը՝ /group ###")
        return

    data = get_schedule_for_group(group)

    if not data:
        await update.message.reply_text("❌ Տվյալներ չգտնվեցին")
        return

    days = list(data.keys())
    lessons = ["1-2", "3-4", "5-6", "7-8"]

    today_index = datetime.datetime.today().weekday()
    if today_index >= 5:
        today_index = 0

    day = days[today_index]
    subjects = data[day]

    text = f"📅 Այսօրվա դասացուցակ — {group}\n\n"
    text += f"📘 {day}\n"

    for i in range(len(lessons)):
        subject = subjects[i] if i < len(subjects) else ""
        text += f"{lessons[i]} → {subject}\n"

    await update.message.reply_text(text)


# 🔹 /tomorrow
async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    group = get_user_group(user_id)

    if not group:
        await update.message.reply_text("❗ Նախ գրիր քո խումբը՝ /group ###")
        return

    data = get_schedule_for_group(group)

    if not data:
        await update.message.reply_text("❌ Տվյալներ չգտնվեցին")
        return

    text = build_tomorrow_text(group, data)

    await update.message.reply_text(text)


# 🔹 /remind
async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Օգտագործում՝ /remind HH:MM\nօրինակ՝ /remind 20:00"
        )
        return

    time = context.args[0]
    context.user_data["remind_time"] = time

    keyboard = [["📌 Միայն այսօր"], ["🔁 Ամեն օր"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Ընտրիր reminder-ի ռեժիմը",
        reply_markup=reply_markup
    )


# 🔹 BUTTONS
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if text == "📅 Այսօրվա դասերը":
        await today(update, context)

    elif text == "📅 Վաղվա դասերը":
        await tomorrow(update, context)

    elif text == "📊 Ամբողջ դասացուցակ":
        await schedule(update, context)

    elif text == "⚙️ Սահմանել խումբ":
        await update.message.reply_text("Գրիր՝ /group ###")

    elif text == "⏰ Reminder դնել":
        await update.message.reply_text("Գրիր՝ /remind HH:MM")

    elif text == "📌 Միայն այսօր":
        time = context.user_data.get("remind_time")
        add_reminder(user_id, time, "once")
        await update.message.reply_text(f"⏰ Reminder դրվեց {time} (միայն այսօր)")

    elif text == "🔁 Ամեն օր":
        time = context.user_data.get("remind_time")
        add_reminder(user_id, time, "daily")
        await update.message.reply_text(f"⏰ Reminder դրվեց {time} (ամեն օր)")


# 🔹 JOB QUEUE
async def check_reminders(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.now().strftime("%H:%M")
    data = get_all_reminders()

    for user_id, reminders in data.items():
        group = get_user_group(int(user_id))

        if not group:
            continue

        schedule_data = get_schedule_for_group(group)

        for r in reminders:
            if r["time"] == now:
                try:
                    text = build_tomorrow_text(group, schedule_data)

                    await context.bot.send_message(
                        chat_id=int(user_id),
                        text=f"⏰ Reminder\n\n{text}",
                    )
                except:
                    pass


# 🔹 MAIN
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("group", set_group))
    app.add_handler(CommandHandler("schedule", schedule))
    app.add_handler(CommandHandler("today", today))
    app.add_handler(CommandHandler("tomorrow", tomorrow))
    app.add_handler(CommandHandler("remind", remind))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    # ✅ JOB QUEUE
    job_queue = app.job_queue
    job_queue.run_repeating(check_reminders, interval=60, first=10)

    print("🤖 Bot-ը աշխատում է...")
    app.run_polling()


if __name__ == "__main__":
    main()