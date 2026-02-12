# Unit tests for `src.features.get`.
from types import SimpleNamespace
from src.features import get
import pytest

class TestGet:
    """Unit tests for 'get.get'."""
    def test_empty_credentials(self, mocker, capsys):
        """
        Verfiy that 'get' prints a message and exits when the vault is empty.
        """
        storage_read_mock = mocker.patch(
            "src.features.get.storage.read_vault",
            return_value = []
        )
        namespace = SimpleNamespace(
            name = "name",
            id = None
        )

        with pytest.raises(SystemExit):
            get.get(namespace)

        output = capsys.readouterr()
        assert "The vault is empty. Use 'keystash add' to save credentials to the vault." in output.out

    def test_valid_id(self, mocker, capsys):
        """
        Verify that 'get' copies the password to the clipboard when a valid
        ID is given.
        """
        credential = {
            "service": "service1",
            "password": "StrongPassword123",
            "username": None,
            "email": None,
            "name": "name1",
            "id": 123
        }
        copy_mock = mocker.patch("src.features.get.pyperclip.copy")
        storage_read_mock = mocker.patch(
            "src.features.get.storage.read_vault",
            return_value = [credential]
        )
        
        namespace = SimpleNamespace(id=credential["id"], name=None)
        get.get(namespace)

        copy_mock.assert_called_with(credential["password"])

        output = capsys.readouterr()
        assert "Password copied to clipboard." in output.out
