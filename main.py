from scraping import Scraping
import constants

scraping = Scraping()
scraping.fetch_url(constants.PORTAL_URL)
scraping.login(constants.username, constants.password)
scraping.click_student_results()
scraping.click_questionnaire()
scraping.switch_to_questionnaire_tab()
scraping.rate_all_subjects()
scraping.close_webdriver()