import os

import pytest

from pages.odakyu_login_page import OdakyuLoginPage
from pages.register_page import RegisterPage


@pytest.fixture
def register_page(page):
    """
    ログイン済み → アカウント管理 → エラーモーダルを閉じる（あれば）→ 新規アカウント追加を開く。
    認証: 環境変数 ODAKYU_ADMIN_EMAIL / ODAKYU_ADMIN_PASSWORD（未設定時は例のまま）。
    """
    email = os.environ.get("ODAKYU_ADMIN_EMAIL", "kimtran@bravesoft.com.vn")
    password = os.environ.get("ODAKYU_ADMIN_PASSWORD", "brave0404")
    OdakyuLoginPage(page).login(email, password, open_page=True, wait_leave_login=True)
    reg = RegisterPage(page)
    reg.navigate_account_management()
    reg.open_new_account_modal()
    return reg
