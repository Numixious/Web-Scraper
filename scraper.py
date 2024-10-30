import requests
from bs4 import BeautifulSoup
import csv

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")

python_jobs = results.find_all(
    "h2", string=lambda text: "python" in text.lower()
)

python_job_cards = [
    h2_element.parent.parent.parent for h2_element in python_jobs
]

# Define CSV file and column headers
csv_file = "python_jobs.csv"
csv_columns = ["Title", "Company", "Location", "Apply Link"]

# Open the CSV file in write mode
with open(csv_file, mode="w", newline='', encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=csv_columns)
    writer.writeheader()

    # Collect job data and write each job as a row in the CSV file
    for job_card in python_job_cards:
        title = job_card.find("h2", class_="title").text.strip()
        company = job_card.find("h3", class_="company").text.strip()
        location = job_card.find("p", class_="location").text.strip()
        link_url = job_card.find_all("a")[1]["href"]

        # Write job data to CSV
        writer.writerow({
            "Title": title,
            "Company": company,
            "Location": location,
            "Apply Link": link_url
        })

print(f"Job listings saved to {csv_file}")
