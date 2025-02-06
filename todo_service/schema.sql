CREATE TABLE IF NOT EXISTS todo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    due_date TEXT,
    due_time TEXT,
    notes TEXT,
    remind integer DEFAULT 0,
    "order" INTEGER UNIQUE NOT NULL
);


