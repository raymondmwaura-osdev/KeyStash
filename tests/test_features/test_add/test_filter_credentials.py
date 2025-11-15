from src.features import add

cred1 = {
    "service": "service1",
    "password": "password1",
    "username": "username1",
    "email": "email1"
    }
cred2 = {
    "service": "service2",
    "password": "password2",
    "username": "username2",
    "email": "email2"
}

class TestFilterCredentials:
    """Unit tests for `add.filter_credentials`."""
    def test_empty_credentials(self):
        """
        Validate that `add.filter_credentials` provides an empty list
        when the input credential set contains no records.
        """
        input_cred = []
        output_cred = add.filter_credentials(
            input_cred,
            **cred1
        )

        assert output_cred == []

    def test_exact_duplicate(self):
        """
        Confirm that `add.filter_credentials` isolates and returns only
        the credential entry that matches all supplied fields.
        """
        input_cred = [cred1, cred2]
        output_cred = add.filter_credentials(
            input_cred,
            **cred1
        )
        expected_output = [cred1]

        assert output_cred == expected_output
