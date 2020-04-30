from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options

from hcap_institutions.models import HealthcareUnit
from hcap_accounts.models import HealthcareUnitNotifier
from hcap_geo.models import Region


class SeleniumTestCase(StaticLiveServerTestCase):
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


def create_test_user():
    user = get_user_model()()
    user.email = "jhon@doe.com"
    user.cpf = "715.769.900-10"
    user.name = "Jhon Doe"
    user.set_password("Secret#123")
    user.save()
    user.emailaddress_set.create(email=user.email, verified=True, primary=True)

    return user


def create_notifier_user():
    hu = create_healthcare_unit()
    user = create_test_user()
    hn = HealthcareUnitNotifier.objects.create(healthcare_unit=hu, user=user, is_authorized=True)
    hn.save()

    return hn


def create_location():
    city = Region.objects.create(name="city", code="CT")
    city.save()

    state = Region.objects.create(name="state", code="ST")
    state.save()

    country = Region.objects.create(name="country", code="CY")
    country.save()

    return (city, state, country)


def create_healthcare_unit():
    city, state, country = create_location()
    healthcare_unit = HealthcareUnit.objects.create(
        city=city,
        state=state,
        country=country,
        cnes_id="000",
        name="healthcare unit",
        is_active=True,
    )
    healthcare_unit.save()

    return healthcare_unit


def login(browser):
    login_input = browser.find_element_by_name("login")
    login_input.send_keys("jhon@doe.com")

    password_input = browser.find_element_by_name("password")
    password_input.send_keys("Secret#123")

    submit_btn = browser.find_element_by_xpath("//button[@type='submit']")
    submit_btn.click()


def signup(browser):
    name_input = browser.find_element_by_name("name")
    name_input.send_keys("Jhon Doe")

    cpf_input = browser.find_element_by_name("cpf")
    cpf_input.send_keys("715.769.900-10")

    email_input = browser.find_element_by_name("email")
    email_input.send_keys("jhon@doe.com")

    password1_input = browser.find_element_by_name("password1")
    password1_input.send_keys("Secret#123")

    password2_input = browser.find_element_by_name("password2")
    password2_input.send_keys("Secret#123")

    submit_btn = browser.find_element_by_xpath("//button[@type='submit']")
    submit_btn.click()
