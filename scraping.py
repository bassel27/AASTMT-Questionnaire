from re import sub
from ssl import OPENSSL_VERSION_NUMBER
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import constants


class Scraping:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def fetch_url(self, url):
        self.driver.get(url)

    def send_username(self, username):
        username_field = self.driver.find_element(
            By.XPATH, '//input[@placeholder="Registration Number"]'
        )
        username_field.send_keys(username)

    def send_password(self, password):
        password_field = self.driver.find_element(
            By.XPATH, '//input[@placeholder="Pin Code"]'
        )
        password_field.send_keys(password)

    def click_login(self):
        login_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')
        login_button.click()

    def login(self, username, password):
        self.send_username(username)
        self.send_password(password)
        self.click_login()

    def click_student_results(self):
        cards = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//h5[@class="card-title text-center"]')
            )
        )
        for card in cards:
            if card.text == "Student Results":
                break
        card.click()

    def click_questionnaire(self):
        try:
            questionnaire_button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//a[@onclick="SubmitQuestionaire()"]')
                )
            )
            questionnaire_button.click()
        except:
            print("Questionnaire not present")

    def switch_to_questionnaire_tab(self):
        questionnaire_tab = self.driver.window_handles[1]
        self.driver.switch_to.window(questionnaire_tab)

    def get_subjects_list(self):
        subjects = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//input[@title="تفاصيل"]'))
        )
        return subjects

    def open_subject(self, subject_element):
        subject_element.click()

    def answer_questionnaire(self):
        radio_buttons = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, constants.RADIO_BUTTONS["متوسط"])
            )
        )
        for radio_button in radio_buttons:
            radio_button.click()

    def submit_questionnaire(self):
        submit_button = self.driver.find_element(By.XPATH, '//input[@name="btn_Save"]')
        submit_button.click()

    def rate_all_subjects(self):
        number_of_subjects = len(self.get_subjects_list())
        for c in range(number_of_subjects):
            subject_elements = self.get_subjects_list()     # refresh because list is lost after change (stale elements)
            self.open_subject(subject_elements[c])
            self.answer_questionnaire()
            self.submit_questionnaire() #edit

    def close_webdriver(self):
        self.driver.quit()


