from selenium import webdriver
import time

class Driver():
  def __init__(self, muscle):
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:\\Users\\Dennis Phun\\AppData\\Local\\Google\\Chrome\\User Data")
    options.add_argument("profile-directory=Default")
    self.driver = webdriver.Chrome(options=options)
    self.url = f"https://www.bodybuilding.com/exercises/finder?muscle={muscle}"
    self.page = 0

  def start(self):
    self.driver.get(self.url)

  def close(self):
    self.driver.close()

  def load_more(self):
    element = self.driver.find_element("xpath", "//button[@class='bb-flat-btn bb-flat-btn--size-lg js-ex-loadMore ExLoadMore-btn']")
    self.driver.execute_script('arguments[0].scrollIntoView();', element)
    time.sleep(1)
    self.driver.execute_script('window.scrollBy(0, -100)', element)
    time.sleep(1)
    element.click()
    self.page += 1
    time.sleep(1)

  def process_page(self):
    result = []
    elements = self.driver.find_elements("xpath", "//div[@class='ExResult-row  flexo-container flexo-between']")
    for element in elements:
        rating = element.find_element("xpath", "./div[3]/div/div[1]").text
        if rating != 'n/a' and float(rating) >= 3:
          subelement = element.find_element("xpath", "./div[2]/h3/a")
          result.append((subelement.text, subelement.get_attribute('href')))
    return result


muscles = ["hamstrings", "calves", "triceps", "traps", "shoulders", "abdominals", "glutes", "biceps", "adductors", "abductors"]

for muscle in muscles: 
  driver = Driver(muscle=muscle)
  driver.start()

  exercises = []

  while True:
    try:
      driver.load_more()
    except Exception as e:
      break

  time.sleep(1)
  exercises += driver.process_page()

  driver.close()
  with open('exercises.txt', 'a') as file:
    for exercise in exercises:
      file.write(f"{exercise[0]}, {exercise[1]}\n")