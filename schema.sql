CREATE TABLE IF NOT EXISTS nodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    avatar TEXT,
    birthday TEXT,
    sex BOOLEAN
);

CREATE TABLE IF NOT EXISTS vertices (
    id TEXT PRIMARY KEY,
    rank INTEGER NOT NULL,
    parent_id INTEGER,
    child_id INTEGER,
    FOREIGN KEY (parent_id) REFERENCES nodes (id) ON DELETE CASCADE,
    FOREIGN KEY (child_id) REFERENCES nodes (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS spouses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    node1_id INTEGER,
    node2_id INTEGER,
    FOREIGN KEY (node1_id) REFERENCES nodes (id) ON DELETE CASCADE,
    FOREIGN KEY (node2_id) REFERENCES nodes (id) ON DELETE CASCADE,
    UNIQUE (node1_id, node2_id)
);