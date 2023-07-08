from datetime import timedelta, datetime

from fastapi import HTTPException, Request, security as _security
from passlib.context import CryptContext
import jwt


class AuthHandler(_security.HTTPBearer):
    secret = "SECRET"
    algorithm = "HS256"
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, auto_error: bool = True):
        super(AuthHandler, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: _security.HTTPAuthorizationCredentials = await super(
            AuthHandler, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid token")
        else:
            raise HTTPException(status_code=403, detail="Invalid or expired token")

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, data):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, minutes=5),
            "iat": datetime.utcnow(),
            "sub": data,
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        except jwt.PyJWTError:
            return None

    def get_login_token(self):
        return _security.OAuth2PasswordBearer(tokenUrl="/login/token")


auth_handler = AuthHandler()
