Below is an example **README.md** you can use for your GitHub repository. Feel free to modify the wording or sections to suit your style and project needs.

---

# TODO Flask Application

A simple yet powerful TODO application built with [Flask](https://palletsprojects.com/p/flask/) and [SQLite](https://www.sqlite.org/index.html). This application allows users to create tasks with optional due dates, times, notes, and reorder them in a user-friendly way. 

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Features

1. **Add Tasks**: Create a new task with a title, an optional due date (in `MM/DD/YYYY` format), an optional due time (`HH:MM` in 24-hour format), and notes.  
2. **View and Search Tasks**: Browse all tasks in an ordered list or search by task title.  
3. **Reorder Tasks**: Move tasks up or down in the list, preserving a unique order.  
4. **Delete Tasks**: Remove completed or irrelevant tasks.  
5. **SQLite Database**: Stores tasks in a lightweight, file-based database.

---

## Prerequisites

- **Python 3.8+** (earlier versions may work, but not officially tested)
- **Flask** (2.0+)  
- **SQLite** (bundled with most Python installations but recommended to have the latest version)

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Vivek-k24/.git
   cd to-do_list_python
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Make sure your `requirements.txt` file contains:
   ```
   Flask==2.2.3
   ```
   *(Adjust versions as needed.)*

---

## Database Setup

This application uses an SQLite database named `todo.db`. By default, the schema is located in a file called `schema.sql`.

1. **Create/Initialize the database** (if you have a script or if the code handles it automatically at runtime):
   ```bash
   python server.py
   ```
   > The application checks if `todo.db` exists. If it does not, it runs the `init_db()` function, which executes `schema.sql` to create the `todo` table.

2. **Alternatively**, you can manually run the script:
   ```bash
   python
   >>> from server import init_db
   >>> init_db()
   ```
   This will create `todo.db` and the `todo` table if they don’t already exist.

---

## Running the Application

Once your database is set up and dependencies are installed, run the Flask development server:

```bash
python server.py
```

By default, the application will be accessible at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

*(You can also set environment variables like `FLASK_APP` or use `flask run`, but the provided `server.py` includes a `__main__` guard to run directly.)*

---

## Usage

### 1. Add a New Task
- Click **“Add TODO”** on the homepage.
- Enter a title (required).
- Optionally pick a date (`YYYY-MM-DD` in the date picker) and time (`HH:MM`) — these will be stored as `MM/DD/YYYY` and `HH:MM`, respectively.
- Add any additional notes if desired.
- Submit the form.

### 2. Search
- Use the search bar at the top of the main page to search tasks by title.
- The search is case-insensitive and partial matches are included.

### 3. Reorder Tasks
- Each task has up/down arrow buttons to move it above or below its neighboring tasks.
- This reordering is handled on the backend by swapping the `order` values in the SQLite database.

### 4. Delete
- Each task shows a **trash icon** to remove it permanently from the list.

---

## Project Structure

A typical layout might look like this:

```
your-repo-name/
├── app/
│   ├── server.py        # Main Flask application
│   ├── schema.sql       # Database schema for SQLite
│   ├── __init__.py      # (Optional) Package file
│   └── static/
│       └── css/
│           └── styles.css
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── add.html
│       ...
├── requirements.txt
├── README.md
└── todo.db              # Generated after init, not tracked in Git
```

- **server.py**: Defines routes (`index`, `add`, `delete`, `resort`) and handles database operations.  
- **schema.sql**: Creates the `todo` table with columns for title, due date, due time, notes, and order.  
- **templates/**: Contains your Jinja2 HTML templates (`index.html`, `add.html`, etc.).  
- **static/**: Holds static assets (CSS, JS, images, etc.).  

---

## License

This project is licensed under the [MIT License](LICENSE), which means you’re free to modify and redistribute it. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [Flask Documentation](https://flask.palletsprojects.com/) for a lightweight and easy-to-use web framework.
- [SQLite](https://www.sqlite.org/index.html) for a simple, file-based database solution.
- Community tutorials and open-source contributors for helpful code snippets and best practices.

---

Feel free to **fork** this repo and adjust the project for your own needs. Contributions are welcome. If you find a bug or want to request a new feature, please open an [issue](https://github.com/Vivek-k24/to-do_list_python/issues). Thank you for checking out the project!
