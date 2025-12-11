import unittest

from modules.real_estate.infrastructure.api.zigbang_api_client import ZigbangApiClient


class MyTestCase(unittest.TestCase):

    def test_fetch_details(self):
        client = ZigbangApiClient()
        resp = client.fetch_detail(46000239)
        print(resp)

    def test_fetch_items(self):
        client = ZigbangApiClient()
        id_list = [
            47000000,
            47000001,
        ]
        resp = client.fetch_by_item_ids(id_list)
        print(resp)

if __name__ == '__main__':
    unittest.main()
