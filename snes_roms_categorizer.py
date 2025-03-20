import os
import time
import csv
import json
import requests
from igdb.wrapper import IGDBWrapper
import shutil
from tqdm import tqdm

def get_access_token(client_id, client_secret):
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to get access token: {response.status_code} - {response.text}")

def map_genre_to_custom(genre_name):
    genre_mapping = {
        "Hack and slash/Beat 'em up": "Action",
        "Platform": "Platformer",
        "Real Time Strategy (RTS)": "Strategy",
        "Turn-based strategy (TBS)": "Strategy",
        "Shooter": "Shooter",
        "Fighting": "Fighting",
        "Adventure": "Adventure",
        "Puzzle": "Puzzle",
        "Role-playing (RPG)": "RPG",
        "Simulator": "Simulation",
        "Sport": "Sports",
        "Strategy": "Strategy",
        "Quiz/Trivia": "Trivia",
        "Pinball": "Pinball",
        "Racing": "Racing",
        "Music": "Music",
        "Tactical": "Tactical",
        "Horror": "Horror",
        "Sandbox": "Sandbox",
        "Open world": "Open World",
        "Stealth": "Stealth",
        "Survival": "Survival",
        "Battle royale": "Battle Royale",
        "MMO": "MMO",
        "MOBA": "MOBA",
        "Card & Board Game": "Card Game",
        "Point-and-click": "Adventure",
        "Visual Novel": "Visual Novel",
        "Idle": "Idle",
        "Arcade": "Arcade",
        "Party": "Party",
        "Educational": "Educational",
        "Fitness": "Fitness",
        "Non-game": "Non-game",
        "Puzzle-platformer": "Puzzle",
        "Run and gun": "Action",
        "Shoot 'em up": "Shooter",
        "Text-based": "Text-based",
        "Third-person shooter": "Shooter",
        "Top-down shooter": "Shooter",
        "Tower defense": "Strategy",
        "Trivia": "Trivia",
        "Vehicular combat": "Action",
        "Wrestling": "Sports",
        "4X": "Strategy",
        "Artillery": "Strategy",
        "Auto battler": "Strategy",
        "Beat 'em up": "Action",
        "Breakout": "Arcade",
        "Casual": "Casual",
        "Christian": "Religious",
        "Combat": "Action",
        "Dungeon crawler": "RPG",
        "Escape room": "Puzzle",
        "First-person shooter": "Shooter",
        "God game": "Simulation",
        "Hero shooter": "Shooter",
        "Hunting": "Sports",
        "Interactive movie": "Adventure",
        "Light gun": "Shooter",
        "Metroidvania": "Platformer",
        "Monster tamer": "RPG",
        "On-rails shooter": "Shooter",
        "Platformer": "Platformer",
        "Programming": "Educational",
        "Rhythm": "Music",
        "Roguelike": "RPG",
        "Roguelite": "RPG",
        "Side-scroller": "Platformer",
        "Social deduction": "Party",
        "Space flight": "Simulation",
        "Survival horror": "Horror",
        "Tactical RPG": "RPG",
        "Tank": "Simulation",
        "Tug of war": "Sports",
        "Turn-based tactics": "Strategy",
        "Virtual pet": "Simulation",
        "Visual novel": "Visual Novel",
        "Walking simulator": "Adventure",
        "Wargame": "Strategy",
        "Word game": "Educational",
        "Zombie": "Horror"
    }
    return genre_mapping.get(genre_name, "Others")

def fetch_genre(game_name, use_custom):
    try:
        byte_array = wrapper.api_request(
            'games',
            f'search "{game_name}"; fields name, genres.name; limit 1;'
        )
        data = json.loads(byte_array.decode('utf-8'))
        
        if data and isinstance(data, list) and len(data) > 0:
            genres = data[0].get("genres", [])
            if genres:
                genre_name = genres[0].get("name", "Others")
                if use_custom:
                    genre_name = map_genre_to_custom(genre_name)
                return genre_name
        return "Others"
    except Exception as e:
        print(f"Error fetching {game_name}: {e}")
        return "Others"

def generate_csv(use_custom):
    rom_files = [f for f in os.listdir(roms_path) if f.endswith(".smc") or f.endswith(".sfc")]

    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ROM Name", "Genre"])

        for filename in tqdm(rom_files, desc="Generating CSV", unit="ROM"):
            game_name = os.path.splitext(filename)[0]
            genre = fetch_genre(game_name, use_custom)
            writer.writerow([filename, genre])
            time.sleep(0.25)

def move_roms():
    if not os.path.exists(csv_path):
        print("CSV database not found. Please generate it first.")
        return

    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        rows = list(reader)

    genres = set(row[1] for row in rows)
    for genre in genres:
        genre_folder = os.path.join(roms_path, genre)
        os.makedirs(genre_folder, exist_ok=True)

    for row in tqdm(rows, desc="Moving ROMs", unit="ROM"):
        filename, genre = row
        current_path = os.path.join(roms_path, filename)
        destination_path = os.path.join(roms_path, genre, filename)
        
        if os.path.exists(current_path):
            shutil.move(current_path, destination_path)
        else:
            print(f"File not found: {filename}")

def reorganize_roms():
    if not os.path.exists(csv_path):
        print("CSV database not found. Please generate it first.")
        return

    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        rows = list(reader)

    genres = set(row[1] for row in rows)
    for genre in genres:
        genre_folder = os.path.join(roms_path, genre)
        os.makedirs(genre_folder, exist_ok=True)

    for row in tqdm(rows, desc="Reorganizing ROMs", unit="ROM"):
        filename, genre = row
        for root, _, files in os.walk(roms_path):
            if filename in files:
                current_path = os.path.join(root, filename)
                destination_path = os.path.join(roms_path, genre, filename)
                
                if root != os.path.join(roms_path, genre):
                    shutil.move(current_path, destination_path)
                break

if __name__ == "__main__":
    roms_path = input("Enter the full path to your ROMs folder: ").strip()
    csv_path = os.path.join(roms_path, "roms_database.csv")

    while True:
        print("\n1. Generate CSV database")
        print("2. Move ROMs based on CSV")
        print("3. Reorganize ROMs based on CSV")
        print("Q. Quit")
        option = input("Select an option (1, 2, 3, or Q): ").strip().lower()

        if option == "1":
            use_custom = input("Do you want to apply custom genre mapping? (yes/no): ").strip().lower()
            use_custom = use_custom == "yes"

            client_id = input("Enter your IGDB Client ID: ").strip()
            client_secret = input("Enter your IGDB Client Secret: ").strip()

            try:
                access_token = get_access_token(client_id, client_secret)
                print("Successfully authenticated with Twitch.")
            except Exception as e:
                print(e)
                continue

            wrapper = IGDBWrapper(client_id, access_token)
            generate_csv(use_custom)
            print("CSV database generated successfully.")
        elif option == "2":
            move_roms()
            print("ROMs moved successfully.")
        elif option == "3":
            reorganize_roms()
            print("ROMs reorganized successfully.")
        elif option in ["q", "quit", "exit"]:
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")