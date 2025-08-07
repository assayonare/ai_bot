# Главный файл для запуска Telegram-бота

from bot import init_bot

def main():
    # Запускаем бота
    print("Бот запущен...")
    init_bot()

if __name__ == "__main__":
    main()