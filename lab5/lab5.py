import requests
import json
from datetime import datetime


def write_response_details(file, server_response):
    """
    Записывает детали ответа сервера в файл
    """
    file.write("\n" + "-" * 100 + "\n")
    file.write("Детали ответа сервера\n")
    file.write("-" * 100 + "\n")
    file.write(f"Код состояния: {server_response.status_code}\n")

    # Запись заголовков ответа
    file.write("\nЗаголовки:\n")
    for header_name, header_value in server_response.headers.items():
        file.write(f"{header_name}: {header_value}\n")

    # Попытка записать тело ответа в формате JSON или как текст
    file.write("\nТело ответа:\n")
    try:
        file.write(json.dumps(server_response.json(), indent=2, ensure_ascii=False) + "\n")
    except ValueError:
        file.write(server_response.text + "\n")


def send_options_request(file, target_url):
    """
    Отправляет OPTIONS запрос и записывает результат в файл
    """
    file.write(f"\n[{datetime.now()}] Отправка OPTIONS запроса к: {target_url}\n")
    try:
        response = requests.options(target_url)
        write_response_details(file, response)
    except requests.exceptions.RequestException as e:
        file.write(f"Ошибка при отправке OPTIONS запроса: {e}\n")


def send_get_request(file, target_url, query_params=None):
    """
    Отправляет GET запрос и записывает результат в файл
    """
    file.write(f"\n[{datetime.now()}] Отправка GET запроса к: {target_url}\n")
    if query_params:
        file.write(f"\nПараметры запроса: {query_params}\n")

    try:
        response = requests.get(target_url, params=query_params)
        write_response_details(file, response)
        return response
    except requests.exceptions.RequestException as e:
        file.write(f"Ошибка при отправке GET запроса: {e}\n")
        return None


def send_post_request(file, target_url, form_data=None, json_data=None):
    """
    Отправляет POST запрос и записывает результат в файл
    """
    file.write(f"\n[{datetime.now()}] Отправка POST запроса к: {target_url}\n")

    if form_data:
        file.write(f"\nДанные формы: {form_data}\n")
    if json_data:
        file.write(f"\nJSON данные:\n{json.dumps(json_data, indent=2, ensure_ascii=False)}\n")

    try:
        response = requests.post(target_url, data=form_data, json=json_data)
        write_response_details(file, response)
        return response
    except requests.exceptions.RequestException as e:
        file.write(f"Ошибка при отправке POST запроса: {e}\n")
        return None


# Базовый URL тестового сервера
base_api_url = "https://httpbin.org"

# Открываем файл для записи (режим 'w' - перезапись)
with open('http_responses.log', 'w', encoding='utf-8') as log_file:
    # Записываем заголовок лога
    log_file.write(f"Лог HTTP-запросов\nДата начала: {datetime.now()}\n\n")

    # 1. Отправка OPTIONS запроса
    send_options_request(log_file, f"{base_api_url}/get")

    # 2. Отправка простого GET запроса
    send_get_request(log_file, f"{base_api_url}/get")

    # 3. Отправка GET запроса с параметрами
    send_get_request(
        log_file,
        f"{base_api_url}/get",
        query_params={"параметр1": "значение1", "параметр2": "значение2"}
    )

    # 4. Отправка POST запроса с данными формы
    send_post_request(log_file, f"{base_api_url}/post", form_data={"логин": "админ", "пароль": "секрет123"})

    # 5. Отправка POST запроса с JSON данными
    send_post_request(log_file, f"{base_api_url}/post", json_data={
        "title": "Test",
        "body": "Hello World",
        "user": 1
    })

    log_file.write("\nЛогирование завершено\n")
