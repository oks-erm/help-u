import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# post
driver = webdriver.Chrome('./chromedriver')
driver.get("https://helpukr.herokuapp.com/")
if "Help U" not in driver.title:
    raise Exception("Unable to load the page!")

try:
    try:
        menu = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#navbar > i"))
        )
        menu.click()
    except:
        pass
    login = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#navbar > ul > li:nth-child(6) > a"))
    )
    login.click()
except:
    print('something went wrong (login)')
else:
    form_email = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "id_login"))
    )
    form_email.clear()
    form_email.send_keys("test1@test.com")
    form_email.send_keys(Keys.TAB)
    form_pass = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "id_password"))
    )
    form_pass.clear()
    form_pass.send_keys("qazqaz123")

    button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "body > div > div:nth-child(2) > div > div > div > form > div.d-grid.gap-2 > button"))
    )
    button.click()
    time.sleep(5)

    try:
        new_post = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "btn-success"))
        )
        new_post.click()
    except:
        print('something went wrong (new post)')
    else:
        try:
            time.sleep(2)
            form_title = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "id_title"))
            )
            form_title.send_keys(f"Selenium Title {random.randint(1, 100000)}")
            time.sleep(1)

            form_image = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "id_image"))
            )
            if driver.name == 'Safari':
                form_image.send_keys(
                        '/Users/test1/Documents/images/wallpaper1.jpg')
            else:
                form_image.send_keys(
                    'C:\\Users\\hello\\Documents\\images\\wallpaper1.jpg')

            time.sleep(2)
            form_country = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#id_country > option:nth-child(2)"))
            )
            form_country.click()
            time.sleep(1)

            time.sleep(2)
            form_city = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "id_city"))
            )
            form_city.send_keys("Selenium City")
            time.sleep(1)

            time.sleep(2)

            button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable(
                    (By.ID, "submit-id-save"))
            )
            
            form_type = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "id_type"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", form_type)
            time.sleep(0.2)
            form_type.click()
            time.sleep(1)
            form_choice = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#id_type > option:nth-child(2)"))
            )
            form_choice.click()

            form_category = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "id_category"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", form_category)
            form_category.click()
            time.sleep(1)
            form_choice_2 = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#id_category > option:nth-child(2)"))
            )
            form_choice_2.click()

            time.sleep(1)
            driver.execute_script("arguments[0].scrollIntoView();", button)
            button.click()
            time.sleep(1)

            return_value = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "search")))
            
            print(f"Success! {return_value is not None}")

        except:
            print("something went wrong (post form)")

driver.close()
