Brief Documentation

This script is designed for automatic data collection from the Czech Statistical Office website about elections. The script retrieves data on voter turnout, votes, and other information for individual municipalities and saves it into a CSV file.

Description

The script performs the following steps:
Downloading HTML page: Downloads the HTML page with election data using the requests library.
Parsing HTML: Parses the HTML page and searches for tables with data on municipalities, voter counts, and votes for individual parties using the BeautifulSoup library.
Extracting data: Extracts data on municipality codes, their names, registered voters, envelopes, valid votes, and votes for individual parties.
Merging data: Merges the data into a single list of dictionaries, where each dictionary represents one municipality.
Saving to CSV: Saves the extracted and merged data into a CSV file.

Library Installation

Before running the script, it is necessary to install the required libraries:
requests
beautifulsoup4

Function Explanation

process_response(url): Downloads and processes the HTML page.
find_tables(soup): Finds all tables with the class table and returns their rows.
find_parties_tables(soup): Finds all divs with the class t2_470 and returns their rows.
scrape_municipality_urls(soup): Extracts URLs for individual municipalities.
convert_relative_to_absolute(url): Converts a relative URL to an absolute URL.
text_to_number(text): Converts text to a number.
scrape_voting_data(url): Extracts data on voters and envelopes.
extract_code_and_location(soup): Extracts municipality codes and names.
extract_parties_data(url): Extracts data on votes for individual parties.
merge_data(municipality_urls, code_and_location, voting_data, parties_data_list): Merges all data into a single list of dictionaries.
scrape_data(soup): Complete data collection.
save_data_csv(data, parties_data_list, filename): Saves data into a CSV file.
get_parties_keys(parties_data_list): Retrieves the names of all parties.
get_header(parties_list): Creates the CSV file header.
write_municipality_row(writer, data, header): Writes a single row of data into the CSV file.
main_fce(url): Main function that manages the entire process.
