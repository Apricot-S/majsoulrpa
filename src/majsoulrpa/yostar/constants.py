import re
from datetime import timedelta

YOSTAR_EMAIL_ADDRESS = "info@passport.yostar.co.jp"
YOSTAR_EMAIL_SUBJECT_PATTERN = re.compile(
    r"^【Yostar】メールアドレスの認証コードは　(?P<code>\d{6})$",
)
VERIFICATION_EMAIL_EXPIRATION = timedelta(minutes=30)
