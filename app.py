from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

# Список доступных API для цитат
quote_apis = [
    "https://zenquotes.io/api/random",
    "https://api-ninjas.com/api/quotes",
    "https://quoteslate.vercel.app/api/quotes/random"
]


@app.route('/', methods=['GET', 'POST'])
def index():
    quote = "Цитата не найдена"
    author = "Неизвестный автор"
    api_url = ""  # Добавляем переменную для хранения URL API

    try:
        # Случайный выбор API для цитат
        api_url = random.choice(quote_apis)  # Сохраняем выбранный URL

        # Запрос цитаты с выбранного API
        response = requests.get(api_url)
        response.raise_for_status()  # Проверка статуса ответа
        quote_data = response.json()

        # Извлечение цитаты и автора
        if api_url == "https://zenquotes.io/api/random":
            quote = quote_data[0]['q']
            author = quote_data[0]['a']
        elif api_url == "https://api-ninjas.com/api/quotes":
            if isinstance(quote_data, list) and len(quote_data) > 0:
                quote = quote_data[0]['quote']
                author = quote_data[0]['author']
            else:
                quote = "Ошибка при получении цитаты"
                author = "Неизвестный автор"
        elif api_url == "https://quoteslate.vercel.app/api/quotes/random":
            if isinstance(quote_data, dict) and 'quote' in quote_data and 'author' in quote_data:
                quote = quote_data['quote']
                author = quote_data['author']
            else:
                quote = "Ошибка при получении цитаты"
                author = "Неизвестный автор"

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        quote = "Ошибка при получении цитаты"
        author = "Неизвестный автор"

    return render_template('index.html', quote=quote, author=author, api_url=api_url)


if __name__ == '__main__':
    app.run(debug=True)