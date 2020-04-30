from django.urls import reverse

from .base import SeleniumTestCase, create_test_user, create_notifier_user, login

class LoginTestCase(SeleniumTestCase):

    def test_first_login(self):
        url = f"{self.live_server_url}{reverse('account_login')}"
        self.browser.get(url)
        
        user = create_test_user()

        login_input = self.browser.find_element_by_name('login')
        login_input.send_keys('jhon@doe.com')
        
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys('Secret#123')
        
        submit_btn = self.browser.find_element_by_xpath("//button[@type='submit']")
        submit_btn.click()

        after_login_url = f"{self.live_server_url}/hcap/request-authorization/"
        self.assertEqual(self.browser.current_url, after_login_url)

        cnes_input = self.browser.find_element_by_id('id_cnes_id')
        self.assertTrue(cnes_input)
        
        select_state = self.browser.find_element_by_id('id_state')
        self.assertTrue(select_state)
