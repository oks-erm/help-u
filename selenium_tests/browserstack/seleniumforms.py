import random
import uuid
import time
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver


#######################################################
# configure the environment following the instructions on
# https: // www.browserstack.com/
# credentials are included in the submission message
# then run this file
# `browserstack-sdk python3 selenium_tests/browserstack/seleniumforms.py`
#######################################################

# you can't read from a file or an environmental
# variable while running on browser stack, so
# paste password here
PASSWORD = "PASTE PASSWORD HERE"


# contact form
driver = webdriver.Chrome('./chromedriver')
driver.get("https://helpukr.herokuapp.com/")
if "Help U" not in driver.title:
    raise Exception("Unable to load the page!")

try:
    form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "contact-form"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", form)
except:
    print('something went wrong contact-form')
else:
    form_name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "name"))
    )
    form_email = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    form_subject = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "subject"))
    )
    form_message = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "message"))
    )

    # Sending input
    form_name.clear()
    form_name.send_keys("Selenium Test Name")
    time.sleep(1)
    form_subject.send_keys(Keys.TAB)
    form_email.clear()
    form_email.send_keys("test@example.com")
    time.sleep(1)
    form_subject.send_keys(Keys.TAB)
    form_subject.clear()
    form_subject.send_keys("Selenium Test subject")
    time.sleep(1)
    form_subject.send_keys(Keys.TAB)
    form_message.clear()
    form_message.send_keys("Selenium Test message text")

    # Submitting the form
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#contact > div > div.container-fluid.col-lg-8.mt-5.mt-lg-0 > form > div.text-center > button')))
    time.sleep(1)
    driver.execute_script("arguments[0].scrollIntoView();", submit_button)
    time.sleep(1)
    submit_button.click()

    # Printing the result
    return_value = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sent-message")))
    time.sleep(3)
    print(f"Success! {return_value.text}")

driver.close()


TEST_COMMENT = str(uuid.uuid4)


# comment
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
    form_pass.send_keys(PASSWORD)
    button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "body > div > div:nth-child(2) > div > div > div > form > div.d-grid.gap-2 > button"))
    )
    button.click()
    time.sleep(5)

    try:
        post = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#listings > div > div > div:nth-child(1) > div > div > a > h4"))
        )
        post.click()
    except:
        print('something went wrong (post)')
    else:
        time.sleep(2)
        button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "btn-success"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", button)
        time.sleep(1)
        button.click()
        time.sleep(1)
        publish = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#comment > div > form > div.text-end > button"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", publish)

        try:
            text = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.ID, "body"))
            )
            text.send_keys(TEST_COMMENT)
            publish.click()
            time.sleep(2)

            return_value = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#comments-block > div.card.border-0.comment > div > div.col-9 > div > p.card-text.text-muted.mb-1"))
            )

            print(f"Success! {return_value.text}")
        except:
            print("something went wrong (text field)")

driver.close()


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
    form_pass.send_keys(PASSWORD)
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
            driver.execute_script(
                "arguments[0].scrollIntoView();", form_category)
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
            time.sleep(3)

            return_value = WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.ID, "search")))

            print(f"Success! {return_value is not None}")

        except:
            print("something went wrong (post form)")

driver.close()


# profile form
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
    form_pass.send_keys(PASSWORD)
    button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "body > div > div:nth-child(2) > div > div > div > form > div.d-grid.gap-2 > button"))
    )
    button.click()
    time.sleep(5)

    try:
        user_name = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#user-name > a"))
        )
        user_name.click()
    except:
        print('something went wrong (user_name)')
    else:
        time.sleep(5)
        try:
            edit = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    # (By.CSS_SELECTOR, "#profile > div > div > div.col-xl-8.col-lg-7 > h2 > a"))
                    (By.CLASS_NAME, "bx-pencil"))
            )
            edit.click()
        except:
            print('something went wrong (edit)')
        else:
            time.sleep(3)
            city = WebDriverWait(driver, 8).until(
                EC.presence_of_element_located(
                    (By.ID, "id_city"))
            )
            city.send_keys('+1')
            time.sleep(3)

            save_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.ID, "submit-id-save"))
            )
            driver.execute_script(
                "arguments[0].scrollIntoView();", save_button)
            time.sleep(1)
            save_button.click()
            time.sleep(5)

            return_value = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#profile > div > div > div.col-xl-8.col-lg-7 > p"))
            )

            print(f"Success! {return_value.text.split(',')[1]}")

driver.close()


# sign in
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
    form_pass.send_keys(PASSWORD)
    button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "body > div > div:nth-child(2) > div > div > div > form > div.d-grid.gap-2 > button"))
    )
    button.click()
    time.sleep(5)

    # Printing the result
    return_value = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "search")))
    print(f"Success! {return_value is not None}")

driver.close()


# sign up
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
    register = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#navbar > ul > li:nth-child(5) > a"))
    )
    register.click()
except:
    print('something went wrong (register)')
else:
    form_email = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "id_email"))
    )
    form_email.clear()
    form_email.send_keys(f"test{random.randint(1, 100000)}@test.com")
    form_email.send_keys(Keys.TAB)

    form_fname = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.ID, "id_first_name"))
    )
    form_fname.clear()
    form_fname.send_keys("Sele")
    form_fname.send_keys(Keys.TAB)

    form_lname = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.ID, "id_last_name"))
    )
    form_lname.clear()
    form_lname.send_keys("Nium")
    form_lname.send_keys(Keys.TAB)

    form_pass1 = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.ID, "id_password1"))
    )
    form_pass1.clear()
    form_pass1.send_keys("qazqaz123")
    form_pass1.send_keys(Keys.TAB)

    form_pass2 = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.ID, "id_password2"))
    )
    form_pass2.clear()
    form_pass2.send_keys("qazqaz123")

    button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#signup_form > div.d-grid.gap-2 > button"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", button)
    time.sleep(1)
    button.click()
    time.sleep(5)

    # Printing the result
    return_value = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".login-block > div.row > div > h1")))
    print(f"Success! {return_value.text}")

driver.close()
