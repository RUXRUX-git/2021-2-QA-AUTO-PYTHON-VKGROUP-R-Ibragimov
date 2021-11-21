import json


def parse_log_line(line):
    command = line.split()
    return {
        "ip": command[0],
        "type": command[5][1:],
        "url": command[6],
        "status_code": int(command[8]),
        "size": 0 if command[9] == "-" else int(command[9])
    }


def get_top_requests_by_size(size_to_request, max_count):
    sorted_keys = sorted(size_to_request, reverse=True)
    selected_count = 0
    res = []
    for size in sorted_keys:
        if selected_count == max_count:
            break
        current_requests = size_to_request[size]
        selected_requests = []
        if len(current_requests) <= max_count - selected_count:
            selected_requests = current_requests
            selected_count += len(current_requests)
        else:
            selected_requests = current_requests[:max_count - selected_count]
            selected_count = max_count
        res.extend([request | {"size": size} for request in selected_requests])
    return res


def assembly_parsing_results(commands_count,
                             type_to_count,
                             most_common_urls,
                             largest_requests,
                             top_users):
    return {
        "commands_count": commands_count,
        "types_count": type_to_count,
        "top_requests": most_common_urls,
        "largest_requests_with_4xx_error": largest_requests,
        "top_users_by_requests_with_5xx_error": top_users
    }


def jsonify(data, file_name):
    json.dump(data, open(file_name, "w"), indent=4)


def stringify(data, file_name):
    with open(file_name, "w") as f:
        f.write(f"Общее количество запросов:\n{data['commands_count']}\n")
        f.write("-" * 40 + "\n")

        f.write("Общее количество запросов по типу:\n")
        for elem in data["types_count"]:
            f.write(f"Запрос: {elem['value']}, количество: {elem['count']}\n")
        f.write("-" * 40 + "\n")

        f.write("Топ 10 самых частых запросов:\n")
        for num, elem in enumerate(data["top_requests"], start=1):
            f.write(f"Топ-{num}:\n")
            f.write(f"url: [{elem['value']}]\n")
            f.write(f"Количество запросов: {elem['count']}\n")
        f.write("-" * 40 + "\n")

        f.write("Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой:\n")
        for num, elem in enumerate(data["largest_requests_with_4xx_error"], start=1):
            f.write(f"Топ-{num}:\n")
            f.write(f"url: [{elem['url']}]\n")
            f.write(f"Статус код: {elem['status_code']}\n")
            f.write(f"Размер запроса: {elem['size']}\n")
            f.write(f"ip адрес: {elem['ip']}\n")
        f.write("-" * 40 + "\n")

        f.write("Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой:\n")
        for num, elem in enumerate(data["top_users_by_requests_with_5xx_error"], start=1):
            f.write(f"Топ-{num}:\n")
            f.write(f"ip адрес: {elem['ip']}, количество запросов: {elem['count']}\n")
