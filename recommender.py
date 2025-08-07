import requests

# Функция для запроса рекомендаций через API текстовой модели
def get_api_recommendations(background, goals, program_data):
    # Формируем промпт для API
    ai_curriculum = ", ".join(program_data.get("ai", {}).get("curriculum", ["Н/Д"]))
    ai_product_curriculum = ", ".join(program_data.get("ai_product", {}).get("curriculum", ["Н/Д"]))
    prompt = (
        f"Абитуриент с бэкграундом: '{background}' и карьерными целями: '{goals}'. "
        f"Рекомендуйте подходящие выборные дисциплины из двух магистерских программ ИТМО. "
        f"Программа 'Искусственный интеллект' включает курсы: {ai_curriculum}. "
        f"Программа 'Управление продуктами в ИИ' включает курсы: {ai_product_curriculum}. "
        f"Ответ должен быть кратким, содержать 2-3 рекомендации с указанием программы и быть на русском языке."
    )

    # Настройки для API (используем Grok API от xAI)
    api_key = "YOUR_XAI_API_KEY"  # Замените на ваш API-ключ
    api_url = "https://api.x.ai/v1/grok"  # URL API (замените на актуальный)

    try:
        # Отправляем запрос к API
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"prompt": prompt, "max_tokens": 150}
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        api_response = response.json()

        # Извлекаем рекомендации из ответа API
        recommendations = api_response.get("choices", [{}])[0].get("text", "").strip().split("\n")
        return [rec for rec in recommendations if rec.strip()] or ["API не вернул рекомендаций."]
    except Exception as e:
        # Резервная логика на случай ошибки API
        return fallback_recommendations(background, goals, program_data)

# Резервная функция рекомендаций (на основе ключевых слов)
def fallback_recommendations(background, goals, program_data):
    recommendations = []
    ai_curriculum = program_data.get("ai", {}).get("curriculum", [])
    ai_product_curriculum = program_data.get("ai_product", {}).get("curriculum", [])

    # Простая логика рекомендаций
    if "программирование" in background.lower() or "информатика" in background.lower():
        recommendations.append("Рекомендуем технические курсы, такие как 'Продвинутое машинное обучение (Python)' или 'Технологии хранения больших данных' из программы ИИ.")
    if "бизнес" in background.lower() or "менеджмент" in background.lower():
        recommendations.append("Рассмотрите курсы, связанные с управлением продуктами, из программы 'Управление продуктами в ИИ', например, управление проектами или разработка продуктов.")
    if "анализ данных" in goals.lower() or "data science" in goals.lower():
        recommendations.append("Курсы 'Введение в машинное обучение (Python)' и 'Автоматическая обработка текстов' из программы ИИ будут очень полезны.")
    if not recommendations:
        recommendations.append("На основе ваших данных, рекомендуем начать с курса 'Введение в машинное обучение' и дисциплин по управлению продуктами.")

    return recommendations

# Основная функция рекомендаций
def recommend_courses(background, goals, program_data):
    return get_api_recommendations(background, goals, program_data)