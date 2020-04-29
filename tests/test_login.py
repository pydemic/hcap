from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options

from hcap_accounts.models.user import User 


class LoginTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        # options.headless = True
        cls.browser = WebDriver(options=options)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_first_login(self):
        url = f"{self.live_server_url}{reverse('account_login')}"
        self.browser.get(url)
        
        user = get_user_model()()
        user.email = 'jhon@doe.com'
        user.cpf = '715.769.900-10'
        user.name = 'Jhon Doe' 
        user.set_password('Secret#123')
        
        user.save()
        user.emailaddress_set.create(email=user.email, verified=True, primary=True)

        login_input = self.browser.find_element_by_name('login')
        login_input.send_keys('jhon@doe.com')
        
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys('Secret#123')
        
        submit_btn = self.browser.find_element_by_xpath("//button[@type='submit']")
        submit_btn.click()

        cnes_input = self.browser.find_element_by_id('id_cnes_id')
        self.assertTrue(cnes_input)
