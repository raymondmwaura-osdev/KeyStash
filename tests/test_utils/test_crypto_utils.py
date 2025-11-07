from src.utils import crypto_utils
import os

PASSWORD = b"master_password"

def test_encrypt_and_decrypt():
	"""
	Verify that encrypting and then decrypting a message
	returns the original plaintext.
	"""
	message = b"Test encryption and decryption."
	salt, encrypted_message = crypto_utils.encrypt(message, PASSWORD)
	decrypted_message = crypto_utils.decrypt(encrypted_message, PASSWORD, salt)

	assert message == decrypted_message

class TestGenerateKey:
	"""Unit tests for `crypto_utils.generate_key`."""

	def test_same_salt_same_key(self):
		"""
		Verify that the same password and salt combination
		produces the same derived key.
		"""
		salt = os.urandom(16)
		key1 = crypto_utils.generate_key(PASSWORD, salt)
		key2 = crypto_utils.generate_key(PASSWORD, salt)

		assert key1 == key2

	def test_diff_salt_diff_key(self):
		"""
		Verify that using different salts with the same password
		results in different derived keys.
		"""
		salt1 = os.urandom(16)
		salt2 = os.urandom(16)
		key1 = crypto_utils.generate_key(PASSWORD, salt1)
		key2 = crypto_utils.generate_key(PASSWORD, salt2)

		assert key1 != key2