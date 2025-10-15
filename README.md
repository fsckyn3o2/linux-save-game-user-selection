# Linux Save Game User Selection

**Linux Save Game User Selection** is a Python application designed to create symbolic links (symlinks) between user folders where save games are stored. This is particularly useful in scenarios where a game does not support separate profile creation for different users.

## Features

- Easily manage save game directories for multiple users.
- Create symlinks to streamline save game selection without modifying the game itself.
- Enhance the user experience by enabling profile-like behavior in unsupported games.

## Prerequisites

Before running the application, ensure you have the following installed:

- **Python**: Version 3.11.8 or higher
- A **Linux** system with KDE desktop environment (or any similar environment supporting symlinks).

## Installation

1. Clone the repository:
   ```bash
   git clone <REPOSITORY_URL>
   ```

2. Navigate to the project directory:
   ```bash
   cd linux-save-game-user-selection
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

*(The `requirements.txt` file should include all dependencies your project requires. If it doesn’t exist yet, you can generate one by using `pip freeze > requirements.txt` after confirming the required packages.)*

## Usage

1. Run the main application script:
   ```bash
   python main.py -g <gameId> [-d <gameDir>]
   
   # -g is required
   # -d is optional
   ```

2. An application window is opening to select the user and configure the symlink for their save game folder.

## Configuration

Files config.cfg and game.cfg are used to create symlinks.

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

## Support

If you encounter any issues, feel free to open an issue in the repository or contact the maintainers.

---

Happy Gaming! 🎮