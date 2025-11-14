from src.features import add

class TestAddCredentials:
    def test_check_exact_duplicate(self, monkeypatch, mocker, tmp_path):
        cred1 = {
            "service": "service1",
            "password": "password1",
            "username": "username1",
            "email": "email1"
        }
        vault_contents = [
            cred1,
            {
                "service": "service2",
                "password": "password2",
                "username": "username2",
                "email": "email2"
            }
        ]

        storage_read_mock = mocker.Mock()
        storage_read_mock.return_value = vault_contents
        mocker.patch("src.features.add.storage.read_json", storage_read_mock)

        vault = tmp_path / "vault.json"
        vault.touch()
        monkeypatch.setattr("src.features.add.constants.VAULT", vault)

        sys_exit_mock = mocker.Mock()
        mocker.patch("src.features.add.sys.exit", sys_exit_mock)
        
        add.AddCredentials(**cred1)
        sys_exit_mock.assert_called_once()

class TestFilterCredentials:
	"""Unit tests for `add.filter_credentials`."""
	def test_empty_credentials(self):
		input_cred = []
		output_cred = add.filter_credentials(
			input_cred,
			service="service1",
			password="password1",
			username="username1",
			email="email1"
		)
		expected_output = []

		assert output_cred == expected_output

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
