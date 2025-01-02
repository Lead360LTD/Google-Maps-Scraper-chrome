from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException

filename = "data"
link = "https://www.google.com/maps/search/aesthetic+clinic+in+Windsor,+ON/@42.3149,-83.0364,12z"

browser = webdriver.Chrome()
record = []
e = []

def Selenium_extractor():
  le = 0
  action = ActionChains(browser)
  a = browser.find_elements(By.CLASS_NAME, "hfpxzc")

  while len(a) < 1000:
    print(len(a))
    var = len(a)
    scroll_origin = ScrollOrigin.from_element(a[len(a)-1])
    action.scroll_from_origin(scroll_origin, 0, 1000).perform()
    time.sleep(2)
    a = browser.find_elements(By.CLASS_NAME, "hfpxzc")

    if len(a) == var:
      le += 1
      if le > 5:
        print("No more new results found.")
        break
    else:
      le = 0

  for i in range(len(a)):
    scroll_origin = ScrollOrigin.from_element(a[i])
    action.scroll_from_origin(scroll_origin, 0, 100).perform()
    action.move_to_element(a[i]).perform()
    try:
      a[i].click()
    except ElementClickInterceptedException:
      browser.execute_script("arguments[0].click();", a[i])
    except NoSuchElementException:
      print("Element not found, skipping...")
      continue
    time.sleep(2)
    source = browser.page_source
    soup = BeautifulSoup(source, 'html.parser')
    try:
      Name_Html = soup.findAll('h1', {"class": "DUwDvf fontHeadlineLarge"})
      print(f"Names found: {len(Name_Html)}")

      if not Name_Html:
        print("No more names found, continuing to write data.")
        continue

      name = Name_Html[0].text
      if name not in e:
        e.append(name)
        divs = soup.findAll('div', {"class": "Io6YTe fontBodyMedium"})
        print(f"Details found: {len(divs)}")
        phone = "Not available"
        for j in range(len(divs)):
          if str(divs[j].text)[0] == "+":
            phone = divs[j].text

        Address_Html = divs[0]
        address = Address_Html.text
        website = "Not available"
        try:
          for z in range(len(divs)):
            if str(divs[z].text)[-4] == "." or str(divs[z].text)[-3] == ".":
              website = divs[z].text
        except:
          pass
        print([name, phone, address, website])
        record.append((name, phone, address, website))
    except Exception as e:
      print(f"Error processing element: {e}")
      continue

  df = pd.DataFrame(record, columns=['Name', 'Phone number', 'Address', 'Website'])
  df.to_csv(filename, index=False, encoding='utf-8')
  print(f"Data written to {filename}")

browser.get(str(link))
time.sleep(10)
Selenium_extractor()
