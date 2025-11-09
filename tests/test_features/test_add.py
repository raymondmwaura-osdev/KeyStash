from src.features import add

class TestFilterCredentials:
	"""Unit tests for `add.filter_credentials`."""

	def test_exact_duplicate(self):
		input_cred = [{
			"service": "service1",
			"password": "password1",
			"username": "username1",
			"email": "email1"
		},
		{
			"service": "service2",
			"password": "password2",
			"username": "username2",
			"email": "email2"
		}]
		output_cred = add.filter_credentials(
			input_cred,
			service="service1",
			password="password1",
			username="username1",
			email="email1"
		)
		expected_output = [{
			"service": "service1",
			"password": "password1",
			"username": "username1",
			"email": "email1"
		}]

		assert output_cred == expected_output