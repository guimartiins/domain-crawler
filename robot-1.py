from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd


def read_domains(filename):
    domains_to_search = pd.read_excel(filename)
    return domains_to_search.values


def check_domain_availability(driver, domain):
    search_input = driver.find_element(By.ID, "is-avail-field")
    search_input.clear()
    search_input.send_keys(domain)
    search_input.send_keys(Keys.RETURN)
    time.sleep(2)
    results = driver.find_elements(By.TAG_NAME, "strong")
    return {
        "domain_name": domain,
        "availability": results[2].text
    }


def check_domains_availability(driver, domains):
    domains_availability = []
    for domain in domains:
        domain_availability = check_domain_availability(driver, domain[0])
        domains_availability.append(domain_availability)
    return domains_availability


def write_domains_availability(filename, domains_availability):
    with open(filename, "w") as f:
        for domain_availability in domains_availability:
            f.write(f"{domain_availability['domain_name']}: {domain_availability['availability']}\n")


if __name__ == "__main__":
    print("Starting up the browser...\n")
    driver = webdriver.Chrome("./")
    driver.get("https://registro.br")
    
    print("Reading excel table...\n")
    domains_to_search = read_domains("domains.xlsx")
    print("Read excel done!\n")

    print("Checking domains availability...\n")
    domains_availability = check_domains_availability(driver, domains_to_search)
    print("Check domains availability done!\n")
    print(domains_availability)

    print("Writing domains availability to file...\n")
    write_domains_availability("domains_availability.txt", domains_availability)
    print("Write domains availability done!\n")

    driver.close()