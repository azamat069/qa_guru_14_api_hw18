import os
import allure
import pytest
import requests
from selene import browser
from dotenv import load_dotenv


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="session")
def browser_manager():
    browser.config.base_url = os.getenv('URL')
    browser.config.window_width = 1600
    browser.config.window_height = 1080

    yield
    browser.quit()


@pytest.fixture(scope="session")
def auth_cookie():
    with allure.step('Получаем авторизационный куки'):
        data = {"Email": os.getenv('LOGIN'), "Password": os.getenv("PASSWORD")}
        response = requests.post(os.getenv('URL') + 'login', data=data, allow_redirects=False)
        assert response.status_code == 302
        auth_cookie = response.cookies.get("NOPCOMMERCE.AUTH")
        return auth_cookie
