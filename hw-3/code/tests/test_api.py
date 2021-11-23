import pytest

from constants import URLS
from base import TestBase


class TestApi(TestBase):
    @pytest.mark.API
    def test_create_segment(self, api_client, random_name):
        id = api_client.post_create_segment(random_name)
        resp = api_client.get_segment(id)
        assert resp["name"] == random_name
        api_client.delete_segment(id)

    @pytest.mark.API
    def test_delete_segment(self, api_client, random_name):
        id = api_client.post_create_segment(random_name)
        api_client.delete_segment(id)
        api_client.get_segment(id, expected_status=404)

    @pytest.mark.API
    def test_create_campaign(self, api_client, tmpdir, random_name, link=URLS.ADS_TARGET):
        id = api_client.post_create_campaign(random_name, link, tmpdir)
        resp = api_client.get_campaign(id)
        assert resp["name"] == random_name
        api_client.delete_campaign(id)
