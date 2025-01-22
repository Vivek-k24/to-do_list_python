CREATE TABLE IF NOT EXISTS todo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    due_date TEXT,
    due_time TEXT,
    notes TEXT,
    "order" INTEGER UNIQUE NOT NULL
);