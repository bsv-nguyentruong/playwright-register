from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url)

    def click(self, selector):
        self.page.click(selector)

    def fill(self, selector, text):
        self.page.fill(selector, text)

    def get_input_value(self, selector):
        return self.page.input_value(selector)

    def is_text_visible(self, text):
        return self.page.is_visible(f"text={text}")

    def dismiss_error_modal_if_present(self, timeout: int = 3_000) -> bool:
        """
        Do thỉnh thoảng code sẽ dễ bị failed do xuất hiện modal báo lỗi, 
        nên chị có thể tạo 1 hàm mục đích để chặn việc đó xảy ra. 
        Việc tạo hàm sẽ apply ở nhiều màn hình nên sẽ để ở base_page.py 
        sau đó gọi ra ở conftest.py để xử lý
        """
        back_button = self.page.get_by_role("button", name="戻る")
        try:
            back_button.wait_for(state="visible", timeout=timeout)
            back_button.click()
            # Wait for the modal to disappear before continuing
            back_button.wait_for(state="hidden", timeout=2000)
            return True
        except Exception:
            # Modal was not present — safe to continue
            return False