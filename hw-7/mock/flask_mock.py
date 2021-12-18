"""
    Ужасно неудобно перенаправлять весь вывод flask (в том числе сообщения при запуске и выводе
    предупреждения - судя по коду библиотеки для вывода баннера используется click.echo, а не
    сконфигурированный логгер). Впринципе, эта информация не сильно полезная, поэтому было принято
    'волевое' решение редиректить то, что редиректится))
    При желании, вывод баннера сервера можно было убрать:
        cli = sys.modules['flask.cli']
        cli.show_server_banner = lambda *x: None
    Ворнинг убрал в conftest.pytest_unconfigure
"""

import json
import logging
import os
import threading
from flask import Flask, jsonify, request
from werkzeug.serving import WSGIRequestHandler

import utils
from config import MOCK_LOG_FILE_PATH, MOCK_HOST, MOCK_PORT, LOG_DIR

if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR)

# Задаем файл для логов, определяем приложение
logging.basicConfig(filename=MOCK_LOG_FILE_PATH)
app = Flask(__name__)

SURNAME_DATA = {}


@app.route('/get_surname/<name>', methods=['GET'])
def get_user_surname(name):
    if surname := SURNAME_DATA.get(name):
        return jsonify(surname), 200
    else:
        return jsonify(f'Surname for user "{name}" not found'), 404


# Ммм, декораторы
def check_arguments(*names):
    """
        Декоратор принимает список имен, последовательно проверяет, что все они переданы
        (если какой-то не передан, то возвращает сообщение об ошибке и 400 код).
        Далее декоратор передает полученный (и проверенный) список имен в декорируемую функцию,
        и возвращает ее результат
    """

    def decorator(func):
        def wrapper():
            values = []
            for name in names:
                if (value := json.loads(request.data).get(name)) is None:
                    return jsonify(f'Can\'t find \'{name}\' in request'), 400
                else:
                    values.append(value)
            return func(*values)

        # Переименовываем wrapper - если этого не сделать, то уже на втором вызове декоратора
        # получим ошибку View function mapping is overwriting an existing endpoint function: wrapper
        wrapper.__name__ = func.__name__
        return wrapper

    return decorator


@app.route('/create', methods=['POST'])
@check_arguments('name', 'surname')
def create_user(name, surname):
    if name in SURNAME_DATA:
        return jsonify(f'User "{name}" already exists'), 400

    SURNAME_DATA[name] = surname
    return jsonify({'name': name, 'surname': surname}), 201


@app.route('/update', methods=['PUT'])
@check_arguments('name', 'surname')
def update_user(name, surname):
    exists = SURNAME_DATA.get(name) is not None
    SURNAME_DATA[name] = surname

    # Прочитал, что правильно возвращать 201, если объекта не было, и 200, если был - поэтому добавил условие
    return jsonify({'name': name, 'surname': surname}), (200 if exists else 201)


@app.route('/delete', methods=['DELETE'])
@check_arguments('name')
def delete_user(name):
    if SURNAME_DATA.get(name) is None:
        return jsonify(f'User "{name}" doesn\'t exist'), 404
    else:
        return jsonify(f'User "{name}" deleted', 200)


@app.route('/shutdown', methods=['GET'])
def shutdown():
    if terminate_func := request.environ.get('werkzeug.server.shutdown'):
        terminate_func()
    return jsonify(f'Ok, exiting'), 200


def run_mock(host=MOCK_HOST, port=MOCK_PORT):
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    server = threading.Thread(target=app.run, kwargs={
        'host': host,
        'port': port
    })

    server.start()

    utils.wait_ready(host, port)

    return server
