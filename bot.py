from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from scraper import load_program_data
from recommender import recommend_courses

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте! Я чат-бот, который поможет вам выбрать между магистратурами ИТМО 'Искусственный интеллект' и 'Управление продуктами в ИИ'. "
        "Расскажите о вашем образовании и навыках (например, 'у меня степень по информатике, знаю Python')."
    )
    context.user_data["awaiting_background"] = True

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()
    program_data = load_program_data()

    # Проверяем, ожидается ли информация о бэкграунде
    if context.user_data.get("awaiting_background"):
        background = user_message
        context.user_data["background"] = background
        context.user_data["awaiting_background"] = False
        context.user_data["awaiting_goals"] = True
        await update.message.reply_text("Спасибо! Теперь расскажите о ваших карьерных целях (например, 'хочу стать специалистом по данным').")
        return

    # Проверяем, ожидается ли информация о целях
    if context.user_data.get("awaiting_goals"):
        goals = user_message
        context.user_data["goals"] = goals
        context.user_data["awaiting_goals"] = False
        recommendations = recommend_courses(context.user_data.get("background", ""), goals, program_data)
        await update.message.reply_text(
            f"На основе вашего бэкграунда и целей, вот мои рекомендации:\n" + "\n".join(recommendations) +
            "\n\nЗадавайте вопросы о программах или учебных планах!"
        )
        return

    # Обрабатываем вопросы, связанные с программами
    if any(keyword in user_message for keyword in ["искусственный интеллект", "ии", "управление продуктами", "учебный план", "курсы", "поступление"]):
        if "искусственный интеллект" in user_message or "ии" in user_message:
            ai_data = program_data.get("ai", {})
            await update.message.reply_text(
                f"**Программа 'Искусственный интеллект'**:\nОписание: {ai_data.get('description', 'Н/Д')}\n"
                f"Учебный план: {', '.join(ai_data.get('curriculum', ['Н/Д']))}\n"
                f"Поступление: {ai_data.get('admission', 'Н/Д')}"
            )
        elif "управление продуктами" in user_message:
            ai_product_data = program_data.get("ai_product", {})
            await update.message.reply_text(
                f"**Программа 'Управление продуктами в ИИ'**:\nОписание: {ai_product_data.get('description', 'Н/Д')}\n"
                f"Учебный план: {', '.join(ai_product_data.get('curriculum', ['Н/Д']))}\n"
                f"Поступление: {ai_product_data.get('admission', 'Н/Д')}"
            )
        elif "учебный план" in user_message or "курсы" in user_message:
            ai_data = program_data.get("ai", {})
            ai_product_data = program_data.get("ai_product", {})
            await update.message.reply_text(
                f"**Учебный план программы ИИ**: {', '.join(ai_data.get('curriculum', ['Н/Д']))}\n"
                f"**Учебный план программы 'Управление продуктами в ИИ'**: {', '.join(ai_product_data.get('curriculum', ['Н/Д']))}"
            )
        elif "поступление" in user_message:
            ai_data = program_data.get("ai", {})
            ai_product_data = program_data.get("ai_product", {})
            await update.message.reply_text(
                f"**Поступление**:\nПрограмма ИИ: {ai_data.get('admission', 'Н/Д')}\n"
                f"Управление продуктами в ИИ: {ai_product_data.get('admission', 'Н/Д')}"
            )
    else:
        await update.message.reply_text(
            "Пожалуйста, задавайте вопросы, связанные с программами 'Искусственный интеллект' или 'Управление продуктами в ИИ', их учебными планами или поступлением."
        )

# Функция для инициализации и запуска бота
def init_bot():
    # Токен Telegram-бота
    TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # Замените на ваш токен
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    application.run_polling()