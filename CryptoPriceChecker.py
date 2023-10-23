import cryptocompare
import requests
import PySimpleGUI as sg

API_KEY = 'YOUR_API_KEY'  # Replace with your actual API key

# Initialize the API key
cryptocompare.cryptocompare._set_api_key_parameter(API_KEY)

class CryptoPrice:
    def __init__(self):
        self.api_key = None
        self.selected_cryptos = []

    def get_api_key(self):
        layout = [
            [sg.Text("Please enter your API key below:", size=(40, 1))],
            [sg.InputText(key="api_key")],
            [sg.Button("Next")]
        ]
        self.window = sg.Window("CryptoPrice", layout=layout, finalize=True)

        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "Cancel"):
                break
            elif event == "Next":
                self.api_key = values["api_key"]
                self.window.close()
                self.select_currencies()

    def select_currencies(self):
        crypto_choices = ["BTC", "ETH", "LTC", "XRP", "BCH", "Loom", "ORBS", "META", "BOND", "USDT", "XRP", "TRB", "USDC"]
        layout = [
            [sg.Text("Please select your preferred currencies from below:")],
            [sg.Listbox(crypto_choices, size=(20, 10), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, key='cryptos')],
            [sg.Button("Next")]
        ]
        self.window = sg.Window("CryptoPrice", layout=layout, finalize=True)

        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "Cancel"):
                break
            if event == 'Next':
                self.selected_cryptos = values['cryptos']
                self.window.close()
                self.display_prices()

    def display_prices(self):
        layout = [
            [sg.Text("Cryptocurrency Prices:")],
            [sg.Multiline(size=(50, 10), key="price_display", disabled=True)],
            [sg.Button("Cancel")]
        ]
        self.window = sg.Window("CryptoPrice", layout=layout, finalize=True)
        self.get_prices()

    def get_prices(self):
        while True:
            try:
                prices = {}
                for crypto in self.selected_cryptos:
                    response = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={crypto}&tsyms=USD&api_key={self.api_key}")
                    data = response.json()
                    price = data.get("USD", "N/A")
                    prices[crypto] = price
                self.window['price_display'].update('\n'.join([f'{crypto}: ${price}' for crypto, price in prices.items()]))
            except Exception as e:
                sg.popup_error(f"Error: {e}")
            event, values = self.window.read(timeout=5000)
            if event in (sg.WIN_CLOSED, "Cancel"):
                break
        self.window.close()

if __name__ == '__main__':
    app = CryptoPrice()
    app.get_api_key()
