# External imports -----------------------------------------------------------------------------------------------------
from pydantic_settings import BaseSettings, SettingsConfigDict





# Necessary classes, objects and functions -----------------------------------------------------------------------------

class EnvSettings(BaseSettings):
    sb_connection_string: str
    sb_host: str
    sb_port: int
    sb_database: str
    sb_user: str
    sb_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


env_settings = EnvSettings()





# Checking .env file accessibility (Option 01) -------------------------------------------------------------------------

# If we keep this code snippet active, and run 'python -m src.core.config' in the terminal, then only this config.py file
# will run, then all confidential variables from the .env file will print as a simple string. The .env file accessibility
# will be confirmed.

# if __name__ == "__main__":
#     print("If the .env file is readable then we'll see the .env variables below:")
#     print(env_settings)





# Checking .env file accessibility (Option 02) -------------------------------------------------------------------------

# If we keep this code snippet active, and run 'python -m src.core.config' in the terminal, then only this config.py file
# will run, then all confidential variables from the .env file will print as a well organized string from. The .env file
# accessibility will be confirmed.

# if __name__ == "__main__":
#     print("Checking if .env variables are loaded correctly...\n")
#
#     for field_name, value in env_settings.model_dump().items():
#         value_str = str(value)
#
#         if any(kw in field_name.lower() for kw in ("string", "user", "password", "pass")):
#             display_value = "*" * len(value_str)
#         else:
#             display_value = value_str
#
#         print(f"✅ {field_name.upper():<25}: {display_value}")





# Checking .env file accessibility (Option 03) -------------------------------------------------------------------------

# If we keep this code snippet active, then every time we will run this project, all confidential variables from the .env
# file will print as a well organized string from to prove that the .env file variables are accessible.

def check_env_settings():
    print("\nChecking if .env variables are loaded correctly...")

    for field_name, value in env_settings.model_dump().items():
        value_str = str(value)

        if any(kw in field_name.lower() for kw in ("string", "user", "password", "pass", "secret", "algorithm")):
            display_value = "*" * len(value_str)
        else:
            display_value = value_str

        print(f"    ✅ {field_name.upper():<30}: {display_value}")


if __name__ == "__main__":
    check_env_settings()




