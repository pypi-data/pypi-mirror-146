import hashlib
import base64
import hashlib
import string

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad,pad
from PaymentDTO.MessageLayer import MessageLayer
from PaymentDTO.CapturePayment import CapturePayment
from PaymentDTO.Payment import Payment
from PaymentDTO.PaymentResponse import PaymentResponse
from PaymentDTO.Product import Product
from PaymentDTO.RefundPayment import RefundPayment
from PaymentDTO.VoidPayment import VoidPayment
import requests
import json

class OnlinePayment:

    def authorizePayment(apiKey:string, apiSecret:string,messageLayer = MessageLayer()):

        header = {"X-API-KEY": apiKey,"X-API-SECRET":apiSecret,"Content-Type": "application/json"} 
        
        enc = _encrypting(messageLayer.account,apiSecret,apiKey)
        messageLayer.account=enc

        enc = _encrypting(messageLayer.cvv2,apiSecret,apiKey)
        messageLayer.cvv2=enc

        
        jsonString = json.dumps(messageLayer.__dict__)
        jsonString = jsonString.replace("_MessageLayer__","")

        response = requests.post("http://164.90.146.112:8062/payments/authorize",data=jsonString,headers=header)

        return response;

    def capturePayment(apiKey:string, apiSecret:string,capturePayment = CapturePayment()):
    
        header = {"X-API-KEY": apiKey,"X-API-SECRET":apiSecret,"Content-Type": "application/json"}

        jsonString = json.dumps(capturePayment.__dict__)
        jsonString = jsonString.replace("_CapturePayment__","")

        response = requests.post("http://164.90.146.112:8062/payments/capture",data=jsonString,headers=header)

        return response;

    def authorizeAndCapturePayment(apiKey:string, apiSecret:string,messageLayer = MessageLayer()):
        
        header = {"X-API-KEY": apiKey,"X-API-SECRET":apiSecret,"Content-Type": "application/json"}

        enc = _encrypting(messageLayer.account,apiSecret,apiKey)
        messageLayer.account=enc

        enc = _encrypting(messageLayer.cvv2,apiSecret,apiKey)
        messageLayer.cvv2=enc

        jsonString = json.dumps(messageLayer.__dict__)
        jsonString = jsonString.replace("_MessageLayer__","")

        response = requests.post("http://164.90.146.112:8062/payments/authorizeandcapture",data=jsonString,headers=header)

        return response;

    def refundAuthorizePayment(apiKey:string, apiSecret:string,refundPayment = RefundPayment()):
        
        header = {"X-API-KEY": apiKey,"X-API-SECRET":apiSecret,"Content-Type": "application/json"}
        jsonString = json.dumps(refundPayment.__dict__)
        jsonString = jsonString.replace("_RefundPayment__","")

        response = requests.post("http://164.90.146.112:8062/payments/authorize/"+refundPayment.paymentTransactionId+"/refund",data=jsonString,headers=header)

        return response;

    def refundCapturePayment(apiKey:string, apiSecret:string,refundPayment = RefundPayment()):
        
        header = {"X-API-KEY": apiKey,"X-API-SECRET":apiSecret,"Content-Type": "application/json"}
        jsonString = json.dumps(refundPayment.__dict__)
        jsonString = jsonString.replace("_RefundPayment__","")

        response = requests.post("http://164.90.146.112:8062/payments/capture/"+refundPayment.paymentTransactionId+"/refund",data=jsonString,headers=header)

        return response;

    def voidAuthorizePayment(apiKey:string, apiSecret:string,voidPayment = VoidPayment()):
        
        header = {"X-API-KEY": apiKey,"X-API-SECRET":apiSecret,"Content-Type": "application/json"}
        jsonString = json.dumps(voidPayment.__dict__)
        jsonString = jsonString.replace("_VoidPayment__","")

        response = requests.post("http://164.90.146.112:8062/payments/authorize/"+voidPayment.paymentTransactionId+"/void",data=jsonString,headers=header)

        return response;

    def voidCapturePayment(apiKey:string, apiSecret:string,voidPayment = VoidPayment()):
        
        header = {"X-API-KEY": apiKey,"X-API-SECRET":apiSecret,"Content-Type": "application/json"}
        jsonString = json.dumps(voidPayment.__dict__)
        jsonString = jsonString.replace("_VoidPayment__","")

        response = requests.post("http://164.90.146.112:8062/payments/capture/"+voidPayment.paymentTransactionId+"/void",data=jsonString,headers=header)

        return response;

    def voidRefundPayment(apiKey:string, apiSecret:string,voidPayment = VoidPayment()):
        
        header = {"X-API-KEY": apiKey,"X-API-SECRET":apiSecret,"Content-Type": "application/json"}
        jsonString = json.dumps(voidPayment.__dict__)
        jsonString = jsonString.replace("_VoidPayment__","")

        response = requests.post("http://164.90.146.112:8062/payments/authorize/"+voidPayment.paymentTransactionId+"/voidrefund",data=jsonString,headers=header)

        return response;

def _encrypting(encryptstr,secret,salt):
    iv = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ];
    key = hashlib.pbkdf2_hmac('SHA256', secret.encode(), salt.encode(), 65536, 32)
    message = pad(encryptstr.encode(), AES.block_size)
    cipher = AES.new(key,AES.MODE_CBC,bytearray(iv))
    encrypt = base64.b64encode(cipher.encrypt(message))

    return str(encrypt,'utf-8')

def _decrypting(decryptstr,secret,salt):
    iv = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ];
    key = hashlib.pbkdf2_hmac('SHA256', secret.encode(), salt.encode(), 65536, 32)
    cipher = AES.new(key,AES.MODE_CBC,bytearray(iv))
    enc = base64.b64decode(decryptstr)
    decrypt = unpad(cipher.decrypt(enc), AES.block_size).decode('utf-8')

    return decrypt