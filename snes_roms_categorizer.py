import os
import time
import csv
import json
import requests
from igdb.wrapper import IGDBWrapper
import shutil
from tqdm import tqdm  # For progress bars

# Function to get the access token from Twitch
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

# Function to map IGDB genre names to custom terms
def map_genre_to_human_readable(genre_name):
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

# Function to fetch the genre of a game from IGDB
def fetch_genre(game_name, use_human_readable):
    try:
        # Search for the game on IGDB
        byte_array = wrapper.api_request(
            'games',
            f'search "{game_name}"; fields name, genres.name; limit 1;'
        )
        # Decode the byte array and parse the JSON response
        data = json.loads(byte_array.decode('utf-8'))
        
        # Extract the genre (if found)
        if data and isinstance(data, list) and len(data) > 0:
            genres = data[0].get("genres", [])
            if genres:
                genre_name = genres[0].get("name", "Others")
                # Apply custom mapping if enabled
                if use_human_readable:
                    genre_name = map_genre_to_human_readable(genre_name)
                return genre_name
        return "Others"
    except Exception as e:
        print(f"Error fetching {game_name}: {e}")
        return "Others"

# Function to generate the CSV database
def generate_csv(use_human_readable):
    # Get a list of all ROM files
    rom_files = [f for f in os.listdir(roms_path) if f.endswith(".smc") or f.endswith(".sfc")]
    total_roms = len(rom_files)

    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ROM Name", "Genre"])  # CSV headers

        # Iterate through all files in the ROMs folder with a progress bar
        for filename in tqdm(rom_files, desc="Generating CSV", unit="ROM"):
            game_name = os.path.splitext(filename)[0]  # Remove file extension
            genre = fetch_genre(game_name, use_human_readable)
            
            # Write the information to the CSV
            writer.writerow([filename, genre])
            
            # Wait 0.25 seconds to comply with the API limit (4 requests per second)
            time.sleep(0.25)

# Function to move ROMs based on the CSV
def move_roms():
    if not os.path.exists(csv_path):
        print("CSV database not found. Please generate it first.")
        return

    # Read the CSV file
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        rows = list(reader)

    # Create genre folders if they don't exist
    genres = set(row[1] for row in rows)  # Get all unique genres from the CSV
    for genre in genres:
        genre_folder = os.path.join(roms_path, genre)
        os.makedirs(genre_folder, exist_ok=True)  # Create folder if it doesn't exist

    # Move files with a progress bar
    for row in tqdm(rows, desc="Moving ROMs", unit="ROM"):
        filename, genre = row
        current_path = os.path.join(roms_path, filename)
        destination_path = os.path.join(roms_path, genre, filename)
        
        if os.path.exists(current_path):
            shutil.move(current_path, destination_path)
        else:
            print(f"File not found: {filename}")

# Function to reorganize ROMs based on the CSV
def reorganize_roms():
    if not os.path.exists(csv_path):
        print("CSV database not found. Please generate it first.")
        return

    # Read the CSV file
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        rows = list(reader)

    # Create genre folders if they don't exist
    genres = set(row[1] for row in rows)  # Get all unique genres from the CSV
    for genre in genres:
        genre_folder = os.path.join(roms_path, genre)
        os.makedirs(genre_folder, exist_ok=True)  # Create folder if it doesn't exist

    # Reorganize files with a progress bar
    for row in tqdm(rows, desc="Reorganizing ROMs", unit="ROM"):
        filename, genre = row
        # Search for the file in all subfolders
        for root, _, files in os.walk(roms_path):
            if filename in files:
                current_path = os.path.join(root, filename)
                destination_path = os.path.join(roms_path, genre, filename)
                
                # Move the file if it's not already in the correct folder
                if root != os.path.join(roms_path, genre):
                    shutil.move(current_path, destination_path)
                break

# Main script
if __name__ == "__main__":
    # Prompt user for ROMs path
    roms_path = input("Enter the full path to your ROMs folder: ").strip()

    # Path to the local CSV database
    csv_path = os.path.join(roms_path, "roms_database.csv")

    # Main menu
    print("1. Generate CSV database")
    print("2. Move ROMs based on CSV")
    print("3. Reorganize ROMs based on CSV")
    option = input("Select an option (1, 2, or 3): ")

    if option == "1":
        # Ask the user if they want to apply human-readable genre mapping
        use_human_readable = input("Do you want to apply human-readable genre mapping? (yes/no): ").strip().lower()
        use_human_readable = use_human_readable == "yes"

        # Prompt user for credentials (only needed for CSV generation)
        client_id = input("Enter your IGDB Client ID: ").strip()
        client_secret = input("Enter your IGDB Client Secret: ").strip()

        # Get the access token
        try:
            access_token = get_access_token(client_id, client_secret)
            print("Successfully authenticated with Twitch.")
        except Exception as e:
            print(e)
            exit()

        # Configure IGDB API with the access token
        wrapper = IGDBWrapper(client_id, access_token)

        # Generate the CSV
        generate_csv(use_human_readable)
        print("CSV database generated successfully.")
    elif option == "2":
        # Move ROMs based on the existing CSV
        move_roms()
        print("ROMs moved successfully.")
    elif option == "3":
        # Reorganize ROMs based on the existing CSV
        reorganize_roms()
        print("ROMs reorganized successfully.")
    else:
        print("Invalid option.")