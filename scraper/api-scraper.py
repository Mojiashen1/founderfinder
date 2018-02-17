# from linkedin_scraper import Person
from selenium import webdriver
from linkedin_scraper import Person, Experience, Education
from linkedin_scraper.functions import time_divide

from selenium.common.exceptions import NoSuchElementException

from collections import namedtuple

class Related(Person):
    def __init__(self, linkedin_url = None, experiences = [], educations = [], driver = None, scrape = True, related = [], depth=0):
        # super().__init__(linkedin_url, experiences, educations, driver, scrape=False)
        self.linkedin_url = linkedin_url
        self.experiences = experiences
        self.educations = educations
        self.related = related
        self.depth = depth

        if driver is None:
            try:
                if os.getenv("CHROMEDRIVER") == None:
                    driver_path = os.path.join(os.path.dirname(__file__), 'drivers/chromedriver')
                else:
                    driver_path = os.getenv("CHROMEDRIVER")

                
                options = webdriver.ChromeOptions()
                options.add_argument("--incognito") # open in incognito
                driver = webdriver.Chrome(driver_path, chrome_options=options)
            except:
                options = webdriver.ChromeOptions()
                options.add_argument("--incognito") # open in incognito
                driver = webdriver.Chrome(chrome_options=options)

        driver.get(linkedin_url)
        self.driver = driver

        if scrape:
            self.scrape(True)

    def add_related(self, url):
        self.related.append(url)

    def scrape(self, close_on_complete=True):
        self.scrape_not_logged_in(close_on_complete=close_on_complete)
            

    def scrape_not_logged_in(self, close_on_complete=True, retry_limit = 10):
        driver = self.driver
        retry_times = 0
        while self.is_signed_in() and retry_times <= retry_limit:
            page = driver.get(self.linkedin_url)
            retry_times = retry_times + 1


        # get name
        self.name = driver.find_element_by_id("name").text

        # get experience
        try:
            exp = driver.find_element_by_id("experience")
            for position in exp.find_elements_by_class_name("position"):
                position_title = position.find_element_by_class_name("item-title").text
                company = position.find_element_by_class_name("item-subtitle").text

                try:
                    times = position.find_element_by_class_name("date-range").text
                    from_date, to_date, duration = time_divide(times)
                except:
                    from_date, to_date = (None, None)
                experience = Experience( position_title = position_title , from_date = from_date , to_date = to_date)
                experience.institution_name = company
                self.add_experience(experience)
        except NoSuchElementException:
            pass

        try:
            # get education
            edu = driver.find_element_by_id("education")
            for school in edu.find_elements_by_class_name("school"):
                university = school.find_element_by_class_name("item-title").text
                degree = school.find_element_by_class_name("original").text
                try:
                    times = school.find_element_by_class_name("date-range").text
                    from_date, to_date, duration = time_divide(times)
                except:
                    from_date, to_date = (None, None)
                education = Education(from_date = from_date, to_date = to_date, degree=degree)
                education.institution_name = university
                self.add_education(education)
        except NoSuchElementException:
            pass

        try:
            # get related
            related = driver.find_element_by_class_name("browse-map--swapped")
            for person in related.find_elements_by_class_name("profile-card"):
                url = person.find_element_by_tag_name('a').get_attribute('href')
                self.add_related(url)
        except NoSuchElementException:
            pass

        # get
        if close_on_complete:
            driver.close()

        for r in self.related:
            new_persons = Related(r, depth=self.depth+1)

def main():
    SEEDS = ['radhikaemens', 'anqi-lu-5aa507a8', 'kishanemens']
    URLS = ['https://www.linkedin.com/in/' + name for name in SEEDS]

    for url in URLS:
        person = Related(url, depth = 0)

def open_browser(url):
    return p


if __name__ == '__main__':
    main()

# from selenium import webdriver
# from bs4 import BeautifulSoup as soup
#
# browser = webdriver.Chrome()
# # browser.add_argument("--incognito")
# browser.get("https://www.linkedin.com/in/radhikaemens")
# page = soup(browser.page_source, "html5lib")
# people = page.find_all('li', {'class': 'profile-card'})
# for p in people:
#     print(p)
# while 1 == 1:
#     pass