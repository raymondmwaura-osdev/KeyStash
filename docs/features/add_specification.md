# `ADD`

> This document defines the intended design, behavior, and constraints of a software feature prior to implementation.

**Feature Name:**  
**`add`**: Add a password entry in the vault file.

**Objective:**  
This feature enables users to securely add a new credential record (login details) to the encrypted vault file (`vault.json`). The entry includes the service name, password, and optionally a username and email. This provides a structured and secure way to store login credentials for various online services.

**Overview:**  
The `add` feature extends the vault system by allowing users to store credentials through the command line in a secure and encrypted manner. It interacts with the encryption module (`crypto_utils`) and file management system (`storage`) to ensure all sensitive data remains encrypted at rest. The feature also ensures that each service entry is unique, maintaining data integrity and preventing accidental duplication. It serves as one of the primary user-facing operations within the password manager.

---

## Functional Requirements

1. The command must support the following options:
   - `-s` / `--service`: Name of the service (e.g., `github.com`).  
   - `-u` / `--username`: Optional username associated with the service.  
   - `-e` / `--email`: Optional email for the account.  
   - `-p` / `--password`: Password for the account.  
   - `--nousername`: Specifies that no username is associated with the entry.  
   - `--noemail`: Specifies that no email is associated with the entry.
2. The `--service` and `--password` arguments are mandatory.
3. Before modifying the vault, the user must provide their master password for authentication.  
   This password is used to decrypt the existing vault and re-encrypt it after modification.
4. If the vault file does not exist, the program must create it automatically before writing the new entry.
5. Duplicate service entries must be detected. The system should:
   - Reject duplicate entries unless explicitly allowed or overwritten by the user.

---

## Input Validation Rules

* `--username` and `--nousername` are mutually exclusive.  
* `--email` and `--noemail` are mutually exclusive.  
* Missing `--service` or `--password` triggers an error message or help output.  
* If the `--password` flag is omitted, the program must securely prompt the user for a password using masked input.  
* If any argument violates mutual exclusivity or is invalid, execution should stop with an appropriate error message.

---

## Security Requirements

* The vault file must remain encrypted at all times except during in-memory processing.  
* Encryption and decryption must use PBKDF2-HMAC (SHA-256) with a 16-byte random salt and Fernet symmetric encryption.  
* The master password must never be logged, printed, or stored in plaintext.  
* Input collected through the command line or interactive prompt must be handled securely using the `getpass` module.  
* The system must clear sensitive data from memory once the operation completes.

---

## User Flow

1. User executes a command such as:  
   ```bash
   keystash add -s github.com -u johndoe -p MySecret123
   ```
2. The program prompts the user to enter the master password securely.
3. The vault file is decrypted (or created if it does not exist).
4. The new entry is validated and added to the vault.
5. The vault is re-encrypted and written back to disk.
6. The system confirms success to the user.

---

## Example Output

```
[✓] Credentials for 'github.com' added successfully.
[✗] Missing required argument: --service
[✗] Invalid master password. Operation aborted.
```

---

## Dependencies

* **Internal Modules:**

  * `storage`; for reading and writing encrypted JSON data.

* **External Libraries:**

  * `argparse`; for command-line argument parsing.
  * `getpass`; for secure password input.
  * `pathlib`; for data serialization and file management.

---

## Test Conditions

* **Successful Add:** Adding a valid entry with all parameters provided.
* **Optional Fields Missing:** Adding entries without username or email.
* **Invalid Input:** Missing required flags (`--service` or `--password`).
* **Authentication Failure:** Incorrect master password entered.
* **Duplicate Handling:** Attempting to add an entry for an existing service.
* **File Creation:** Adding an entry when the vault does not yet exist.
* **Encryption Integrity:** Verifying that the resulting file remains unreadable without decryption.

---
