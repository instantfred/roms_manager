import os
import time
import csv
import json
import requests
from igdb.wrapper import IGDBWrapper
import shutil
from tqdm import tqdm
from colorama import Fore, Style, init
from genre_mapping import custom_genre_mapping

# Initialize colorama
init(autoreset=True)

# Global variables to store credentials and API wrapper
client_id = None
client_secret = None
access_token = None
wrapper = None

def get_access_token():
    global client_id, client_secret, access_token, wrapper
    if not client_id or not client_secret:
        client_id = input("Enter your IGDB Client ID: ").strip()
        client_secret = input("Enter your IGDB Client Secret: ").strip()

    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        access_token = response.json()["access_token"]
        wrapper = IGDBWrapper(client_id, access_token)
        print(Fore.GREEN + "Successfully authenticated with Twitch.")
    else:
        raise Exception(f"Failed to get access token: {response.status_code} - {response.text}")

def map_genre_to_custom(genre_name):
    genre_mapping = custom_genre_mapping
    return genre_mapping.get(genre_name, "Others")

def fetch_game_info(game_name, use_custom):
    try:
        byte_array = wrapper.api_request(
            'games',
            f'search "{game_name}"; fields name, genres.name, involved_companies.company.name; limit 1;'
        )
        data = json.loads(byte_array.decode('utf-8'))
        
        if data and isinstance(data, list) and len(data) > 0:
            game_data = data[0]
            genres = game_data.get("genres", [])
            publishers = game_data.get("involved_companies", [])

            genre_name = genres[0].get("name", "Others") if genres else "Others"
            if use_custom:
                genre_name = map_genre_to_custom(genre_name)

            publisher_names = [company["company"]["name"] for company in publishers if company.get("company")]
            publisher = publisher_names[0] if publisher_names else "Unknown Publisher"

            return {
                "name": game_data.get("name", game_name),
                "genre": genre_name,
                "publisher": publisher
            }
        return {
            "name": game_name,
            "genre": "Others",
            "publisher": "Unknown Publisher"
        }
    except Exception as e:
        print(Fore.RED + f"Error fetching {game_name}: {e}")
        return {
            "name": game_name,
            "genre": "Others",
            "publisher": "Unknown Publisher"
        }

def generate_csv(use_custom):
    rom_files = []
    for root, _, files in os.walk(roms_path):
        for file in files:
            if file.endswith(".smc") or file.endswith(".sfc"):
                rom_files.append(os.path.join(root, file))

    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ROM Name", "Genre", "Publisher"])

        for rom_path in tqdm(rom_files, desc="Generating CSV", unit="ROM"):
            filename = os.path.basename(rom_path)
            game_name = os.path.splitext(filename)[0]
            game_info = fetch_game_info(game_name, use_custom)
            writer.writerow([filename, game_info["genre"], game_info["publisher"]])
            time.sleep(0.25)

def reorganize_roms(organize_by):
    if not os.path.exists(csv_path):
        print(Fore.RED + "CSV database not found. Please generate it first.")
        return

    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        rows = list(reader)

    if organize_by == "genre":
        key_index = 1
    elif organize_by == "publisher":
        key_index = 2
    elif organize_by == "alphabet":
        key_index = 0
    else:
        print(Fore.RED + "Invalid organization option.")
        return

    keys = set(row[key_index] for row in rows)
    for key in keys:
        if organize_by == "alphabet":
            key_folder = os.path.join(roms_path, key[0].upper())
        else:
            key_folder = os.path.join(roms_path, key)
        os.makedirs(key_folder, exist_ok=True)

    for row in tqdm(rows, desc=f"Reorganizing by {organize_by}", unit="ROM"):
        filename, genre, publisher = row
        if organize_by == "genre":
            key = genre
        elif organize_by == "publisher":
            key = publisher
        elif organize_by == "alphabet":
            key = filename[0].upper()

        for root, _, files in os.walk(roms_path):
            if filename in files:
                current_path = os.path.join(root, filename)
                destination_path = os.path.join(roms_path, key, filename)
                
                if root != os.path.join(roms_path, key):
                    shutil.move(current_path, destination_path)
                break

def cleanup_empty_folders():
    print(Fore.YELLOW + "Cleaning up empty folders...")
    deleted_folders = 0

    for root, dirs, _ in os.walk(roms_path, topdown=False):
        for dir in dirs:
            folder_path = os.path.join(root, dir)
            try:
                if not os.listdir(folder_path):
                    os.rmdir(folder_path)
                    print(Fore.CYAN + f"Deleted empty folder: {folder_path}")
                    deleted_folders += 1
            except Exception as e:
                print(Fore.RED + f"Error deleting folder {folder_path}: {e}")

    print(Fore.GREEN + f"Deleted {deleted_folders} empty folders.")

if __name__ == "__main__":
    roms_path = input(Fore.CYAN + "Enter the full path to your ROMs folder: ").strip()
    csv_path = os.path.join(roms_path, "roms_database.csv")

    while True:
        print(Fore.YELLOW + "\n1. Generate CSV database")
        print(Fore.YELLOW + "2. Organize by Genre")
        print(Fore.YELLOW + "3. Organize by Publisher")
        print(Fore.YELLOW + "4. Organize by Alphabet")
        print(Fore.YELLOW + "5. Clean up empty folders")
        print(Fore.YELLOW + "Q. Quit")
        option = input(Fore.CYAN + "Select an option (1-5, or Q): ").strip().lower()

        if option == "1":
            use_custom = input(Fore.CYAN + "Do you want to apply custom genre mapping? (yes/no): ").strip().lower()
            use_custom = use_custom == "yes"

            try:
                if not wrapper:
                    get_access_token()
                generate_csv(use_custom)
                print(Fore.GREEN + "CSV database generated successfully.")
            except Exception as e:
                print(Fore.RED + str(e))
        elif option == "2":
            reorganize_roms("genre")
            print(Fore.GREEN + "ROMs reorganized successfully.")
        elif option == "3":
            reorganize_roms("publisher")
            print(Fore.GREEN + "ROMs reorganized successfully.")
        elif option == "4":
            reorganize_roms("alphabet")
            print(Fore.GREEN + "ROMs reorganized successfully.")
        elif option == "5":
            cleanup_empty_folders()
        elif option in ["q", "quit", "exit"]:
            print(Fore.YELLOW + "Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid option. Please try again.")