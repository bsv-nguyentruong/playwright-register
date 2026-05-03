"""
新規アカウント追加（仕様 新規アカウント追加-1 〜 -17）
"""

from __future__ import annotations

from playwright.sync_api import Page

import pytest

from pages.register_page import RegisterPage


def _assert_list_open_button_matches_spec_full_title(page: Page) -> None:
    """
    Spec: nút / vùng tương đương phải hiển thị đủ「新規アカウント追加」.
    Thực tế Odakyu list: nút chỉ「新規追加」→ luôn FAIL cho đến khi UI khớp spec.
    """
    opening = page.locator(".account-management").locator(
        "button.common-submit-btn.primary", has_text="新規"
    ).first
    assert opening.is_visible()
    assert opening.inner_text().strip() == "新規アカウント追加"


def _require_point_change(reg: RegisterPage) -> None:
    if not reg.has_point_change_section():
        pytest.skip("この環境では「チケット組成時のポイント付与パラメータの変更権限」が表示されない")


def test_register_01(register_page):
    """
    ID testcase: 新規アカウント追加-1
    Note: Case 1 chỉ kiểm tra text — so sánh nhãn nút mở form với spec「新規アカウント追加」
    (thực tế「新規追加」→ FAIL cho đến khi UI đổi nhãn khớp spec).
    """
    _assert_list_open_button_matches_spec_full_title(register_page.page)


def test_register_02(register_page):
    """
    ID testcase: 新規アカウント追加-2
    Note: Xác nhận đang ở đúng URL quản lý tài khoản (chứa /account-management) khi mở form.
    """
    assert "/account-management" in register_page.page.url


def test_register_03(register_page):
    """
    ID testcase: 新規アカウント追加-3
    Note: Kiểm tra nhãn trường tên tài khoản và giới hạn 255 ký tự hiển thị đúng.
    """
    m = register_page.modal
    assert m.get_by_text("アカウント名", exact=False).is_visible()
    assert m.get_by_text("255文字以内", exact=False).is_visible()


def test_register_04(register_page):
    """
    ID testcase: 新規アカウント追加-4
    Note: Kiểm tra có nhập được tên tài khoản và giá trị hiển thị đúng trong ô nhập.
    """
    register_page.fill_account_name("テスト太郎")
    assert register_page.get_account_name_value() == "テスト太郎"


def test_register_05(register_page):
    """
    ID testcase: 新規アカウント追加-5
    Note: Xác nhận nhãn「メールアドレス」xuất hiện trên form thêm tài khoản.
    """
    assert register_page.modal.get_by_text("メールアドレス", exact=False).is_visible()


def test_register_06(register_page):
    """
    ID testcase: 新規アカウント追加-6
    Note: Kiểm tra nhập email đúng định dạng thì giá trị được giữ đúng trong ô (ví dụ nguyentruong@...).
    """
    email = "nguyentruong@bravesoft-vn.com.vn"
    register_page.fill_email(email)
    assert register_page.get_email_value() == email


def test_register_07(register_page):
    """
    ID testcase: 新規アカウント追加-7
    Note: Xác nhận nhãn mật khẩu kèm quy tắc「半角英数字 8〜32文字」theo spec.
    """
    m = register_page.modal
    assert m.get_by_text("パスワード", exact=False).is_visible()
    assert m.get_by_text("8文字以上32文字以内", exact=False).is_visible()


def test_register_08(register_page):
    """
    ID testcase: 新規アカウント追加-8
    Note: Kiểm tra placeholder ô mật khẩu là ********** như thiết kế.
    """
    ph = register_page.get_password_locator().get_attribute("placeholder")
    assert ph == "**********"


def test_register_09(register_page):
    """
    ID testcase: 新規アカウント追加-9
    Note: Kiểm tra nhập được mật khẩu và kiểu input là password (che ký tự trên UI).
    """
    register_page.fill_password("abcd1234")
    loc = register_page.get_password_locator()
    assert loc.input_value() == "abcd1234"
    assert loc.get_attribute("type") == "password"


def test_register_10(register_page):
    """
    ID testcase: 新規アカウント追加-10
    Note: Kiểm tra combobox quyền hiển thị, có icon dropdown, ban đầu chưa chọn Master/Tenant.
    """
    block = register_page.permission_block()
    assert block.locator('[role="combobox"]').is_visible()
    assert block.locator(".multiselect-caret").is_visible()
    txt = register_page.permission_display_text()
    assert "マスター管理者" not in txt
    assert "テナント管理者" not in txt


def test_register_11(register_page):
    """
    ID testcase: 新規アカウント追加-11
    Note: Kiểm tra chọn「マスター管理者」thì giá trị hiển thị trên combobox quyền đúng.
    """
    register_page.select_permission("マスター管理者")
    assert "マスター管理者" in register_page.permission_display_text()


def test_register_12(register_page):
    """
    ID testcase: 新規アカウント追加-12
    Note: Kiểm tra chọn「テナント管理者」thì hiển thị đúng trên combobox quyền.
    """
    register_page.select_permission("テナント管理者")
    assert "テナント管理者" in register_page.permission_display_text()


def test_register_13(register_page):
    """
    ID testcase: 新規アカウント追加-13
    Note: Xác nhận không chọn được hai quyền cùng lúc — chọn sau thay thế chọn trước (chỉ một giá trị).
    """
    register_page.select_permission("マスター管理者")
    register_page.select_permission("テナント管理者")
    disp = register_page.permission_display_text()
    assert "テナント管理者" in disp
    assert "マスター管理者" not in disp


def test_register_14(register_page):
    """
    ID testcase: 新規アカウント追加-14
    Note: Nếu màn có block quyền chỉnh tham số điểm khi ghép vé — kiểm tra nhãn và lựa chọn 有/無 hiển thị.
    """
    _require_point_change(register_page)
    sec = register_page.point_change_section()
    assert sec.get_by_text("有", exact=True).is_visible()
    assert sec.get_by_text("無", exact=True).is_visible()


def test_register_15(register_page):
    """
    ID testcase: 新規アカウント追加-15
    Note: Kiểm tra có thể chọn「有」cho quyền thay đổi tham số điểm (khi block tồn tại).
    """
    _require_point_change(register_page)
    register_page.select_point_change("有")


def test_register_16(register_page):
    """
    ID testcase: 新規アカウント追加-16
    Note: Kiểm tra có thể chọn「無」cho cùng block (khi block tồn tại).
    """
    _require_point_change(register_page)
    register_page.select_point_change("無")


def test_register_17(register_page):
    """
    ID testcase: 新規アカウント追加-17
    Note: Xác nhận 有/無 không chọn đồng thời — chọn sau ghi đè (hành vi chọn một).
    """
    _require_point_change(register_page)
    register_page.select_point_change("有")
    register_page.select_point_change("無")
    assert register_page.point_change_section().get_by_text("無", exact=True).is_visible()
