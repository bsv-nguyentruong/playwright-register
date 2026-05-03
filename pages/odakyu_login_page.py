"""
Odakyu マスター管理者ログイン
https://admin.odakyu.bravesoft.vn/login
"""

from __future__ import annotations

from pages.base_page import BasePage

LOGIN_URL = "https://admin.odakyu.bravesoft.vn/login"


class OdakyuLoginPage(BasePage):
    email_input = '//form[contains(@class,"login-form")]//input[@name="email"]'
    password_input = '//input[@id="password"]'
    login_button = '//button[@type="submit" and contains(@class,"login-button")]'
    password_toggle_icon = '//img[contains(@class,"eye-password")]'

    def __init__(self, page):
        super().__init__(page)

    def open_login_page(self, wait_until: str = "domcontentloaded") -> None:
        self.page.goto(LOGIN_URL, wait_until=wait_until)
        self.page.locator(self.email_input).wait_for(state="visible", timeout=30_000)

    def input_email(self, email: str) -> None:
        self.fill(self.email_input, email)

    def input_password(self, password: str) -> None:
        self.fill(self.password_input, password)

    def wait_until_login_button_enabled(self, timeout_ms: int = 30_000) -> None:
        self.page.wait_for_function(
            "() => { const b = document.querySelector('button.login-button'); return b && !b.disabled; }",
            timeout=timeout_ms,
        )

    def click_login(self) -> None:
        self.wait_until_login_button_enabled()
        self.click(self.login_button)

    def login(
        self,
        email: str,
        password: str,
        *,
        open_page: bool = True,
        wait_leave_login: bool = True,
        post_login_timeout_ms: int = 120_000,
    ) -> None:
        if open_page:
            self.open_login_page()
        self.input_email(email)
        self.input_password(password)
        self.click_login()
        if wait_leave_login:
            self.wait_leave_login_url(timeout_ms=post_login_timeout_ms)

    def wait_leave_login_url(self, timeout_ms: int = 120_000) -> None:
        self.page.wait_for_function(
            "() => !window.location.href.includes('/login')",
            timeout=timeout_ms,
        )

    def toggle_password_visibility(self) -> None:
        self.click(self.password_toggle_icon)

    def is_on_login_path(self) -> bool:
        return "/login" in (self.page.url or "")
