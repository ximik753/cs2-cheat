import requests


class OffsetManager:
    def __init__(self):
        print('[-] Fetching offset...')
        self.offsets = requests.get(
            'https://raw.githubusercontent.com/a2x/cs2-dumper/main/generated/offsets.json').json()
        self.clientdll = requests.get(
            'https://raw.githubusercontent.com/a2x/cs2-dumper/main/generated/client.dll.json').json()

    def offset(self, a):
        try:
            return self.offsets['client_dll']['data'][a]['value']
        except:
            print(f'Offset {a} not found.')
            exit()

    def get(self, a, b):
        try:
            return self.clientdll[a]['data'][b]['value']
        except:
            print(f'Unable to get {a}, {b}.')
            exit()
