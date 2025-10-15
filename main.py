import tkinter as tk
from pathlib import Path
from tkinter import ttk, font
from tkinter import messagebox
import subprocess
import argparse
import configparser

# Initialize the argument parser
# --game it's the game id set in config.cfg/GAME_ID
# --dir it's the directory name where is the game is stored
parser = argparse.ArgumentParser(description="This application is used to select a user and execute a for Saved Games symlink.")
parser.add_argument("-g", "--game", type=str, help="Game", required=True)
parser.add_argument("-d", "--dir", type=str, help="Directory", required=False)
args = parser.parse_args()

# Read a properties file with sections
def read_configfile(filename="config.cfg"):
    cfgParser = configparser.ConfigParser()
    cfgParser.optionxform = str  # Preserve the original case of keys
    cfgParser.read(Path(__file__).parent.resolve() / filename)

    props = {}
    for section in cfgParser.sections():
        props[section.upper()] = {}
        for key, value in cfgParser.items(section):
            props[section.upper()][key] = value
    return props

config = read_configfile()
game = read_configfile("game.cfg")
languages=config["MAIN"].get("languages", "en,fr").split(",")

if (not args.game in game["GAME_TITLE"]) and (not args.dir in game["GAME_TITLE"]) :
    print("Selected game not found in game.cfg : ", args.game, args.dir)
    exit(1)

if (not args.game in config["GAME_ID"]) and (not args.dir in config["GAME_ID"]) :
    print("Selected game is not configured in config.cfg : ", args.game, args.dir)
    exit(1)

game_title = 'Game Title'
if args.game in game["GAME_TITLE"]:
    game_title = game["GAME_TITLE"][args.game]

game_id = ''
if args.game in config["GAME_ID"]:
    game_id = config["GAME_ID"][args.game]
elif args.dir in config["GAME_ID"]:
    game_id = config["GAME_ID"][args.dir]


if not config["GAME_DIR"][game_id] or not config["USER_DIR"][game_id] :
    print("Selected game not correctly configured : ", game_id)
    exit(1)


translations = {}
for language in languages:
    translations[language]=config["TRANSLATION_" + language.upper()]

current_language = config["MAIN"].get("defaultLanguage", "en")
language_index = languages.index(current_language)

def update_language():
    global current_language
    lang_data = translations[current_language]

    # Update the window title
    root.title(lang_data["title"])

    # Update all visible text
    label.config(text=lang_data["select_user"])
    execute_button.config(text=lang_data["validate"])
    dropdown.set(lang_data["placeholder"])
    language_link.config(text=lang_data["language_toggle"])
    max_withTxt = max(len(user) for user in users)
    max_withTxt = max(max_withTxt, len(translations[current_language]["placeholder"]))
    dropdown.config(width=max_withTxt)


def toggle_language():
    global current_language
    global language_index
    language_index+=1
    if language_index >= len(languages): language_index=0
    current_language = languages[language_index]
    update_language()
    root.update_idletasks()

def validate_and_execute():
    lang_data = translations[current_language]

    # Get the selected user from the Combobox
    selected_user = dropdown.get().lower()

    if not selected_user or selected_user == lang_data["placeholder"]:
        # Show a warning if no user is selected
        messagebox.showwarning(lang_data["no_selection"], lang_data["select_warning"])
        return

    # Confirmation dialog
    confirm = messagebox.askyesno(lang_data["confirm_selection"], lang_data["confirm_prompt"].format(selected_user))
    if confirm:
        try:
            root_dir = config["ROOT_DIR"][game_id] or "/home/nico/Saved\\ Games/"
            game_dir = config["GAME_DIR"][game_id]
            user_dir = config["USER_DIR"][game_id].format(selected_user)

            # Remove symlink
            command = f"rm -f {game_dir}"
            subprocess.run(command, shell=True, check=False)

            command = f"ln -s {root_dir}{user_dir} {game_dir}"
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror(lang_data["error"], lang_data["error_message"].format(str(e)))


# Create main application window
root = tk.Tk()
root.title(translations[current_language]["title"])

# Define larger fonts for Combobox
font_large = ("Arial", 16)  # Font for the Combobox text
font_link = ("Arial", 11, "underline")
font_xlarge = ("Arial", 24)

# Apply a custom style to the Combobox using ttk.Style
style = ttk.Style()
style.configure(
    "TCombobox",
    font=font_large,
    arrowsize=30,
    foreground="black",  # Text color of placeholder/selected value
    fieldbackground="white",  # Background color for the input area in readonly state
    background="white"  # Background color for the dropdown button
)
style.theme_use("default")

# Apply a custom style for the internal list using the root `tk` widget
root.option_add("*TCombobox*Listbox*Font", font_large)
root.grid_rowconfigure(0)

# Create a clickable link for language toggle (top-right corner)
language_link = tk.Label(root, text=translations[current_language]["language_toggle"], font=font_link,
                         fg="blue", cursor="hand2")
language_link.bind("<Button-1>", lambda e: toggle_language())
language_link.grid(row=0, column=5, sticky="ne", padx=10, pady=10)

# Create a Label with a larger font
labelTitle = tk.Label(root, text=game_title, font=font_xlarge, height=3, anchor="n")
labelTitle.grid(row=0, column=1, columnspan=4, sticky="n")

label = tk.Label(root, text=translations[current_language]["select_user"], font=font_large)
label.grid(row=2, column=2, sticky="w", padx=10)

# Create a Dropdown (Combobox) with a larger font and dropdown options
users = config["MAIN"].get("users", "user1,user2").split(",")
max_withTxt = max(len(user) for user in users)
max_withTxt = max(max_withTxt, len(translations[current_language]["placeholder"]))
dropdown = ttk.Combobox(root, values=users, style="TCombobox", state="readonly", font=font_large, width=max_withTxt)
dropdown.set(translations[current_language]["placeholder"])
dropdown.grid(row=2, column=3, sticky="e", padx=10)

# Add a Button with a larger font
execute_button = tk.Button(root, text=translations[current_language]["validate"], font=font_large, command=validate_and_execute)
execute_button.grid(row=3, column=0, columnspan=6, pady=40)

root.grid_columnconfigure(0, weight=0, minsize=font.Font(family=font_link[0],size=font_link[1]).measure(translations[current_language]["language_toggle"]))
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=0)
root.grid_columnconfigure(3, weight=0)
root.grid_columnconfigure(4, weight=1)
root.grid_columnconfigure(5, weight=0)

# Run the application
root.mainloop()
