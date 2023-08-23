from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

# Start a new instance of Chrome web browser
driver = webdriver.Chrome()

# Navigate to the webpage
driver.get("http://uc.socioambiental.org/pt-br")

# Click on the specified element to load the table
tab_element = driver.find_element(
    By.CSS_SELECTOR, "#tab-pesquisa > div.nav-tabs-custom > ul > li:nth-child(2) > a"
)
tab_element.click()

# Wait for a few seconds to ensure the table is loaded
time.sleep(5)

# Get the table's HTML
table_html = driver.find_element(By.CSS_SELECTOR, "div#results table").get_attribute(
    "outerHTML"
)

# Use BeautifulSoup to parse the table and extract required data
soup = BeautifulSoup(table_html, "html.parser")
table_rows = soup.find_all("tr")

# First table data
data = []

# Second table data
data2 = []

# Dictionary mapping acronyms to full names
acronym_to_full = {
    "PES": "Parque Estadual",
    "REBIO": "Reserva Biológica",
    "PARNA": "Parque Nacional",
    "ESEC": "Estação Ecológica",
    "RESEX": "Reserva Extrativista",
    "FLONA": "Floresta Nacional",
    "FES": "Floresta Estadual",
    "ARIE": "Área de Relevante Interesse Ecológico",
    "APA": "Área de Proteção Ambiental",
    "RVS": "Refúgio de Vida Silvestre",
    "RDS": "Reserva de Desenvolvimento Sustentável",
    "RBIOSF": "Reserva Biológica de Uso Sustentável Florestal",
    "RESEC": "Reserva Ecológica",
    "FERS": "Floresta Estadual de Rendimento Sustentado",
    "MONAT": "Monumento Natural",
}

for tr in table_rows[1:]:  # skipping the header row
    tds = tr.find_all("td")

    url_end = tds[0].a["href"].split("/")[-1]
    category = tds[1].text.strip()
    area = tds[2].text.strip()
    code = tds[3].text.strip()

    # REPLACE ACRONYM FOR FULL
    full_category = acronym_to_full.get(category, category)
    name = full_category + " " + tds[0].text.strip()

    # Add to the main data
    data.append(
        [name, category, area, code, "http://uc.socioambiental.org" + tds[0].a["href"]]
    )

    # Add to the second table
    description = f"nature reserve in Brazil ({full_category})"
    data2.append([name, url_end, description])

# Convert to pandas DataFrame
df = pd.DataFrame(data, columns=["Name", "Category", "Area (ha)", "Code", "URL"])
df2 = pd.DataFrame(data2, columns=["Label", "ID", "Description"])

# Save data to CSV
df.to_csv("table_data.csv", index=False)
df2.to_csv("table_data2.csv", index=False)

# Close the browser
driver.close()
