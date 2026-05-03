"""
新規アカウント追加（仕様 新規アカウント追加-1 〜 -17）
"""

from __future__ import annotations

import pytest

from pages.register_page import RegisterPage


def _require_point_change(reg: RegisterPage) -> None:
    if not reg.has_point_change_section():
        pytest.skip("この環境では「チケット組成時のポイント付与パラメータの変更権限」が表示されない")


def test_new_account_01_screen_title(register_page):
    """新規アカウント追加-1 画面タイトル"""
    assert register_page.modal.get_by_text("新規アカウント追加").is_visible()


def test_new_account_02_url(register_page):
    """新規アカウント追加-2 URL"""
    assert "/account-management" in register_page.page.url


def test_new_account_03_account_name_label(register_page):
    """新規アカウント追加-3 アカウント名ラベル"""
    m = register_page.modal
    assert m.get_by_text("アカウント名", exact=False).is_visible()
    assert m.get_by_text("255文字以内", exact=False).is_visible()


def test_new_account_04_account_name_input(register_page):
    """新規アカウント追加-4 アカウント名入力"""
    register_page.fill_account_name("テスト太郎")
    assert register_page.get_account_name_value() == "テスト太郎"


def test_new_account_05_email_label(register_page):
    """新規アカウント追加-5 メールアドレスラベル"""
    assert register_page.modal.get_by_text("メールアドレス", exact=False).is_visible()


def test_new_account_06_email_input_valid(register_page):
    """新規アカウント追加-6 メール形式"""
    email = "trucly@bravesoft-vn.com.vn"
    register_page.fill_email(email)
    assert register_page.get_email_value() == email


def test_new_account_07_password_label(register_page):
    """新規アカウント追加-7 パスワードラベル"""
    m = register_page.modal
    assert m.get_by_text("パスワード", exact=False).is_visible()
    assert m.get_by_text("8文字以上32文字以内", exact=False).is_visible()


def test_new_account_08_password_placeholder(register_page):
    """新規アカウント追加-8 placeholder"""
    ph = register_page.get_password_locator().get_attribute("placeholder")
    assert ph == "**********"


def test_new_account_09_password_masked_input(register_page):
    """新規アカウント追加-9 入力・マスク"""
    register_page.fill_password("abcd1234")
    loc = register_page.get_password_locator()
    assert loc.input_value() == "abcd1234"
    assert loc.get_attribute("type") == "password"


def test_new_account_10_permission_select_initial(register_page):
    """新規アカウント追加-10 権限セレクト初期"""
    block = register_page.permission_block()
    assert block.locator('[role="combobox"]').is_visible()
    assert block.locator(".multiselect-caret").is_visible()
    txt = register_page.permission_display_text()
    assert "マスター管理者" not in txt
    assert "テナント管理者" not in txt


def test_new_account_11_permission_master(register_page):
    """新規アカウント追加-11 マスター管理者"""
    register_page.select_permission("マスター管理者")
    assert "マスター管理者" in register_page.permission_display_text()


def test_new_account_12_permission_tenant(register_page):
    """新規アカウント追加-12 テナント管理者"""
    register_page.select_permission("テナント管理者")
    assert "テナント管理者" in register_page.permission_display_text()


def test_new_account_13_permission_single_choice(register_page):
    """新規アカウント追加-13 単一選択"""
    register_page.select_permission("マスター管理者")
    register_page.select_permission("テナント管理者")
    disp = register_page.permission_display_text()
    assert "テナント管理者" in disp
    assert "マスター管理者" not in disp


def test_new_account_14_point_change_labels(register_page):
    """新規アカウント追加-14"""
    _require_point_change(register_page)
    sec = register_page.point_change_section()
    assert sec.get_by_text("有", exact=True).is_visible()
    assert sec.get_by_text("無", exact=True).is_visible()


def test_new_account_15_point_change_select_yes(register_page):
    """新規アカウント追加-15"""
    _require_point_change(register_page)
    register_page.select_point_change("有")


def test_new_account_16_point_change_select_no(register_page):
    """新規アカウント追加-16"""
    _require_point_change(register_page)
    register_page.select_point_change("無")


def test_new_account_17_point_change_exclusive(register_page):
    """新規アカウント追加-17"""
    _require_point_change(register_page)
    register_page.select_point_change("有")
    register_page.select_point_change("無")
    assert register_page.point_change_section().get_by_text("無", exact=True).is_visible()
