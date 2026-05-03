"""
新規アカウント追加モーダル（アカウント管理）
https://admin.odakyu.bravesoft.vn/account-management
"""

from __future__ import annotations

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage

ACCOUNT_MANAGEMENT_URL = "https://admin.odakyu.bravesoft.vn/account-management"


class RegisterPage(BasePage):
    """「新規アカウント追加」ダイアログ。"""

    def __init__(self, page: Page):
        super().__init__(page)
        self._modal = page.locator(".modify-account-modal-content")

    @property
    def modal(self) -> Locator:
        return self._modal

    def navigate_account_management(self, wait_until: str = "domcontentloaded") -> None:
        self.page.goto(ACCOUNT_MANAGEMENT_URL, wait_until=wait_until)
        self.page.locator(".account-management, .page-main-title").first.wait_for(
            state="visible", timeout=60_000
        )

    def dismiss_error_modal_if_present(self) -> None:
        back = self.page.locator(".common-modal-content .back-btn")
        if back.is_visible(timeout=2_000):
            back.click()
            self.page.wait_for_timeout(500)

    def wait_account_list_ready(self) -> None:
        """ローディングオーバーレイが消えるまで待つ（クリックが遮られるのを防ぐ）。"""
        overlay = self.page.locator(".loading-overlay")
        if overlay.count() > 0:
            overlay.first.wait_for(state="hidden", timeout=120_000)

    def prepare_account_management_view(self) -> None:
        """一覧表示可能になるまで（オーバーレイ・エラーモーダル）。"""
        for _ in range(4):
            self.wait_account_list_ready()
            back = self.page.locator(".common-modal-content .back-btn")
            if back.is_visible(timeout=1_500):
                back.click()
                self.page.wait_for_timeout(600)
                continue
            break

    def open_new_account_modal(self) -> None:
        self.prepare_account_management_view()
        root = self.page.locator(".account-management")
        add = root.locator("button", has_text="新規アカウント追加").or_(
            root.locator("button", has_text="新規追加")
        ).first
        add.wait_for(state="visible", timeout=30_000)
        add.click(force=True)
        self._modal.locator(".title-confirm").wait_for(state="visible", timeout=20_000)

    def permission_block(self) -> Locator:
        return self._modal.locator(".label-input").filter(has_text="権限").first

    def permission_combobox(self) -> Locator:
        return self.permission_block().locator('[role="combobox"]')

    def wait_no_global_overlay(self) -> None:
        """モーダル操作中に再表示されるローディング／エラーダイアログを処理。"""
        self.wait_account_list_ready()
        self.dismiss_error_modal_if_present()
        self.wait_account_list_ready()

    def select_permission(self, label: str) -> None:
        self.wait_no_global_overlay()
        block = self.permission_block()
        block.locator('[role="combobox"]').click(force=True)
        block.locator(".multiselect-dropdown").wait_for(state="visible", timeout=10_000)
        block.locator(".multiselect-option", has_text=label).click(force=True)

    def permission_display_text(self) -> str:
        return self.permission_combobox().inner_text()

    def fill_account_name(self, value: str) -> None:
        self._modal.locator('input[name="userName"]').fill(value)

    def get_account_name_value(self) -> str:
        return self._modal.locator('input[name="userName"]').input_value()

    def fill_email(self, value: str) -> None:
        self._modal.locator('form.modal-content input[name="email"]').fill(value)

    def get_email_value(self) -> str:
        return self._modal.locator('form.modal-content input[name="email"]').input_value()

    def fill_password(self, value: str) -> None:
        self._modal.locator('input[name="password"].inputPassword').fill(value)

    def get_password_locator(self) -> Locator:
        return self._modal.locator('input[name="password"].inputPassword')

    def toggle_password_visibility(self) -> None:
        self._modal.locator("img.eye-password").click()

    def point_change_section(self) -> Locator:
        return self._modal.get_by_text("チケット組成時のポイント付与パラメータの変更権限")

    def has_point_change_section(self, timeout_ms: int = 2_000) -> bool:
        try:
            self.point_change_section().wait_for(state="visible", timeout=timeout_ms)
            return True
        except Exception:
            return False

    def select_point_change(self, aru_or_nashi: str) -> None:
        self.point_change_section().get_by_text(aru_or_nashi, exact=True).click()
