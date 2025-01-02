Clone the Repository
Open a terminal or command prompt and run the following commands:

bash
Copy code
git clone https://github.com/Lead360LTD/Scraper.git
cd Scraper
Install ChromeDriver

Download the appropriate version of ChromeDriver for your installed Chrome browser version from ChromeDriver Downloads.
Extract the downloaded file and move chromedriver.exe to your C:\Windows\System32 directory to ensure it's accessible from anywhere in the terminal.
Install Required Python Libraries
Use pip to install the necessary libraries:

bash
Copy code
pip install beautifulsoup4 pandas selenium
Run the Script
Execute the scraping script to start gathering data:

bash
Copy code
python google_maps_scraper.py



Key Features
Automated Navigation: Uses Selenium WebDriver to interact with Google Maps dynamically.
Web Scraping Power: Leverages BeautifulSoup to parse and extract data from HTML.
Error Handling: Includes mechanisms to handle common exceptions, such as elements not being clickable or not found.
Data Output: Saves the scraped data into a well-structured Pandas DataFrame, which can then be exported to CSV or other formats.
Requirements
Python 3.7 or higher
Libraries:
selenium
beautifulsoup4
pandas
time
Browser and WebDriver:
Google Chrome (or other supported browsers)
Corresponding WebDriver (e.g., chromedriver)
How It Works
Initialize Selenium WebDriver: The script launches a browser instance to interact with Google Maps.
Perform Search Queries: Specify search terms like "restaurants in New York" to fetch results.
Scroll and Navigate: Utilizes automated scrolling to load additional results and handle pagination.
Parse Data: Extracts business details from the loaded results using both Selenium and BeautifulSoup.
Save Results: Outputs the collected data into a CSV or other desired formats.
