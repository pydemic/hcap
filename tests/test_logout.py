from django.urls import reverse

from .base import SeleniumTestCase, login, create_test_user


class LogoutTestCase(SeleniumTestCase):
    def test_logout(self):
        login_url = f"{self.live_server_url}{reverse('account_login')}"
        self.browser.get(login_url)
        create_test_user()
        login(self.browser)

        before_logout_url = self.browser.current_url

        logout_btn = self.browser.find_element_by_xpath("//a[@href='/accounts/logout/']")
        logout_btn.click()

        self.assertNotEqual(before_logout_url, self.browser.current_url)

        leave_btn = self.browser.find_element_by_xpath("//button[@type='submit']")
        leave_btn.click()

        self.assertEqual(self.browser.current_url, login_url + "?next=/hcap/")
