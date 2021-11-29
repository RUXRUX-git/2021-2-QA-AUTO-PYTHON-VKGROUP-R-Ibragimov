import socket

import os.path

from config import MOCK_HOST, MOCK_PORT, DEFAULT_HTTP_VERSION, \
    LOG_DIR, REQUESTS_HANDLER_FILE_PATH


class UnexpectedRequestMethodException(Exception):
    pass


class SocketClient:

    def __init__(self, host=MOCK_HOST, port=MOCK_PORT):
        self.host = host
        self.port = port

        if not os.path.isdir(LOG_DIR):
            os.makedirs(LOG_DIR)
        self.log_file = REQUESTS_HANDLER_FILE_PATH

    def _set_client(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(0.1)
        client.connect((self.host, self.port))
        return client

    def get_response(self, client: socket.socket, jsonify=False):
        all_data = []

        while True:
            data = client.recv(4096)
            if data:
                all_data.append(data.decode())
            else:
                break

        res = ''.join(all_data)
        res_json = self._jsonify_response(res)

        with open(self.log_file, 'a') as f:
            f.write(' '.join([res_json['protocol'], res_json['status_code'], res_json['result']]))
            f.write('\n')
            f.write('Headers:\n')
            f.write(res_json['head'].split('\n', 1)[-1])
            f.write('\n')
            f.write('Data:\n')
            f.write(res_json['data'])
            f.write('\n\n')

        if jsonify:
            return res_json
        else:
            return res

    @staticmethod
    def _jsonify_response(resp: str):
        head, data = resp.split('\r\n\r\n')
        protocol, status_code, result = head.split('\r\n', 1)[0].split(' ', 2)

        return {
            'protocol': protocol,
            'status_code': status_code,
            'result': result,
            'head': head,
            'data': data
        }

    # Изначально хотел передавать заголовки как kwargs, но испугался того,
    # что будет TypeError, если мы передадим заголовок с таким же именем, как один из аргументов функции
    @staticmethod
    def _form_http_head(method, url, protocol, headers: dict):
        res = ' '.join([method, url, protocol]) + '\r\n'
        # Формируем заголовки
        res += '\r\n'.join([': '.join([key, str(value)]) for key, value in headers.items()])
        res += '\r\n\r\n'
        return res

    def _request(self, client: socket.socket, head: str, data=None, jsonify_response=False):
        full_request = head
        if data is not None:
            full_request += data

        client.send(full_request.encode())

        return self.get_response(client, jsonify=jsonify_response)

    @property
    def default_headers(self):
        return {
            'Host': self.host,
            'Connection': 'close'
        }

    def get(self, url, protocol=DEFAULT_HTTP_VERSION, jsonify_response=False):
        client = self._set_client()
        head = self._form_http_head('GET', url, protocol=protocol, headers=self.default_headers)

        return self._request(client, head=head, jsonify_response=jsonify_response)

    # Попытка избавиться от дублирования кода
    def _request_with_body(self, url, method, protocol=DEFAULT_HTTP_VERSION, data='',
                           jsonify_response=False, content_type='application/json'):
        methods_list = ['POST', 'PUT', 'DELETE']

        if method not in methods_list:
            possible_methods = ' or '.join([f"'{elem}'" for elem in methods_list])
            raise UnexpectedRequestMethodException(f"Expected {possible_methods}, got '{method}'")

        client = self._set_client()
        headers = self.default_headers | {
            'Content-Type': content_type,
            'Content-Length': len(data)
        }
        head = self._form_http_head(method, url, protocol=protocol, headers=headers)

        return self._request(client, head=head, data=data, jsonify_response=jsonify_response)

    def post(self, url, protocol=DEFAULT_HTTP_VERSION, data='',
             jsonify_response=False, content_type='application/json'):
        return self._request_with_body(url, 'POST', protocol=protocol, data=data,
                                       jsonify_response=jsonify_response, content_type=content_type)

    def put(self, url, protocol=DEFAULT_HTTP_VERSION, data='',
            jsonify_response=False, content_type='application/json'):
        return self._request_with_body(url, 'PUT', protocol=protocol, data=data,
                                       jsonify_response=jsonify_response, content_type=content_type)

    def delete(self, url, protocol=DEFAULT_HTTP_VERSION, data='',
               jsonify_response=False, content_type='application/json'):
        return self._request_with_body(url, 'DELETE', protocol=protocol, data=data,
                                       jsonify_response=jsonify_response, content_type=content_type)
