"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Filip Hájek
email: filipp.hajek@gmail.com
discord: Filip filip936
"""

import requests
import bs4
import csv
import sys

def main_fce():
    if len(sys.argv) != 3:
        print("Usage: python Engeto_projekt_3_final.py <URL> <output_filename>")
        return
    
    url = sys.argv[1]
    output_filename = sys.argv[2]
    save_scrape(url, output_filename)

def save_scrape(url, output_filename):
    soup = process_response(url)
    data, parties_data_list = scrape_data(soup)
    save_data_csv(data, parties_data_list, output_filename)


def process_response(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("The URL could not be opened") 
    return bs4.BeautifulSoup(response.text, features="html.parser")

def find_tables(soup):
    tables = soup.find_all("table", {"class":"table"})
    list_tables = []
    for table in tables:
        list_tables.append(table.find_all("tr")[2:])
    return list_tables

def find_parties_tables(soup):
    tables = soup.find_all("div", {"class": "t2_470"})
    list_tables = []
    for table in tables:
        list_tables.append(table.find_all("tr")[2:])
    return list_tables

def scrape_municipality_urls(soup):
    td_municipalities = soup.find_all("td", {"class": "cislo"})
    urls = [td.find('a', href=True)['href'] for td in td_municipalities]
    absolute_urls = [convert_relative_to_absolute(url) for url in urls]
    return absolute_urls

def convert_relative_to_absolute(url):
    return f"https://volby.cz/pls/ps2017nss/{url}"

def text_to_number(text):
    text = text.replace(' ', '').replace('\xa0', '')
    return int(text)

def scrape_voting_data(url):
    soup = process_response(url)
    data = {}
    vote_table = soup.find("table", {"id": "ps311_t1"})
    if vote_table:
        td_numbers = vote_table.find_all("td", {"class": "cislo"})
        if len(td_numbers) >= 4:
            data["registered"] = text_to_number(td_numbers[3].text)
            data["envelopes"] = text_to_number(td_numbers[4].text)
            data["valid"] = text_to_number(td_numbers[7].text)
        else:
            print(f"Insufficient data for voting numbers in URL: {url}")
    else:
        print(f"Voting data table not found for URL: {url}")
    return data

def extract_code_and_location(soup):
    tables = find_tables(soup)
    list_data = []
    for table in tables:
        for tr in table:
            data = {}
            number = tr.find("td", {"class":"cislo"})
            name = tr.find("td", {"class":"overflow_name"})
            if number and name:
                data["code"] = number.get_text(strip=True)
                data["location"] = name.get_text(strip=True)
                list_data.append(data)
    return list_data

def extract_parties_data(url):
    soup = process_response(url)
    parties_data = {}
    parties_tables = find_parties_tables(soup)
    for table in parties_tables:
        for tr in table:
            party_name = tr.find("td", {"class": "overflow_name"})
            party_votes = tr.find("td", {"class": "cislo", "headers": "t1sa2 t1sb3"})
            if not party_votes:
                party_votes = tr.find("td", {"class": "cislo", "headers": "t2sa2 t2sb3"})
            if party_name and party_votes:
                parties_data[party_name.text.strip()] = text_to_number(party_votes.text)
            else:
                print("Wrong parties data. Name: ", party_name, "| Votes: ", party_votes, " | tr: ", tr)
    return parties_data

def merge_data(municipality_urls, code_and_location, voting_data, parties_data_list):
    merged_data = []
    for i in range(len(municipality_urls)):
        combined_data = {**code_and_location[i], **voting_data[i], **parties_data_list[i]}
        merged_data.append(combined_data)
    return merged_data

def scrape_data(soup):
    municipality_urls = scrape_municipality_urls(soup)
    code_and_location = extract_code_and_location(soup)
    parties_data_list = [extract_parties_data(url) for url in municipality_urls]
    voting_data = [scrape_voting_data(url) for url in municipality_urls]
    return merge_data(municipality_urls, code_and_location, voting_data, parties_data_list), parties_data_list

def save_data_csv(data, parties_data_list, filename):
    parties_list = get_parties_keys(parties_data_list)
    with open(filename, mode="w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        header = get_header(parties_list)
        writer.writerow(header)
        for municipality_data in data:
            write_municipality_row(writer, municipality_data, header)

def get_parties_keys(parties_data_list):
    headers = set()
    for date in parties_data_list:
        headers.update(date.keys())
    return list(headers)

def get_header(parties_list):
    row = ['code', 'location', 'registered', 'envelopes', 'valid']
    return row + parties_list

def write_municipality_row(writer, data, header):
    row = []
    for column in header:
        value = data.get(column)
        if value is None and "parties" in data:
            value = data["parties"].get(column, 0)
        row.append(value)
    writer.writerow(row)

if __name__ == "__main__":
    main_fce()