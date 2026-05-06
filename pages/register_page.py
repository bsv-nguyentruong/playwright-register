"""
新規アカウント追加モーダル（アカウント管理）
https://admin.odakyu.bravesoft.vn/account-management

"""

from __future__ import annotations

import re

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage

ACCOUNT_MANAGEMENT_URL = "https://admin.odakyu.bravesoft.vn/account-management"


class RegisterPage(BasePage):
    """Dialog「新規アカウント追加」trên /account-management."""

    def __init__(self, page: Page):
        super().__init__(page)
        self._modal = page.locator(".modify-account-modal-content")

    @property
    def modal(self) -> Locator:
        """Vùng dialog đã mở (scope mọi get_by_* trong modal)."""
        return self._modal

    @property
    def _form(self) -> Locator:
        """Form trong modal — gắn label với field tốt hơn cho get_by_label."""
        return self._modal.locator("form.modal-content")

    # --- Điều hướng & mở modal (trang list) ---

    def navigate_account_management(self, wait_until: str = "domcontentloaded") -> None:
        self.page.goto(ACCOUNT_MANAGEMENT_URL, wait_until=wait_until)
        self.page.locator(".account-management").get_by_text(
            "アカウント管理", exact=False
        ).first.wait_for(state="visible", timeout=60_000)

    def dismiss_error_modal_if_present(self) -> None:
        back = self.page.locator(".common-modal-content").get_by_role(
            "button", name=re.compile(r"\s*戻る\s*")
        )
        if back.is_visible(timeout=2_000):
            back.click()
            self.page.wait_for_timeout(500)

    def wait_account_list_ready(self) -> None:
        overlay = self.page.locator(".loading-overlay")
        if overlay.count() > 0:
            overlay.first.wait_for(state="hidden", timeout=120_000)

    def prepare_account_management_view(self) -> None:
        for _ in range(4):
            self.wait_account_list_ready()
            back = self.page.locator(".common-modal-content").get_by_role(
                "button", name=re.compile(r"\s*戻る\s*")
            )
            if back.is_visible(timeout=1_500):
                back.click()
                self.page.wait_for_timeout(600)
                continue
            break

    def open_new_account_modal(self) -> None:
        self.prepare_account_management_view()
        mgmt = self.page.locator(".account-management")
        add = mgmt.get_by_role("button", name=re.compile(r"新規.*追加"))
        add.wait_for(state="visible", timeout=30_000)
        add.click(force=True)
        self._modal.locator(".title-confirm").get_by_text(
            "新規アカウント追加", exact=False
        ).wait_for(state="visible", timeout=20_000)

    # --- Quyền (multiselect Vue) ---

    def permission_block(self) -> Locator:
        return self._form.locator(".label-input").filter(has_text="権限").first

    def permission_combobox(self) -> Locator:
        return self.permission_block().get_by_role("combobox")

    def wait_no_global_overlay(self) -> None:
        self.wait_account_list_ready()
        self.dismiss_error_modal_if_present()
        self.wait_account_list_ready()

    def select_permission(self, label: str) -> None:
        self.wait_no_global_overlay()
        block = self.permission_block()
        block.get_by_role("combobox").click(force=True)
        block.locator(".multiselect-dropdown").wait_for(state="visible", timeout=10_000)
        block.get_by_role("option", name=label).click(force=True)

    def permission_display_text(self) -> str:
        return self.permission_combobox().inner_text()

    # --- Trường form (get_by_label trong scope form) ---

    def fill_account_name(self, value: str) -> None:
        # self._form.get_by_label("アカウント名", exact=False).fill(value) 
        self._form.locator("input[name='userName']").fill(value)
    ###NNTT: get_by_label() bị lỗi vì nó đang tìm thẻ <label> có text "アカウント名" thì không có
    #HTML chỗ này đang không có define giá trị nào để sử dụng user facing nên cần chuyển sang dùng XPATH, CSS
    # chỗ này nên đổi thành: self._form.locator("input[name='userName']").fill(value)

    def get_account_name_value(self) -> str:
        # return self._form.get_by_label("アカウント名", exact=False).input_value()
        return self._form.locator("input[name='userName']").input_value()
        ### NNTT: get_by_label() tương tự trên lỗi ở fill_account_name

    def fill_email(self, value: str) -> None:
        # self._form.get_by_label("メールアドレス", exact=False).fill(value)
        self._form.locator("input[name='email']").fill(value)
    ### NNTT: get_by_label() tương tự trên lỗi ở fill_account_name

    def get_email_value(self) -> str:
        # return self._form.get_by_label("メールアドレス", exact=False).input_value()
        return self._form.locator("input[name='email']").input_value()
    ### NNTT: get_by_label() tương tự trên lỗi ở fill_account_name

    def fill_password(self, value: str) -> None:
        # self._form.get_by_label("パスワード", exact=False).fill(value)
        self._form.locator("input[name='password']").fill(value)
    ### NNTT: get_by_label() tương tự trên lỗi ở fill_account_name

    def get_password_locator(self) -> Locator:
        # return self._form.get_by_label("パスワード", exact=False)
        return self._form.locator("input[name='password']")
    ### NNTT: get_by_label() tương tự trên lỗi ở fill_account_name

    def toggle_password_visibility(self) -> None:
        self.get_password_locator().locator("+ img").click()

    # --- Block điểm (khi có trên build) ---

    def point_change_section(self) -> Locator:
        # return self._modal.get_by_text("チケット組成時のポイント付与パラメータの変更権限")
        
    ### NNTT: do get_by_text() trả về chính thẻ label-title chứa text đó, chỉ trả có mỗi text không trả nguyên component
    #        nên get_by_text("有") sẽ bị lỗi do nằm trong sibling div ra ngoài scope → get_by_text("有") fail.
    # Nên đổi lại thành: 
        return self._modal.locator(".label-input").filter(
            has_text="チケット組成時のポイント付与パラメータの変更権限"
        )

    def has_point_change_section(self, timeout_ms: int = 2_000) -> bool:
        try:
            self.point_change_section().wait_for(state="visible", timeout=timeout_ms)
            return True
        except Exception:
            return False

    def select_point_change(self, aru_or_nashi: str) -> None:
        self.point_change_section().get_by_text(aru_or_nashi, exact=True).click()
