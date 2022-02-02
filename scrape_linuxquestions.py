from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import csv

__author__ = 'Deepankara Reddy'


# ---------- constants: ----------
BASE_URL = 'https://www.linuxquestions.org/questions/linux-software-2/'
CSV_COL_NAMES = ['title', 'description', 'url', 'date']


# ---------- functions: ----------
def write_to_file(rows):
    with open('scraped_questions.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(CSV_COL_NAMES)
        writer.writerows(rows)


# ---------- main: ----------
if __name__ == '__main__':
    # initialize Selenium:
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--private")
    driver = webdriver.Firefox(options=firefox_options)

    # software questions page:
    driver.get(BASE_URL)
    WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.CSS_SELECTOR, '.pagenav'))

    # we find a list of forum threads in `.find_elements()` (n.b. plural name):
    threads = driver.find_elements(By.CSS_SELECTOR, '#threadslist a[id^="thread_title"]')
    links = [(thread.get_attribute('href'), thread.text) for thread in threads]

    # scrape every thread on the page:
    data = []
    for url, title in links:
        driver.get(url)
        WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.ID, 'posts'))

        post = driver.find_element(By.CSS_SELECTOR, '#posts table[id^="post"]')
        description = post.find_element(By.CSS_SELECTOR, 'div[id^="post_message"]').text
        date = post.find_element(By.CSS_SELECTOR, '.thead').text
        data.append([title, description, url, date])

        driver.back()

    write_to_file(data)

    driver.quit()
