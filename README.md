# ROM Organizer Script

This script is designed to automatically organize a collection of SNES ROMs into folders based on their genre. It uses the IGDB API to fetch game information and categorize the ROMs. Additionally, it allows you to generate a local database in CSV format and move the ROM files to their corresponding folders.

## Requirements

- **Python 3.8 or higher**: Make sure you have Python installed. You can download it from [python.org](https://www.python.org/).
- **Python Libraries**: The script uses the following libraries:
    - `requests`
    - `tqdm`
    - `igdb-api-v4`

    You can install them by running:
    ```bash
    pip install requests tqdm igdb-api-v4
    ```

- **IGDB Credentials**:
    - You will need a Client ID and a Client Secret from IGDB. Sign up at [IGDB API](https://api-docs.igdb.com/) to get them.

## Setup

1. **Clone or download the script**:
     - Download the `snes_roms_organizer.py` script and place it in a folder of your choice.

2. **Prepare your ROM collection**:
     - Place all your ROM files (`.smc` or `.sfc`) in a folder. For example:
         ```
         D:\ROMS\
         ```

## Usage

### Step 1: Run the Script

Open a terminal or command prompt and navigate to the folder where you saved the script. Then, run:
```bash
python snes_roms_organizer.py
```

### Step 2: Select an Option

The script will display a menu with two options:
```
1. Generate CSV database
2. Move ROMs based on CSV
Select an option (1 or 2):
```

#### Option 1: Generate the CSV Database

1. Enter the path to your ROMs folder:
     ```
     Enter the full path to your ROMs folder: D:\ROMS\
     ```

2. Choose whether to apply a custom genre mapping:
     ```
     Do you want to apply a custom genre mapping? (yes/no): yes
     ```
     What this means, is that we are going to map the games into the categories defined by the variable `map_genre_to_human_readable`. You can always update that to your desire or omit it to use IGDB's categories.

3. Enter your IGDB credentials:
     ```
     Enter your IGDB Client ID: your_client_id
     Enter your IGDB Client Secret: your_client_secret
     ```

4. Wait for the CSV to be generated:
     - The script will query the IGDB API for each ROM and generate a `roms_database.csv` file in the ROMs folder. You will see a progress bar:
         ```
         Generating CSV: 100%|████████████████████| 50/50 [00:12<00:00,  4.00ROM/s]
         CSV database generated successfully.
         ```

#### Option 2: Move ROMs Based on the CSV

1. Enter the path to your ROMs folder:
     ```
     Enter the full path to your ROMs folder: D:\ROMS\
     ```

2. Wait for the ROMs to be moved:
     - The script will read the `roms_database.csv` file and move the ROMs to their corresponding genre folders. You will see a progress bar:
         ```
         Moving ROMs: 100%|████████████████████| 50/50 [00:03<00:00, 500.00ROM/s]
         ROMs moved successfully.
         ```

## Usage Examples

### Example 1: Generate the CSV
```plaintext
Enter the full path to your ROMs folder: D:\ROMS\
1. Generate CSV database
2. Move ROMs based on CSV
Select an option (1 or 2): 1
Do you want to apply human-readable genre mapping? (yes/no): yes
Enter your IGDB Client ID: abcdefg12345
Enter your IGDB Client Secret: hijklmn67890
Successfully authenticated with Twitch.
Generating CSV: 100%|████████████████████| 50/50 [00:12<00:00,  4.00ROM/s]
CSV database generated successfully.
```

### Example 2: Move the ROMs
```plaintext
Enter the full path to your ROMs folder: D:\ROMS\
1. Generate CSV database
2. Move ROMs based on CSV
Select an option (1 or 2): 2
Moving ROMs: 100%|████████████████████| 50/50 [00:03<00:00, 500.00ROM/s]
ROMs moved successfully.
```

## Folder Structure

After moving the ROMs, the folder structure will look like this:
```
D:\ROMS\
├── Action
│   ├── 3 Ninjas Kick Back.smc
│   └── Super Mario World.smc
├── RPG
│   └── Chrono Trigger.smc
├── Puzzle
│   └── Tetris Attack.smc
└── Others
        └── SomeOtherGame.smc
```

## Additional Notes

- **API Rate Limit**: IGDB has a limit of 4 requests per second. The script includes a delay to comply with this limit.
- **Genre Mapping**: If you choose to apply custom genre mapping, genre names will be simplified (e.g., "Hack and slash/Beat 'em up" becomes "Action").
- **Errors**: If a file is not found during the move process, the script will print a message but continue with the next file.

## Support

If you encounter any issues or have questions, feel free to open an issue in the repository or contact me directly.

I hope this script helps you organize your ROM collection! 😊

