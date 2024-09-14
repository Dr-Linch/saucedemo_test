import os.path
import time
import os

from dotenv import load_dotenv

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

load_dotenv(os.path.join('.', '.env'))


def by_test():
    user = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={user.chrome}')

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url='https://www.saucedemo.com/')
        time.sleep(5)

        login_input = driver.find_element(By.ID, 'user-name')
        login_input.clear()
        login_input.send_keys(os.getenv('USER_LOGIN'))
        time.sleep(2)

        password_input = driver.find_element(By.ID, value='password')
        password_input.clear()
        password_input.send_keys(os.getenv('USER_PASSWORD'))
        time.sleep(2)
        password_input.send_keys(Keys.ENTER)

        time.sleep(10)

        all_items = driver.find_elements(By.CLASS_NAME, 'inventory_item_description')
        for item in all_items:
            item_title = item.find_element(By.CLASS_NAME, 'inventory_item_name').text

            if item_title == os.getenv('ITEM_TITLE'):
                item.find_element(By.XPATH, '//button[@class="btn btn_primary btn_small btn_inventory "]').click()
                break

        time.sleep(2)

        shop_card = driver.find_element(By.CLASS_NAME, 'shopping_cart_link')
        shop_card.click()
        time.sleep(5)

        my_item = driver.find_element(By.CLASS_NAME, 'cart_item')
        my_item_title = my_item.find_element(By.CLASS_NAME, 'inventory_item_name')
        if my_item_title.text == os.getenv('ITEM_TITLE'):
            checkout = driver.find_element(By.ID, 'checkout')
            checkout.click()

            input_first_name = driver.find_element(By.ID, 'first-name')
            input_first_name.clear()
            input_first_name.send_keys(os.getenv('USER_FIRST_NAME'))
            time.sleep(2)

            input_last_name = driver.find_element(By.ID, 'last-name')
            input_last_name.clear()
            input_last_name.send_keys(os.getenv('USER_LAST_NAME'))
            time.sleep(2)

            input_postal_code = driver.find_element(By.ID, 'postal-code')
            input_postal_code.clear()
            pc = os.getenv('USER_POSTAL_CODE')

            if pc != '':
                input_postal_code.send_keys(pc)
            else:
                input_postal_code.send_keys('12345-6789')

            btn_continue = driver.find_element(By.ID, 'continue')
            btn_continue.click()
            time.sleep(5)

            btn_finished = driver.find_element(By.ID, 'finish')
            btn_finished.click()
            time.sleep(5)

            complete_h = driver.find_element(By.CLASS_NAME, 'complete-header')
            if complete_h.text != 'Thank you for your order!':
                raise Exception()

            back_to_products = driver.find_element(By.ID, 'back-to-products')
            back_to_products.click()
            time.sleep(5)

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    by_test()
