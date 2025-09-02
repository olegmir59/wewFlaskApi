from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    quote = "Цитата не найдена"
    author = "Неизвестный автор"
    api_url = "https://zenquotes.io/api/random"
    try:
        # Запрос цитаты с выбранного API
        response = requests.get(api_url)
        response.raise_for_status()  # Проверка статуса ответа
        quote_data = response.json()

        # Извлечение цитаты и автора
        quote = quote_data[0]['q']
        author = quote_data[0]['a']
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        quote = "Ошибка при получении цитаты"
        author = "Неизвестный автор"
    return render_template('index.html', quote=quote, author=author, api_url=api_url)


if __name__ == '__main__':
    app.run(debug=True)