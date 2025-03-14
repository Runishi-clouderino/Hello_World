import time

import requests
from bs4 import BeautifulSoup

#List of OSRS skill names in the corred order
skill_names = [
    "Attack", "Strength", "Defence", "Ranged", "Prayer", "Magic", "Cooking", "Woodcutting",
    "Fletching", "Fishing", "Firemaking", "Crafting", "Smithing", "Mining", "Herblore",
    "Agility", "Thieving", "Slayer", "Farming", "Runecrafting", "Hunter", "Construction",
    "Hitpoints", "Overall"
]

def OSRS_username():
    username = input("Please enter your OSRS username: ")
    return username

def OSRS_hiscores(username):
    url = f"https://secure.runescape.com/m=hiscore_oldschool/hiscorepersonal?user={username}"
    time.sleep(3)

    try:
        response = requests.get(url)
        #check if the response was succesful
        if response.status_code == 200:
            return response.text #this will return the raw stats in text format
        else:
            print("Error fetching data. Please check username.")
            return None
    except Exception as e:
        print(f"An error occured: {e}")
        return None

def parse_hiscore_data(html_content):
    #use beautifulsoup to parse ht HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    #find the stats table
    table = soup.find('table', {'class': 'hiscore-table'}) # Look for the table with class 'hiscore-table'

    #List to store parsed data
    stats = []

    #iterate over each row in the table (skipping the header row)
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        if len(cells) > 1:
            skill_name = cells[0].get_text(strip=True) #skill name
            skill_level = cells[1].get_text(strip=True) #skill level
            skill_exp = cells[2].get_text(strip=True) #skill exp
            stats.append((skill_name, skill_level, skill_exp))

    return stats



def display_stats(stats):
    if stats:
        print("OSRS Stats:")
        for stat in stats:
            skill_name, skill_level, skill_exp = stat
            print(f"{skill_name}: Level{skill_level} | XP: {skill_exp}")
    else:
        print("No data display.")

def main():
    username = OSRS_username()
    html_content = OSRS_hiscores(username)

    if html_content:
        stats = parse_hiscore_data(html_content)
        display_stats(stats)

if __name__ == "__main__":
    main()
