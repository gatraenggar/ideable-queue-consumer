from decouple import config
import jwt

class TokenManager():
    def verify_random_token(token):
        return jwt.decode(token, config("RANDOM_TOKEN_KEY"), algorithms=["HS256"])
