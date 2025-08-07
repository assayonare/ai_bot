import requests
from bs4 import BeautifulSoup
import json
import re

# Функция для парсинга данных о программах с сайтов
def scrape_program_data():
    # Список URL для двух магистерских программ
    urls = {
        "ai": "https://abit.itmo.ru/program/master/ai",
        "ai_product": "https://abit.itmo.ru/program/master/ai_product"
    }
    programs_data = {}

    for program, url in urls.items():
        try:
            # Отправляем HTTP-запрос с пользовательским агентом
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Извлекаем описание программы
            description = ""
            desc_elements = soup.find_all("p")
            for elem in desc_elements:
                if "Создавайте AI-продукты и технологии" in elem.text:
                    description = elem.text.strip()
                    break

            # Извлекаем учебный план
            curriculum = []
            curriculum_section = soup.find("section", {"class": re.compile("curriculum|program")})
            if curriculum_section:
                courses = curriculum_section.find_all(["li", "p"])
                curriculum = [course.text.strip() for course in courses if course.text.strip()]

            # Сохраняем данные в словарь
            programs_data[program] = {
                "description": description,
                "curriculum": curriculum,
                "admission": "Вступительные экзамены проводятся онлайн, оцениваются по 100-балльной шкале. Подробности на abit.itmo.ru."
            }
        except Exception as e:
            programs_data[program] = {"error": f"Ошибка при парсинге: {str(e)}"}

    # Сохраняем данные в JSON-файл
    with open("programs_data.json", "w", encoding="utf-8") as f:
        json.dump(programs_data, f, ensure_ascii=False, indent=2)

    return programs_data

# Функция для загрузки данных программ
def load_program_data():
    try:
        # Пробуем загрузить данные из JSON
        with open("programs_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Если файл не существует, парсим данные заново
        return scrape_program_data()