# ROM Organizer Script

This script is designed to help you organize your SNES ROM collection by categorizing them into folders based on genre, publisher, or alphabetical order. It uses the IGDB API to fetch game information and allows you to customize genre mappings. Additionally, it includes a cleanup feature to remove empty folders after reorganization.

## Features

### Generate CSV Database
- Fetches game information (genre, publisher) from the IGDB API.
- Creates a `roms_database.csv` file in your ROMs folder.

### Reorganize ROMs
- Moves ROMs into folders based on:
     - **Genre**
     - **Publisher**
     - **Alphabetical order** (first letter of the ROM name).

### Clean Up Empty Folders
- Deletes all empty folders in the ROMs directory after reorganization.

### Colored Console Output
- Uses colored text for better readability:
     - **Success messages**: Green
     - **Error messages**: Red
     - **Prompts**: Cyan
     - **Menu options**: Yellow

### Custom Genre Mapping
- Allows you to map IGDB genre names to custom, user-friendly names.

## Requirements

- **Python 3.8 or higher**: Download from [python.org](https://www.python.org/).
- **Python Libraries**:
     - `requests`
     - `tqdm`
     - `colorama`
     - `igdb-api-v4`
- Install them using:
     ```bash
     pip install requests tqdm colorama igdb-api-v4
     ```
- **IGDB API Credentials**:
     - Register at [IGDB API](https://api-docs.igdb.com/) to get a Client ID and Client Secret.

## Usage

### Step 1: Run the Script
Open a terminal or command prompt and navigate to the folder where the script is located. Run the script using:
```bash
python snes_rom_organizer.py
```

### Step 2: Enter the ROMs Path
The script will prompt you to enter the full path to your ROMs folder. For example:
```
Enter the full path to your ROMs folder: D:\ROMS\
```

### Step 3: Select an Option
The script will display a menu with the following options:
```
1. Generate CSV database
2. Organize by Genre
3. Organize by Publisher
4. Organize by Alphabet
5. Clean up empty folders
Q. Quit
Select an option (1-5, or Q/q/quit/exit):
```

#### Option 1: Generate CSV Database
- Enter IGDB Credentials (if not already authenticated):
     ```
     Enter your IGDB Client ID: abcdefg12345
     Enter your IGDB Client Secret: hijklmn67890
     Successfully authenticated with Twitch.
     ```
- Apply Custom Genre Mapping (optional):
     ```
     Do you want to apply custom genre mapping? (yes/no): yes
     ```
- Wait for CSV Generation:
     The script will fetch game information and create a `roms_database.csv` file in your ROMs folder.

#### Option 2-4: Reorganize ROMs
- **Organize by Genre**: Moves ROMs into folders named after their genre.
- **Organize by Publisher**: Moves ROMs into folders named after their publisher.
- **Organize by Alphabet**: Moves ROMs into folders named after the first letter of the ROM name.

#### Option 5: Clean Up Empty Folders
- Deletes all empty folders in the ROMs directory. Useful after reorganizing ROMs.

#### Option Q: Quit
- Exits the script.

## Example Workflow

### Generate CSV:
```
Select an option (1-5, or Q/q/quit/exit): 1
Do you want to apply custom genre mapping? (yes/no): yes
Enter your IGDB Client ID: abcdefg12345
Enter your IGDB Client Secret: hijklmn67890
Successfully authenticated with Twitch.
Generating CSV: 100%|████████████████████| 50/50 [00:12<00:00,  4.00ROM/s]
CSV database generated successfully.
```

### Reorganize ROMs by Publisher:
```
Select an option (1-5, or Q/q/quit/exit): 3
Reorganizing by publisher: 100%|████████████████████| 50/50 [00:03<00:00, 500.00ROM/s]
ROMs reorganized successfully.
```

### Clean Up Empty Folders:
```
Select an option (1-5, or Q/q/quit/exit): 5
Cleaning up empty folders...
Deleted empty folder: D:\ROMS\OldFolder
Deleted 1 empty folders.
```

### Quit:
```
Select an option (1-5, or Q/q/quit/exit): q
Goodbye!
```

## Folder Structure Examples

### By Publisher:
```
D:\ROMS\
├── Nintendo
│   ├── Super Mario World.smc
│   └── The Legend of Zelda.smc
├── Capcom
│   └── Street Fighter II.smc
└── Unknown Publisher
          └── SomeOtherGame.smc
```

### By Alphabet:
```
D:\ROMS\
├── A
│   └── Aladdin.smc
├── S
│   ├── Super Mario World.smc
│   └── Street Fighter II.smc
└── T
          └── The Legend of Zelda.smc
```

## Notes

- **API Rate Limit**: IGDB has a limit of 4 requests per second. The script includes a delay to comply with this limit.
- **Custom Genre Mapping**: You can modify the `genre_mapping` dictionary in the script to customize genre names.
- **Empty Folder Cleanup**: The cleanup feature only deletes empty folders. Folders with files are left untouched.

## Support

If you encounter any issues or have questions, feel free to open an issue or contact me directly.

Enjoy organizing your ROM collection! 😊OM Organizer Script