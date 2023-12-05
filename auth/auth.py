import time
from typing import Dict

import jwt
from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy
from decouple import config

cookie_transport = CookieTransport(cookie_max_age=3600)




SECRET = config("secret")
JWT_ALGORITHM = config("algoritm")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

# def token_response(token: str):
#     return {
#         "access_token": token
#     }
#
# # function used for signing the JWT string
# def signJWT(user_id: str) -> Dict[str, str]:
#     payload = {
#         "user_id": user_id,
#         "expires": time.time() + 600
#     }
#     token = jwt.encode(payload, SECRET, algorithm=JWT_ALGORITHM)
#
#     return token_response(token)
#
#
# def decodeJWT(token: str) -> dict:
#     try:
#         decoded_token = jwt.decode(token, SECRET, algorithms=[JWT_ALGORITHM])
#         return decoded_token if decoded_token["expires"] >= time.time() else None
#     except:
#         return {}
#
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)