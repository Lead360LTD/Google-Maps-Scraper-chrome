from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException

filename = "data.csv"
link = "https://www.google.com/maps/search/aesthetic+clinic+in+Windsor,+ON/@42.3149,-83.0364,12z"

browser = webdriver.Chrome()
record = []
processed_names = set()  # Use a set to track processed names

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
      # Extract business name
      name_html = soup.find('h1', {"class": "DUwDvf lfPIob"})
      name = name_html.text if name_html else "Not available"
      print(f"Name: {name}")

      if name not in processed_names:
        processed_names.add(name)
        
        # Extract phone number and address
        divs = soup.findAll('div', {"class": "Io6YTe fontBodyMedium kR99db fdkmkc"})
        phone = "Not available"
        address = "Not available"

        for div in divs:
          text = div.text
          if text.startswith("+"):
            phone = text
          elif "," in text:  # Assuming address contains commas
            address = text

        # Extract website
        website_html = soup.find('a', {"class": "CsEnBe"})
        website = website_html['aria-label'].replace("Website: ", "") if website_html else "Not available"

        print(f"Scraped: {name}, {phone}, {address}, {website}")
        record.append([name, phone, address, website])
    except Exception as e:
      print(f"Error processing element: {e}")
      continue

  # Write data to CSV
  with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Phone number', 'Address', 'Website'])
    writer.writerows(record)
  print(f"Data written to {filename}")

browser.get(str(link))
time.sleep(10)
Selenium_extractor()
browser.quit()
