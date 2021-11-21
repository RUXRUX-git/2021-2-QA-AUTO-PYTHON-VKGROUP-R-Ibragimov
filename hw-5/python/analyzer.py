import argparse
from collections import Counter

import utils

LOG_FILE = "access.log"
TEXT_RES_FILE = "res.txt"
JSON_RES_FILE = "res.json"

TOP_MOST_COMMON_REQUESTS_NUMBER = 10
TOP_LARGEST_REQUESTS_NUMBER = 5
TOP_USERS_BY_REQUESTS_NUMBER = 5

commands_count = 0
type_to_count = Counter()
url_to_count = Counter()
size_to_request = {}
ip_to_count = Counter()

f = open("access.log", "r")
for line in f:
    parsed = utils.parse_log_line(line)

    commands_count += 1

    type_to_count[parsed["type"]] += 1

    url_to_count[parsed["url"]] += 1

    if 400 <= parsed["status_code"] < 500:
        command_info = {key: parsed[key] for key in parsed if key in {"url", "status_code", "ip"}}
        size_to_request.setdefault(parsed["size"], []).append(command_info)
    elif 500 <= parsed["status_code"] < 600:
        ip_to_count[parsed["ip"]] += 1

res = utils.assembly_parsing_results(commands_count,
                                     [{"value": elem[0], "count": elem[1]} for elem in type_to_count.most_common()],
                                     [{"value": elem[0], "count": elem[1]} for elem in
                                         url_to_count.most_common(TOP_MOST_COMMON_REQUESTS_NUMBER)],
                                     utils.get_top_requests_by_size(size_to_request, TOP_LARGEST_REQUESTS_NUMBER),
                                     [{"ip": elem[0], "count": elem[1]} for elem in
                                         ip_to_count.most_common(TOP_USERS_BY_REQUESTS_NUMBER)])

parser = argparse.ArgumentParser()
parser.add_argument("--json", action="store_true")
start_arguments = parser.parse_args()
if start_arguments.json:
    utils.jsonify(res, JSON_RES_FILE)
else:
    utils.stringify(res, TEXT_RES_FILE)
