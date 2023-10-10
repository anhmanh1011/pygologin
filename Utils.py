import poplib
import re
import traceback

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import visibility_of_element_located, element_to_be_clickable
from selenium.webdriver.support.wait import WebDriverWait


def go_to_url(driver: WebDriver, url: str):
    driver.get(url)


def wait_util(driver: WebDriver, by: str, element: str, time_wait: int) -> WebElement:
    return WebDriverWait(driver, time_wait).until(
        visibility_of_element_located((by, element)))


def wait_util_clickable(driver: WebDriver, by: str, element: str, time_wait: int) -> WebElement:
    return WebDriverWait(driver, time_wait).until(
        element_to_be_clickable((by, element)))


def get_code_from_mail(email_username: str, email_password: str) -> str:
    try:
        email = email_username
        password = email_password
        pop3_server = "outlook.office365.com"
        server = poplib.POP3_SSL(pop3_server, 995)

        # ssl加密后使用
        # server = poplib.POP3_SSL('pop.163.com', '995')
        print(server.set_debuglevel(1))  # 打印与服务器交互信息
        print(server.getwelcome())  # pop有欢迎信息
        server.user(email)
        server.pass_(password)
        print('Messages: %s. Size: %s' % server.stat())
        print(email + ": successful")
        num_messages = len(server.list()[1])
        result: str = ''
        for i in range(num_messages):
            # get the message at index i
            message_lines = server.retr(i + 1)[1]
            # join the message lines into a single string
            message_text = b'\n'.join(message_lines)
            # print draw
            raw_text: str = message_text.decode('utf-8')
            # parse the message text into an email object
            message = email_parse.message_from_bytes(message_text)
            # print the subject and sender of the message
            date = message.get("Date")
            sub: str = message["subject"]
            sender: str = message["from"]
            print(f'Subject: {sub}')
            print(f'From: {sender}')
            print(f'date: {date}')

            if sender.__contains__('noreply@github.com'):
                # and sub.__contains__('Please verify your device'):
                # Create a regular expression pattern to match the text pattern.
                pattern = r'Verification code: (\d{6})'

                # Use the re.search() function to search for the pattern in the email.
                match = re.search(pattern, raw_text)

                # If the pattern is found, extract the 6 digits after it.
                if match:
                    print(raw_text)
                    result = match.group(1)
                # result = re.findall("[0-9]{6}", content)[0]
        print("code: " + result)
        return result
    except Exception as ex:
        print(ex)
        traceback.print_exc()
        return ''
