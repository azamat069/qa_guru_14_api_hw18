import json
import allure
import os
import requests
from allure_commons.types import AttachmentType, Severity
from selene import browser, have, be


@allure.tag('Web')
@allure.severity(Severity.CRITICAL)
@allure.feature('Корзина')
@allure.story('Добавление товара в корзину')
def test_add_item_to_cart(auth_cookie, browser_manager):
    authorization_cookie = {"NOPCOMMERCE.AUTH": auth_cookie}
    with allure.step('Добавляем товар "Build your own expensive computer" в корзину'):
        data = {
            "product_attribute_74_5_26": 81,
            "product_attribute_74_6_27": 83,
            "product_attribute_74_3_28": 86,
            "addtocart_74.EnteredQuantity": 1
        }
        response_add_item = requests.post(os.getenv('URL') + 'addproducttocart/details/74/1', data=data,
                                          cookies=authorization_cookie)
        allure.attach(body=str(response_add_item.cookies), name="Cookies", attachment_type=AttachmentType.TEXT,
                      extension="txt")
        allure.attach(body=json.dumps(response_add_item.json(), indent=4, ensure_ascii=True), name="Response",
                      attachment_type=AttachmentType.JSON, extension="json")
    with allure.step('Добавляем авторизационный куки в браузер'):
        browser.open(os.getenv('URL')).driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": auth_cookie})
        browser.open(os.getenv('URL') + 'cart')
    with allure.step('Проверяем что пользователь авторизован'):
        browser.element('[class="account"]').should(have.text(os.getenv('LOGIN')))
    with allure.step('Проверяем что товар добавилен в корзину'):
        browser.element('[href="/build-your-own-expensive-computer-2"]').should(be.enabled)


@allure.tag('Web')
@allure.severity(Severity.CRITICAL)
@allure.feature('Корзина')
@allure.story('Добавление нескольких товаров в корзину')
def test_add_few_items_to_cart(auth_cookie, browser_manager):
    authorization_cookie = {"NOPCOMMERCE.AUTH": auth_cookie}
    with allure.step('Добавляем товар "Computing and Internet" в корзину'):
        data = {"addtocart_13.EnteredQuantity": 5}
        response_add_item = requests.post(os.getenv('URL') + 'addproducttocart/details/13/1', data=data,
                                          cookies=authorization_cookie)
        allure.attach(body=str(response_add_item.cookies), name="Cookies", attachment_type=AttachmentType.TEXT,
                      extension="txt")
        allure.attach(body=json.dumps(response_add_item.json(), indent=4, ensure_ascii=True), name="Response",
                      attachment_type=AttachmentType.JSON, extension="json")
    with allure.step('Добавляем авторизационный куки в браузер'):
        browser.open(os.getenv('URL')).driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": auth_cookie})
        browser.open(os.getenv('URL') + 'cart')
    with allure.step('Проверяем что пользователь авторизован'):
        browser.element('[class="account"]').should(have.text(os.getenv('LOGIN')))
    with allure.step('Проверяем что товар добавилен в корзину в количесте 5шт.'):
        browser.element('[href="/computing-and-internet"]').should(be.enabled)
