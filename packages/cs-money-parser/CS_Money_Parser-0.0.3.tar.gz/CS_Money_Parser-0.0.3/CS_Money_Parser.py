import requests
import json


class parser:

    def __init__(self):

        self.url = {
            "csmoney": "https://inventories.cs.money/5.0/load_bots_inventory/730"
        }
        self.params = {
            "CSM": "?buyBonus=40&isStore=true&limit=60&maxPrice=10000&minPrice=1&withStack=true&offset=",
        }
        self.session = requests.Session()
        self.session.headers = {
            "Info": "I'm a bot please don't ban me))",
            "accept": "*/*",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
        }

        self.items = []

    def csmoney(self, maxPrice=10000, minPrice=1, name=None):
        """
        :param maxPrice: Maximum item price, in dollars $. Type INT
        :param minPrice: Minimum item price, in dollars $. Type INT
        :param name: Item name. Type STR
        :return: Returns items as a dictionary. Type LIST
        """
        offset = 0
        while True:
            r = self.session.get(self.url["csmoney"], params={
                "buyBonus": 40,
                "isStore": "true",
                "limit": 60,
                "maxPrice": maxPrice,
                "minPrice": minPrice,
                "withStack": "true",
                "offset": offset,
                "name": name
            }).json()
            try:
                for i in r['items']:
                    self.items.append(i)

                offset += 60
                write_file = open("cs.json", "w")
                write_file.write(json.dumps(self.items))
                write_file.close()
                print(f'Предметов в словарь: {str(len(self.items))}')
            except:
                print("Все предметы в словаре")
                break