
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
import json
import os
import pandas as pd

TOKEN = "8174580404:AAEP0SgZWgEcBlIOx8n_d02T8ei38oe0JRI"
DATA_FILE = "user_data.json"
CONFIG, LOG, LIMIT = range(3)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def start(update, context):
    update.message.reply_text("👋 Привет! Я — твой финансовый помощник.\nИспользуй /help, чтобы узнать команды.")

def help_command(update, context):
    update.message.reply_text(
        "📌 Команды:\n"
        "/start — начать\n"
        "/help — помощь\n"
        "/config — задать доход и категории\n"
        "/log — добавить запись\n"
        "/summary — фин.сводка\n"
        "/categorysummary — расходы по категориям\n"
        "/export — экспортировать в Excel\n"
        "/setlimit — задать лимит\n"
        "/notifyon — включить уведомления\n"
        "/notifyoff — отключить уведомления"
    )

def config(update, context):
    update.message.reply_text("Введите: доход, категории через запятую\nПример: 200000, еда, транспорт, учёба")
    return CONFIG

def save_config(update, context):
    user_id = str(update.message.from_user.id)
    parts = update.message.text.split(",")
    if len(parts) < 2:
        update.message.reply_text("❌ Неверный формат.")
        return CONFIG
    income = int(parts[0].strip())
    categories = [x.strip() for x in parts[1:]]
    data = load_data()
    data[user_id] = {
        "income": income,
        "categories": categories,
        "logs": [],
        "notify": False,
        "limits": {}
    }
    save_data(data)
    update.message.reply_text("✅ Настройки сохранены!")
    return ConversationHandler.END

def log(update, context):
    update.message.reply_text("Введите: доход/расход, категория, сумма\nПример: расход, еда, 5000")
    return LOG

def save_log(update, context):
    user_id = str(update.message.from_user.id)
    parts = update.message.text.split(",")
    if len(parts) != 3:
        update.message.reply_text("❌ Неверный формат.")
        return LOG
    entry_type, category, amount = [x.strip() for x in parts]
    amount = int(amount)

    data = load_data()
    if user_id not in data:
        update.message.reply_text("Сначала настройте с помощью /config")
        return ConversationHandler.END
    data[user_id]["logs"].append({
        "type": entry_type,
        "category": category,
        "amount": amount
    })
    save_data(data)

    if entry_type == "расход":
        spent = sum(l["amount"] for l in data[user_id]["logs"]
                    if l["type"] == "расход" and l["category"] == category)
        limit = data[user_id].get("limits", {}).get(category)
        if limit and spent > limit:
            update.message.reply_text(
                f"⚠️ Вы превысили лимит по '{category}': {spent}₸ (лимит: {limit}₸)")

    update.message.reply_text("✅ Запись добавлена.")
    return ConversationHandler.END

def summary(update, context):
    user_id = str(update.message.from_user.id)
    data = load_data()
    if user_id not in data:
        update.message.reply_text("Нет данных. Введите /config.")
        return
    total_income = data[user_id]["income"]
    expenses = sum(log["amount"] for log in data[user_id]["logs"] if log["type"] == "расход")
    balance = total_income - expenses
    update.message.reply_text(f"💰 Доход: {total_income}₸\n💸 Расходы: {expenses}₸\n📊 Баланс: {balance}₸")

def category_summary(update, context):
    user_id = str(update.message.from_user.id)
    data = load_data()
    if user_id not in data or not data[user_id]["logs"]:
        update.message.reply_text("Нет записей.")
        return
    summary = {}
    for log in data[user_id]["logs"]:
        if log["type"] == "расход":
            summary[log["category"]] = summary.get(log["category"], 0) + log["amount"]
    msg = "\n".join([f"🔹 {k}: {v}₸" for k, v in summary.items()])
    update.message.reply_text(f"📊 Расходы по категориям:\n{msg}")

def export_data(update, context):
    user_id = str(update.message.from_user.id)
    data = load_data()
    if user_id not in data or not data[user_id]["logs"]:
        update.message.reply_text("Нет данных для экспорта.")
        return
    df = pd.DataFrame(data[user_id]["logs"])
    filename = f"{user_id}_finance_export.xlsx"
    df.to_excel(filename, index=False)
    update.message.reply_document(open(filename, "rb"))

def set_limit(update, context):
    update.message.reply_text("Введите лимит: категория, сумма\nПример: транспорт, 10000")
    return LIMIT

def save_limit(update, context):
    user_id = str(update.message.from_user.id)
    parts = update.message.text.split(",")
    if len(parts) != 2:
        update.message.reply_text("Неверный формат.")
        return LIMIT
    category, limit = parts[0].strip(), int(parts[1])
    data = load_data()
    if "limits" not in data[user_id]:
        data[user_id]["limits"] = {}
    data[user_id]["limits"][category] = limit
    save_data(data)
    update.message.reply_text(f"✅ Лимит {limit}₸ установлен для '{category}'")
    return ConversationHandler.END

def notify_on(update, context):
    user_id = str(update.message.from_user.id)
    data = load_data()
    if user_id in data:
        data[user_id]["notify"] = True
        save_data(data)
        update.message.reply_text("🔔 Уведомления включены.")
    else:
        update.message.reply_text("Сначала настройте с помощью /config")

def notify_off(update, context):
    user_id = str(update.message.from_user.id)
    data = load_data()
    if user_id in data:
        data[user_id]["notify"] = False
        save_data(data)
        update.message.reply_text("🔕 Уведомления отключены.")

def send_notify(bot):
    data = load_data()
    for user_id, user_data in data.items():
        if user_data.get("notify"):
            income = user_data["income"]
            expenses = sum(log["amount"] for log in user_data["logs"] if log["type"] == "расход")
            balance = income - expenses
            bot.send_message(chat_id=int(user_id),
                             text=f"📢 Еженедельная сводка:\n💰 Доход: {income}₸\n💸 Расходы: {expenses}₸\n📊 Баланс: {balance}₸")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("summary", summary))
    dp.add_handler(CommandHandler("categorysummary", category_summary))
    dp.add_handler(CommandHandler("export", export_data))
    dp.add_handler(CommandHandler("notifyon", notify_on))
    dp.add_handler(CommandHandler("notifyoff", notify_off))
    dp.add_handler(CommandHandler("setlimit", set_limit))

    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler("config", config)],
        states={CONFIG: [MessageHandler(Filters.text & ~Filters.command, save_config)]},
        fallbacks=[]
    ))
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler("log", log)],
        states={LOG: [MessageHandler(Filters.text & ~Filters.command, save_log)]},
        fallbacks=[]
    ))
    dp.add_handler(ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('.*'), set_limit)],
        states={LIMIT: [MessageHandler(Filters.text & ~Filters.command, save_limit)]},
        fallbacks=[]
    ))

    scheduler = BackgroundScheduler(timezone=timezone("Asia/Almaty"))
    scheduler.add_job(lambda: send_notify(updater.bot), 'cron', day_of_week='sun', hour=10, minute=0)
    scheduler.add_job(lambda: send_notify(updater.bot), 'cron', hour=19, minute=32)
    scheduler.start()

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
