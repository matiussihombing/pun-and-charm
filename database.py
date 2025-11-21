import sqlite3
import random

DB_NAME = 'jokes_app.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Create Content table
    c.execute('''CREATE TABLE IF NOT EXISTS content (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL, -- 'joke' or 'pickup'
                    language TEXT NOT NULL, -- 'en' or 'id'
                    text TEXT NOT NULL,
                    status TEXT DEFAULT 'pending' -- 'approved' or 'pending'
                )''')
    
    # Create Ratings table
    c.execute('''CREATE TABLE IF NOT EXISTS ratings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content_id INTEGER,
                    score INTEGER,
                    FOREIGN KEY(content_id) REFERENCES content(id)
                )''')
    
    conn.commit()
    conn.close()

def seed_data(initial_data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Check if we already have data to avoid duplicates on restart
    c.execute('SELECT count(*) FROM content')
    if c.fetchone()[0] > 0:
        conn.close()
        return

    print("Seeding database...")
    
    for lang in ['en', 'id']:
        for type_ in ['jokes', 'pickup']:
            # Map 'jokes' to 'joke' for consistency if needed, but let's keep 'jokes'/'pickup' as types
            # Actually user code used 'jokes' and 'pickup' keys. Let's stick to that.
            items = initial_data[lang][type_]
            for text in items:
                c.execute('INSERT INTO content (type, language, text, status) VALUES (?, ?, ?, ?)', 
                          (type_, lang, text, 'approved'))
    
    conn.commit()
    conn.close()

def get_random_content(type_, language, exclude_ids=None):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    if exclude_ids is None:
        exclude_ids = []
    
    # Create placeholders for the IN clause
    placeholders = ','.join('?' for _ in exclude_ids)
    
    # Get a random approved item, excluding the ones in the list
    query = f'''
        SELECT c.id, c.text, AVG(r.score) as average_rating, COUNT(r.id) as rating_count
        FROM content c
        LEFT JOIN ratings r ON c.id = r.content_id
        WHERE c.type = ? AND c.language = ? AND c.status = 'approved'
        {f"AND c.id NOT IN ({placeholders})" if exclude_ids else ""}
        GROUP BY c.id
        ORDER BY RANDOM()
        LIMIT 1
    '''
    
    params = [type_, language]
    if exclude_ids:
        params.extend(exclude_ids)
        
    c.execute(query, params)
    row = c.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None

def get_pending_content():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM content WHERE status = 'pending' ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_content_status(content_id, status):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE content SET status = ? WHERE id = ?", (status, content_id))
    conn.commit()
    conn.close()
    return True

def delete_content(content_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM content WHERE id = ?", (content_id,))
    conn.commit()
    conn.close()
    return True

def add_rating(content_id, score):
    if score < 1 or score > 5:
        return False
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO ratings (content_id, score) VALUES (?, ?)', (content_id, score))
    conn.commit()
    conn.close()
    return True

def submit_content(type_, language, text):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO content (type, language, text, status) VALUES (?, ?, ?, ?)', 
              (type_, language, text, 'pending'))
    conn.commit()
    conn.close()
    return True
