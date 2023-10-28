import base64
import hashlib
import hmac
import json
# Секретный ключ для подписи токена
SECRET_KEY = 'PUTIN_BOMBA_WZRIW_CHECHNYA'
# Функция для генерации токена на основе почты и пароля
def generate_token(email, password):
    # Проверка пользователя по почте и паролю (реализуйте свою логику)
    if check_user(email, password):
        # Создаем заголовок (Header)
        header = {
            "alg": "HS256",
            "typ": "JWT"
        }
        encoded_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode()

        # Создаем JSON-полезную нагрузку (Payload)
        payload = {
            "email": email,
            "password_hash": hashlib.sha256(password.encode()).hexdigest()
        }
        encoded_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()

        # Создаем подпись (Signature)
        signature = base64.urlsafe_b64encode(hmac.new(SECRET_KEY.encode(), (encoded_header + '.' + encoded_payload).encode(), hashlib.sha256).digest()).decode()

        # Создание JWT
        jwt_token = f'{encoded_header}.{encoded_payload}.{signature}'
        return jwt_token
    else:
        return None

# Функция для проверки пользователя (заглушка, реализуйте свою логику)
def check_user(email, password):
    # Здесь вы должны реализовать проверку почты и пароля в вашей базе данных или хранилище
    # В этом примере, предполагается, что пользователь существует всегда
    return True

