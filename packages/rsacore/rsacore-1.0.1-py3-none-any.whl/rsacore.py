import rsa
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class Core:
	def __init__(self):
		self.aes_key = get_random_bytes(16)
		self.aes = AES.new(self.aes_key, AES.MODE_EAX)
	
	def GenKeys(self):
		pubkey, self.rsa_privkey = rsa.newkeys(1024)
		return pubkey
	
	def SetPubKey(self, pubkey):
		self.rsa_pubkey = pubkey
	
	def EncryptRSA(self, data):
		return rsa.encrypt(data, self.rsa_pubkey)
	
	def DecryptRSA(self, data):
		return rsa.decrypt(data, self.rsa_privkey)
	
	def SignRSA(self, data):
		return rsa.sign(data, self.rsa_privkey, "SHA-256")
	
	def CheckSignRSA(self, data, sign):
		try:
			if rsa.verify(data, sign, self.rsa_pubkey):
				return True
		except rsa.pkcs1.VerificationError:
			return False
	
	def EncryptAES(self, data):
		nonce = self.aes.nonce
		return self.aes.encrypt(data), nonce
	
	def DecryptAES(self, data, nonce):
		return AES.new(self.aes_key, AES.MODE_EAX, nonce).decrypt(data)
	
	def Encrypt(self, msg):
		msg, nonce = self.EncryptAES(msg)
		aes_data = {"AES_KEY": self.aes_key.hex(), "NONCE": nonce.hex()}
		aes_data = self.EncryptRSA(json.dumps(aes_data).encode()).hex()
		data = {"data": msg.hex(), "aes_data": aes_data}
		data = {"data": data, "sign": self.SignRSA(json.dumps(data).encode()).hex()}
		return json.dumps(data)
	
	def Decrypt(self, msg):
		msg = json.loads(msg)
		data_msg = msg["data"]
		aes_data = data_msg["aes_data"]
		sign = msg["sign"]
		msg = json.dumps(data_msg).encode()
		print(self.CheckSignRSA(msg, bytes.fromhex(sign)))
		if not self.CheckSignRSA(msg, bytes.fromhex(sign)):
			print("Verify fail!")
			return None
		data = self.DecryptRSA(bytes.fromhex(aes_data))
		data = json.loads(data)
		self.aes_key = bytes.fromhex(data["AES_KEY"])
		nonce = bytes.fromhex(data["NONCE"])
		data = self.DecryptAES(bytes.fromhex(data_msg["data"]), nonce)
		return data
		

