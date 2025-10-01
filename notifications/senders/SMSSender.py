import smtplib
import smpplib
import requests
from email.mime.text import MIMEText
from ..config import SMSAERO_EMAIL, SMSAERO_API_KEY, SMTP_HOST, SMTP_PORT, SMTP_LOGIN, SMTP_PSWD


class SMSSender:
    def __init__(self):
        self.email = SMSAERO_EMAIL
        self.api_key = SMSAERO_API_KEY
        
    def send_via_api(self, phone, text, sign="SMS Aero"):
        try:
            url = "https://gate.smsaero.ru/v2/sms/send"
            auth = (self.email, self.api_key)
            data = {
                "number": phone,
                "text": text,
                "sign": sign
            }
            
            response = requests.post(url, auth=auth, json=data)
            response.raise_for_status()
            result = response.json()
            return result.get('success', False)
        except Exception as e:
            print(f"Ошибка API SMS: {e}")
            return False
    
    def send_via_smtp(self, phone, text):
        try:
            sms_email = f"{phone}@smsaero.ru"
            msg = MIMEText(text, 'plain', 'utf-8')
            msg['From'] = self.email
            msg['To'] = sms_email
            
            server = smtplib.SMTP('smtp.smsaero.ru', 2525)
            server.starttls()
            server.login(self.email, self.api_key)
            server.send_message(msg)
            server.quit()
            print("SMS отправлено через SMTP!")
            return True
        except Exception as e:
            print(f"Ошибка SMTP SMS: {e}")
            return False

    def send_via_smpp(self, phone, text):
        client = None
        try:
            client = smpplib.Client(
                host=SMTP_HOST,
                port=SMTP_PORT
            )

            client.connect()
            client.bind_transceiver(
                system_id=SMTP_LOGIN,
                password=SMTP_PSWD
            )

            client.send_message(
                source_addr_ton=smpplib.consts.SMPP_TON_INTL,
                source_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                source_addr='SMSAero',
                dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
                dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                destination_addr=phone[1:],
                short_message=text.encode('utf-16-be'),
                data_coding=0x08
            )

            print("SMS отправлено через SMPP!")
            return True

        except Exception as e:
            print(f"Ошибка SMPP: {e}")
            return False
        finally:
            client.unbind()
            client.disconnect()

    def send(self, phone, text):
        if self.send_via_api(phone, text):
            return True
        elif self.send_via_smtp(phone, text):
            return True
        elif self.send_via_smpp(phone, text):
            return True
        else:
            return False