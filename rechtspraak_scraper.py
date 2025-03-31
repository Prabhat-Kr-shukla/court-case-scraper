from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import csv
from datetime import datetime
import re

# Generate timestamped file names
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
json_file = f"court_cases_{timestamp}.json"
csv_file = f"court_cases_{timestamp}.csv"

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the Rechtspraak website
url = "https://uitspraken.rechtspraak.nl/resultaat?inhoudsindicatie=zt0&publicatiestatus=ps1&sort=Relevance"
driver.get(url)
time.sleep(3)

MAX_RESULTS = 1000
results_collected = 0
data = []

while results_collected < MAX_RESULTS:
    # Get page source and parse with BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    # Extract cases
    cases = soup.select(".rnl-listresults-item-container")

    for case in cases:
        ecli_link = case.find("a", href=True)
        if not ecli_link:
            continue

        title = ecli_link.text.strip()
        link = "https://uitspraken.rechtspraak.nl" + ecli_link["href"]

        # Extract ECLI
        ecli_match = re.search(r"(ECLI:[A-Z]{2}:[A-Z]+:\d{4}:\d+)", title)
        ecli = ecli_match.group(0) if ecli_match else "N/A"

        # Extract Court Name
        court = title.split(",")[0].replace(ecli, "").strip()

        # Extract Date Correctly
        date_tag = case.find("label", string=re.compile("Datum uitspraak", re.IGNORECASE))
        date = date_tag.find_next("span").text.strip() if date_tag else "N/A"

        # Extract Summary Correctly
        summary_tag = case.find("label", string=re.compile("Inhoudsindicatie", re.IGNORECASE))
        summary = summary_tag.find_next("span").text.strip() if summary_tag else "No summary available"



        # Store extracted data
        data.append({
            "ECLI": ecli,
            "Title": title,
            "Summary": summary,
            "Date": date,
            "Court": court,
            "Link": link
        })

    results_collected = len(data)
    print(f"✅ Results collected so far: {results_collected}")

    # Try clicking 'Load More' button
    load_more_buttons = driver.find_elements(By.ID, "lib-rnl-lib-rnl-laadMeerBtn")

    if load_more_buttons:
        print(f"📌 Clicking 'Load More' button... (Collected: {results_collected})")
        driver.execute_script("arguments[0].click();", load_more_buttons[0])
        time.sleep(3)
    else:
        print("❌ No more 'Load More' button found.")
        break

driver.quit()

# Save data to JSON
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# Save data to CSV
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["ECLI", "Title", "Summary", "Date", "Court", "Link"])
    writer.writeheader()
    writer.writerows(data)

print(f"📂 Data saved: {json_file} & {csv_file}")
