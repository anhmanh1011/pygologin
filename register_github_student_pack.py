import os
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import ImapMail
import Utils
from gologin import GoLogin

base_profile_path: str = r'D:\profiles'

username_email = 'marumgaymonc@hotmail.com'
passmail = 'W3zSQ792@hotmail.com'
username = 'marumgaymonc'
def scrap(profile):
    profile_path = os.path.join(base_profile_path, profile.get('name'))

    gl = GoLogin({
        "local": True,
        "credentials_enable_service": False,
        "profile_path": profile_path,
        "executable_path": r'D:browser\orbita-browser\chrome.exe',
        "port": profile['port'],

    })
    if not os.path.exists(profile_path):
        print('start create profile')
        gl.create({
            'name': profile.get('name'),
        })
        print('done profile success')

    debugger_address = gl.start()

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", debugger_address)
    driver = webdriver.Chrome(options=chrome_options)
    mainWindow = driver.current_window_handle;

    for handler in driver.window_handles:
        if not handler.__eq__(mainWindow):
            driver.switch_to.window(handler)
            driver.close()
    driver.switch_to.window(mainWindow)

    driver.get("https://education.github.com/discount_requests/application")

    time.sleep(3)
    if driver.current_url.__contains__('/login'):

        Utils.wait_util(driver, By.ID, 'login_field', 10).send_keys(username_email)
        Utils.wait_util(driver, By.ID, 'password', 10).send_keys('Anhmanhbu8' + Keys.ENTER)
        time.sleep(3)
        if driver.current_url.__contains__('/verified-device'):
            code = ImapMail.get_code_from_mail(username_email, passmail, r'(\d{6})')
            print('code:' + code) 
            Utils.wait_util(driver, By.ID, 'otp', 10).send_keys('code' + Keys.ENTER)

    time.sleep(5)

    if driver.current_url.__contains__('/discount_requests/application'):
        driver.get("https://github.com/" + username)
        time.sleep(3)
        Utils.wait_util(driver, By.XPATH,
                        '/html/body/div[1]/div[6]/main/div/div/div[1]/div/div/div[3]/div[2]/div[2]/button', 10).click()
        time.sleep(1)
        Utils.wait_util(driver, By.ID, 'user_profile_name', 10).clear()
        Utils.wait_util(driver, By.ID, 'user_profile_name', 10).send_keys(username+' roy')

        Utils.wait_util(driver, By.ID, 'user_profile_bio', 10).clear()
        Utils.wait_util(driver, By.ID, 'user_profile_bio', 10).send_keys('student')
        Utils.wait_util(driver, By.XPATH,
                        '/html/body/div[1]/div[6]/main/div/div/div[1]/div/div/div[3]/div[1]/waiting-form/form/div[9]/button[1]',
                        10).click()
        time.sleep(2)

    driver.get("https://education.github.com/discount_requests/application")
    if driver.current_url.__contains__('discount_requests/application'):
        Utils.wait_util(
            driver, By.XPATH,
            '/html/body/div/main/div/div/div[1]/div/div[4]/div/form/div[1]/fieldset/div/div[1]/div/label/div'
            , 5).click()
        time.sleep(1)

        Utils.wait_util(
            driver, By.XPATH,
            "/html/body/div/main/div/div/div[1]/div/div[4]/div/form/div[1]/div[5]/div/auto-complete/input"
            , 5).send_keys("Ananda Mohan College")

        time.sleep(2)

        Utils.wait_util(
            driver, By.XPATH, "/html/body/div/main/div/div/div[1]/div/div[4]/div/form/div[2]/textarea"
            , 5).send_keys("for learn")

        driver.find_element(By.XPATH, '/html/body/div/main/div/div/div[1]/div/div[4]/div/form/div[4]/input').click()

        time.sleep(3)

    if driver.current_url.__contains__('additional_information'):
        print('keo anh vaooooooooooooo ====== ')
        time.sleep(1000)

    # time.sleep(10)

    # driver.quit()
    # time.sleep(10)
    # gl.stop()


profiles = [
    {'name': 'profile_id_1', 'profile_path': r'D:\profiles\manh_test1', 'port': 3500},
    {'name': 'profile_id_2', 'profile_path': r'D:\profiles\manh_test2', 'port': 3501},
    {'name': 'profile_id_3', 'profile_path': r'D:\profiles\manh_test3', 'port': 3502},

]
if __name__ == '__main__':
    # with Pool(3) as p:
    #     p.map(scrap, profiles)
    #
    # os.system('taskkill /im chrome.exe /f')
    # os.system('taskkill /im chromedriver.exe /f')
    profile = {'name': 'profile_id_106', 'port': 3500}

    scrap(profile)
