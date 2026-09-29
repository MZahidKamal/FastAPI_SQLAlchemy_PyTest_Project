from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from src.core.config import env_settings
import uuid





def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    data_to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=env_settings.access_token_expire_minutes)
    data_to_encode.update({"exp": expire, "type": "access"})
    encoded_access_token = jwt.encode(data_to_encode, env_settings.secret_key, algorithm=env_settings.algorithm)
    return encoded_access_token





# def create_refresh_token(data: dict) -> str:
#     to_encode = data.copy()
#     expire = datetime.now(timezone.utc) + timedelta(days=env_settings.refresh_token_expire_days)
#     to_encode.update({"exp": expire, "type": "refresh"})
#     encoded_refresh_token = jwt.encode(to_encode, env_settings.secret_key, algorithm=env_settings.algorithm)
#     return encoded_refresh_token

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=env_settings.refresh_token_expire_days)
    to_encode.update({"exp": expire, "type": "refresh", "jti": str(uuid.uuid4())})
    encoded_refresh_token = jwt.encode(to_encode, env_settings.secret_key, algorithm=env_settings.algorithm)
    return encoded_refresh_token





def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, env_settings.secret_key, algorithms=[env_settings.algorithm])
        return payload
    except JWTError:
        return None





# ----------------------------------------------------------------------------------------------------------------------

# if __name__ == "__main__":
#     token = create_access_token({"sub": "123"})
#     print("Token:", token)
#     print("Decoded:", decode_token(token))      # To run only this file, run 'python -m src.core.security' command in the IDE terminal.





def check_jwt_settings():
    print("\nChecking if JWT encryptions are working correctly...")

    try:
        test_token = create_access_token({"sub": "startup-check"})
        decoded = decode_token(test_token)

        if decoded is None:
            raise ValueError("JWT decode failed during startup check.")

        print("    ✅ JWT settings are valid — token creation and decoding both work.")

    except Exception as e:
        print("❌ JWT settings check failed.")
        print(f"   Reason: {e}")


if __name__ == "__main__":
    check_jwt_settings()




