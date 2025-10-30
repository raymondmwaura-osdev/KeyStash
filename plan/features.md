# KeyStash

### Primary Features

+ Allow the user to add passwords. Have the following fields:
    - `service`: The site, e.g. `github`, `leetcode`.
    - `username`: User's username on the site. Example: `yomama123`.
    - `password`: The password to the site.
    - `email`: The email used to sign in to the site.

+ Allow the user to delete passwords. Completely remove the entry.
+ Save the passwords in a json file.

  ```json
  {
    "firstnamesecondname@gmail.com": [
      {
        "service": "github",
        "username": "yomama123",
        "password": "lk*['kaD23",
      },

      {
        "service": "leetcode",
        ...
      },

      ...
    ],

    "secondemail": [
      ...
    ]
  }
  ```

+ Encrypt the json file. Generate the encryption key from a master password provided by the user.
+ Allow the user to read specific passwords. Filter by `email`, `username`, or `service`. Have different command-line options for specifying these.
+ Only provide the passwords when a master key is provided to verify the user's identity.

### Additional Features

+ Backup the file to a cloud service like google drive.
