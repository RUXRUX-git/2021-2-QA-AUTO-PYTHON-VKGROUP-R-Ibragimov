EMAIL = "ruxrux2002@yandex.ru"
PASSWORD = "44f3ee14-7ba6-4177-bec8-48136ab010f0"


class URLS:
    BASE = "https://target.my.com/"

    ADS_TARGET = "http://example.com/"

    LOGIN = "https://auth-ac.my.com/auth"
    LOGIN_CONTINUE = r"https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email"
    LOGIN_FAILURE = "https://account.my.com/login/"
    CSRF = "csrf/"

    LOAD_FILE = "api/v2/content/static.json"

    URLS = "api/v1/urls/"

    SEGMENTS = "api/v2/remarketing/segments.json"
    SPECIFIC_SEGMENT_TEMPLATE = "api/v2/remarketing/segments/{}.json"

    CAMPAIGNS = "api/v2/campaigns.json"
    SPECIFIC_CAMPAIGN_TEMPLATE = "api/v2/campaigns/{}.json"

    MASS_ACTION = "api/v2/campaigns/mass_action.json"
