# My Recipe Book

A graphical desktop application for managing your personal recipe collection.  
Built with Python and Tkinter, using an in-memory SQLite database.

---

## Features

- **Browse recipes** by category, preparation time, and portions.
- **Add, edit, and delete** recipes.
- **Filter** recipes using intuitive controls.
- **Save** your data to files for persistence.
- **Modern GUI** with hover and click effects.

---

## Installation

1. **Clone or download** this repository.
2. Make sure you have **Python 3.10+** installed.
3. Install required packages (only standard library is used: `tkinter`, `sqlite3`).

---

## Usage

1. Place the required data files in the `table/` directory:
    - `categories.dat`
    - `connect.dat`
    - `recipes.dat`
2. Place images in the `images/` and `bg/` directories as referenced in the code.
3. Run the application:

   ```bash
   python main.py
   ```

---

## Project Structure

- `main.py` — Entry point, starts the GUI.
- `Interface.py` — Main GUI logic and layout.
- `Click.py` — Handles click events.
- `Hover.py` — Handles hover (mouse-over) events.
- `Database.py` — Handles all database operations (in-memory SQLite).

- `table/` — Data files for categories, connections, and recipes.
- `images/`, `bg/` — Image assets for the GUI.

---

## Notes

- All data is loaded into memory at startup and saved back to files on exit.
- The application is designed for educational purposes and may require the correct data/image files to run properly.
- The GUI uses the "Dubai" font; if not available, Tkinter will use a default font.

---

## Author

Barbora Marcinčáková

---
