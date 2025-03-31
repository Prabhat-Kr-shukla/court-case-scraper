# Court Case Scraper

This is a Python-based web scraper that extracts court case details from the Dutch judicial website. It uses **Selenium** and **BeautifulSoup** to scrape case details and saves the results in JSON and CSV formats.

## Features
- Extracts **ECLI**, **Title**, **Summary**, **Date**, **Court**, and **Link**.
- Saves data in **JSON** and **CSV** formats.
- Automatically loads more results for extensive scraping.
- Headless **Selenium** browsing for efficiency.

---

## Prerequisites
Make sure you have the following installed:

- Python 3.x
- Google Chrome (latest version)
- ChromeDriver (handled automatically by `webdriver_manager`)

### Required Python Packages
Install the dependencies using:
```sh
pip install -r requirements.txt
```

---

## Running the Scraper
### Windows
1. Clone the repository:
   ```sh
   git clone https://github.com/Prabhat-Kr-shukla/court-case-scraper.git
   ```
2. Navigate to the project folder:
   ```sh
   cd court-case-scraper
   ```
3. Run the script:
   ```sh
   python scraper.py
   ```
4. The extracted data will be saved as:
   - `court_cases_YYYYMMDD_HHMMSS.json`
   - `court_cases_YYYYMMDD_HHMMSS.csv`

### Mac
1. Open Terminal and clone the repository:
   ```sh
   git clone https://github.com/Prabhat-Kr-shukla/court-case-scraper.git
   ```
2. Navigate to the project directory:
   ```sh
   cd court-case-scraper
   ```
3. Run the script:
   ```sh
   python3 scraper.py
   ```

---

## Notes
- The scraper may need **modifications** if the website structure changes.
- Increase `time.sleep()` values if scraping too fast leads to missing data.
- Run with `--headless` mode for silent execution.

---

## Contributing
Feel free to submit **issues** or **pull requests** to improve the project! 🚀
