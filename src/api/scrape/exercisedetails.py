from selenium import webdriver

class Driver():
  def __init__(self):
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:\\Users\\Dennis Phun\\AppData\\Local\\Google\\Chrome\\User Data")
    options.add_argument("profile-directory=Default")
    self.driver = webdriver.Chrome(options=options)

  def close(self):
    self.driver.close()

  def get_info(self, url=""):
    self.driver.get(url)
    info = {}
    info['rating'] = self.driver.find_element("xpath", "//div[@class='ExRating-badge']").text
    info['name'] = self.driver.find_element("xpath", "//div[@class='grid-8 grid-12-s grid-12-m']/h1").text
    instructions = self.driver.find_elements("xpath", "//div[@class='grid-8 grid-12-s grid-12-m']/ol/li")
    info['instructions'] = [x.text for x in instructions]
    info['type'] = self.driver.find_element("xpath", "//div[@class='grid-3 grid-12-s grid-8-m']//li[contains(text(), 'Type')]/a").text
    info['muscle'] = self.driver.find_element("xpath", "//div[@class='grid-3 grid-12-s grid-8-m']//li[contains(text(), 'Main Muscle Worked')]/a").text
    try:
      info['equipment'] = self.driver.find_element("xpath", "//div[@class='grid-3 grid-12-s grid-8-m']//li[contains(text(), 'Equipment')]/a").text
    except:
      info['equipment'] = 'n/a'
    info['level'] = self.driver.find_element("xpath", "//div[@class='grid-3 grid-12-s grid-8-m']//li[contains(text(), 'Level')]").text.split(":")[1].strip()
    return info


exercises = []
exercise_details = []

with open('exercises.txt', 'r') as file, open('exercisedetails.txt', 'a') as file2:
  exercises = [tuple(line.strip().split(', ')) for line in file]
  driver = Driver()
  
  for i in range(319,len(exercises)):
    exercise = exercises[i]
    try:
      info = driver.get_info(exercise[1])
      if info:
        file2.write(f"{info['name']}, {info['rating']}, {info['instructions']}, {info['type']}, {info['muscle']}, {info['equipment']}, {info['level']}\n")
        print(f"{i}: success")
    except Exception as e:
      print(f"{i}: fail")
      print(e)
      break
  
  driver.close()