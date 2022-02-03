from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import csv

__author__ = 'Deepankara Reddy'


# ---------- constants: ----------
BASE_URL = 'https://www.linuxquestions.org/questions/linux-software-2/'
CSV_COL_NAMES = ['title', 'description', 'url', 'date']
FILE_NAME = 'scraped_questions.csv'


# ---------- helper functions: ----------
def create_file():
    with open(FILE_NAME, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(CSV_COL_NAMES)


def append_to_file(rows):
    with open(FILE_NAME, 'a') as file:
        writer = csv.writer(file)
        writer.writerows(rows)


# ---------- main: ----------
if __name__ == '__main__':
    # initialize Selenium:
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--private")
    driver = webdriver.Firefox(options=firefox_options)

    create_file()

    # goto "overview" page (a listing of posts), then begin scraping logic:
    driver.get(BASE_URL)
    while True:
        WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.CSS_SELECTOR, '.pagenav'))
        back_url = driver.current_url

        # we find a list of forum threads:
        # n.b. use of plural `.find_elements` rather than `find_element`:
        threads = driver.find_elements(By.CSS_SELECTOR, '#threadslist a[id^="thread_title"]')
        thread_links = [(thread.get_attribute('href'), thread.text) for thread in threads]

        # scrape every thread on the page:
        data = []
        for thread_url, title in thread_links:
            driver.get(thread_url)
            WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.ID, 'posts'))

            post = driver.find_element(By.CSS_SELECTOR, '#posts table[id^="post"]')
            description = post.find_element(By.CSS_SELECTOR, 'div[id^="post_message"]').text
            date = post.find_element(By.CSS_SELECTOR, '.thead').text
            data.append([title, description, thread_url, date])

        append_to_file(data)

        # go back to questions page:
        driver.get(back_url)
        WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.CSS_SELECTOR, '.pagenav'))
        # n.b. use of plural `.find_elements` -- the singular `.find_element` will throw an error if element not found:
        next_buttons = driver.find_elements(By.CSS_SELECTOR, '.pagenav a[rel="next"]')

        # if we can't find any "next" pagination buttons, then we reached the end of the threads;
        # otherwise, go to next page:
        if next_buttons:
            next_buttons[0].click()
        else:
            break

    print('--- finished scraping successfully ---')
    driver.quit()
