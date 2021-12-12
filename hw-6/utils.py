from collections import Counter

from constants import TOP_MOST_COMMON_REQUESTS_NUMBER, \
    TOP_LARGEST_REQUESTS_NUMBER, \
    TOP_USERS_BY_REQUESTS_NUMBER


def parse_log_line(line):
    command = line.split()
    return {
        "ip": command[0],
        "type": command[5][1:],
        "url": command[6],
        "status_code": int(command[8]),
        "size": 0 if command[9] == "-" else int(command[9])
    }


def count_requests(file_name):
    with open(file_name, "r") as f:
        return len(f.readlines())


def type_to_count(file_name):
    with open(file_name, "r") as f:
        _type_to_count = Counter()
        for line in f:
            parsed = parse_log_line(line)
            if len(parsed["type"]) <= 100:
                _type_to_count[parsed["type"]] += 1

        return [{"value": elem[0], "count": elem[1]} for elem in _type_to_count.most_common()]


def url_to_count(file_name):
    with open(file_name, "r") as f:
        _url_to_count = Counter()
        for line in f:
            parsed = parse_log_line(line)
            _url_to_count[parsed["url"]] += 1

        return [{"value": elem[0], "count": elem[1]} for elem in
                _url_to_count.most_common(TOP_MOST_COMMON_REQUESTS_NUMBER)]


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


def size_to_4xx_response(file_name):
    with open(file_name, "r") as f:
        _size_to_4xx_response = {}
        for line in f:
            parsed = parse_log_line(line)
            if 400 <= parsed["status_code"] < 500:
                command_info = {key: parsed[key] for key in parsed if key in {"url", "status_code", "ip"}}
                _size_to_4xx_response.setdefault(parsed["size"], []).append(command_info)

        return get_top_requests_by_size(_size_to_4xx_response, TOP_LARGEST_REQUESTS_NUMBER)


def ip_with_5xx_response_to_count(file_name):
    with open(file_name, "r") as f:
        _ip_with_5xx_response_to_count = Counter()
        for line in f:
            parsed = parse_log_line(line)
            if 500 <= parsed["status_code"] < 600:
                _ip_with_5xx_response_to_count[parsed["ip"]] += 1

        return [{"ip": elem[0], "count": elem[1]} for elem in
                _ip_with_5xx_response_to_count.most_common(TOP_USERS_BY_REQUESTS_NUMBER)]

print()