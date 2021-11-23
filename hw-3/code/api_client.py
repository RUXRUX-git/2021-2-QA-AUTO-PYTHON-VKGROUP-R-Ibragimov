import requests
from urllib.parse import urljoin

import utils
from constants import URLS, EMAIL, PASSWORD


class SegmentNotFoundException(Exception):
    pass


class UnexpectedStatusCodeException(Exception):
    pass


class ApiClient:
    def __init__(self, base_url, email, password):
        self.base_url = base_url
        self.email = email
        self.password = password

        self.session = requests.Session()
        self._csrf_token = None

    def _request(self, method, url,
                 add_base=True, expected_status=200, **kwargs):
        full_url = urljoin(self.base_url, url) if add_base else url
        resp = self.session.request(method, full_url, **kwargs)

        if resp.status_code != expected_status:
            raise UnexpectedStatusCodeException(f"Expected status {expected_status}, got {resp.status_code}.\n"
                                                f"Request url is '{full_url}'.")
        return resp

    def _get(self, url, add_base=True, expected_status=200, **kwargs):
        return self._request("GET", url, add_base=add_base,
                             expected_status=expected_status, **kwargs)

    def _post(self, url, add_base=True, expected_status=200, **kwargs):
        return self._request("POST", url, add_base=add_base,
                             expected_status=expected_status, **kwargs)

    def _delete(self, url, add_base=True, expected_status=200, **kwargs):
        return self._request("DELETE", url, add_base=add_base,
                             expected_status=expected_status, **kwargs)

    @property
    def _cookies(self):
        return self.session.cookies

    def get_csrf(self):
        if self._csrf_token is None:
            self._get(URLS.CSRF)
            self._csrf_token = self._cookies['csrftoken']

        return self._csrf_token

    @property
    def default_headers(self):
        return {"X-CSRFToken": self.get_csrf()}

    def post_login(self):
        headers = {
            "Referer": URLS.LOGIN
        }
        data = {
            "email": EMAIL,
            "password": PASSWORD,
            "continue": URLS.LOGIN_CONTINUE,
            "failure": URLS.LOGIN_FAILURE
        }

        return self._post(URLS.LOGIN, add_base=False, headers=headers, data=data, allow_redirects=True)

    def post_load_image(self, image_path):
        with open(image_path, "rb") as f:
            files = {"file": f}
            resp = self._post(URLS.LOAD_FILE,
                              headers=self.default_headers, files=files)
            return resp.json()["id"]

    def get_banner_id(self, link):
        params = {"url": link}
        resp = self._get(URLS.URLS, headers=self.default_headers, params=params)
        return resp.json()["id"]

    def post_create_segment(self, name):
        json_data = {
            "name": name,
            "pass_condition": 1,
            "relations": [{
                "object_type": "remarketing_player",
                "params": {
                    "type": "positive",
                    "left": 365,
                    "right": 0
                }
            }],
            "logicType": "or"
        }

        resp = self._post(URLS.SEGMENTS,
                          headers=self.default_headers, json=json_data, allow_redirects=True)
        return resp.json()["id"]

    def get_segment(self, id, expected_status=200):
        # Идея была такой - хотелось добавить дополнительный вывод в консоль при падении.
        # При этом рейзить новое исключение, отлавливая UnexpectedStatusCodeException, не хочется,
        # потому что потеряем лог. Нагуглил примерно такое решение:
        url = URLS.SPECIFIC_SEGMENT_TEMPLATE.format(id)
        try:
            res = self._get(url, headers=self.default_headers, expected_status=expected_status).json()
            return res
        except UnexpectedStatusCodeException as e:
            raise SegmentNotFoundException(f"Can't find segment with id {id}") from e

    def delete_segment(self, id, expected_status=204):
        return self._delete(URLS.SPECIFIC_SEGMENT_TEMPLATE.format(id),
                            headers=self.default_headers, expected_status=expected_status)

    def post_create_campaign(self, name, link, tmpdir):
        json_data = {
            "package_id": 960,
            "objective": "traffic",
            "name": name,
            "banners": [{
                "urls": {
                    "primary": {
                        "id": self.get_banner_id(link)
                    }
                },
                "textblocks": {},
                "content": {
                    "image_240x400": {
                        "id": self.post_load_image(utils.create_random_image(tmpdir, 240, 400))
                    }
                },
            }]
        }

        resp = self._post(URLS.CAMPAIGNS, headers=self.default_headers, json=json_data)
        return resp.json()["id"]

    def get_campaign(self, id):
        return self._get(URLS.SPECIFIC_CAMPAIGN_TEMPLATE.format(id), headers=self.default_headers).json()

    def delete_campaign(self, id, expected_status=204):
        json_data = [
            {
                "id": id,
                "status": "deleted"
            }
        ]

        return self._post(URLS.MASS_ACTION,
                          headers=self.default_headers, json=json_data, expected_status=expected_status)
