import os
import sys

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

# Path to the SQLite database
DATABASE = os.path.join(os.path.dirname(__file__), 'todo.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Initialize the database by executing schema.sql script.
    """
    with app.app_context():
        conn = get_db_connection()
        with open(os.path.join(os.path.dirname(__file__), 'schema.sql')) as f:
            conn.executescript(f.read())
        conn.close()

@app.route('/')
def index():
    """
    Show all TODOs in sorted order by the "order" column.
    Allows an optional search query.
    """
    search_query = request.args.get('search_query', '').strip()
    conn = get_db_connection()

    if search_query:
        # Use LIKE search if there's a query
        todos = conn.execute(
            'SELECT * FROM todo WHERE title LIKE ? ORDER BY "order"',
            (f'%{search_query}%',)
        ).fetchall()
    else:
        # Otherwise, return all
        todos = conn.execute('SELECT * FROM todo ORDER BY "order"').fetchall()

    conn.close()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=('GET', 'POST'))
def add():
    """
    Add a new TODO item. 
    - New items get an "order" = current max order + 1
    - Stores due_date (MM/DD/YYYY), due_time, notes
    """
    if request.method == 'POST':
        title = request.form['title'].strip()
        due_date_input = request.form['due_date']  # 'YYYY-MM-DD' from <input type="date">
        due_time_input = request.form['due_time']  # 'HH:MM' from <input type="time">
        notes = request.form['notes'].strip() if 'notes' in request.form else None

        if title:
            # Convert to MM/DD/YYYY if date provided
            due_date_str = None
            if due_date_input:
                parsed_date = datetime.strptime(due_date_input, '%Y-%m-%d')
                due_date_str = parsed_date.strftime('%m/%d/%Y')

            # For time, store the raw value (e.g. '14:30')
            due_time_str = due_time_input.strip() if due_time_input else None

            conn = get_db_connection()

            # Get current max order
            row = conn.execute('SELECT MAX("order") AS max_order FROM todo').fetchone()
            max_order = row['max_order'] if row['max_order'] else 0

            # Insert new record, including notes
            conn.execute(
                '''
                INSERT INTO todo (title, due_date, due_time, notes, "order")
                VALUES (?, ?, ?, ?, ?)
                ''',
                (title, due_date_str, due_time_str, notes, max_order + 1)
            )
            conn.commit()
            conn.close()

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/resort/<int:id>/<string:direction>', methods=['POST'])
def resort(id, direction):
    conn = get_db_connection()
    current_todo = conn.execute('SELECT * FROM todo WHERE id = ?', (id,)).fetchone()

    if not current_todo:
        conn.close()
        return redirect(url_for('index'))

    current_order = current_todo['order']

    if direction == 'up':
        # Get the item directly above (largest order that's still less than current_order)
        above_todo = conn.execute(
            'SELECT * FROM todo WHERE "order" < ? ORDER BY "order" DESC LIMIT 1',
            (current_order,)
        ).fetchone()

        if above_todo:
            above_order = above_todo['order']
            # Perform a three-step swap to avoid UNIQUE constraint collisions
            # 1) Move the above item to a temporary unused order (e.g., -1)
            conn.execute('UPDATE todo SET "order" = -1 WHERE id = ?', (above_todo['id'],))
            
            # 2) Move the current item up
            conn.execute('UPDATE todo SET "order" = ? WHERE id = ?', (above_order, id))
            
            # 3) Move the above item down
            conn.execute('UPDATE todo SET "order" = ? WHERE id = ?', (current_order, above_todo['id']))

    elif direction == 'down':
        # Get the item directly below (smallest order that's still greater than current_order)
        below_todo = conn.execute(
            'SELECT * FROM todo WHERE "order" > ? ORDER BY "order" ASC LIMIT 1',
            (current_order,)
        ).fetchone()

        if below_todo:
            below_order = below_todo['order']
            # Three-step swap again
            # 1) Move the below item to a temporary unused order
            conn.execute('UPDATE todo SET "order" = -1 WHERE id = ?', (below_todo['id'],))
            
            # 2) Move the current item down
            conn.execute('UPDATE todo SET "order" = ? WHERE id = ?', (below_order, id))
            
            # 3) Move the below item up
            conn.execute('UPDATE todo SET "order" = ? WHERE id = ?', (current_order, below_todo['id']))

    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    """
    Delete a TODO item.
    """
    conn = get_db_connection()
    conn.execute('DELETE FROM todo WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/api/due_soon', methods=['GET'])
def due_soon():
    """
    API endpoint for the reminder microservice to query tasks 
    that have 'remind=1' and are due within the next 5 minutes.
    Returns JSON data.
    """
    now = datetime.now()
    in_five_minutes = now + timedelta(minutes=5)

    # Convert 'now' and 'in_five_minutes' to MM/DD/YYYY HH:MM for comparison
    # We'll do a naive approach: parse each record's due_date+due_time and compare in Python
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM todo WHERE remind=1').fetchall()

    results = []
    for row in rows:
        if row['due_date'] and row['due_time']:
            # Row due date/time is in format mm/dd/yyyy and hh:mm
            dt_str = f"{row['due_date']} {row['due_time']}"
            try:
                due_dt = datetime.strptime(dt_str, '%m/%d/%Y %H:%M')
                if now <= due_dt <= in_five_minutes:
                    results.append({
                        'id': row['id'],
                        'title': row['title'],
                        'due_date': row['due_date'],
                        'due_time': row['due_time'],
                        'notes': row['notes']
                    })
            except ValueError:
                # Malformed date/time, ignore or log
                pass

    conn.close()
    return {'due_soon': results}

# If running directly (not via a WSGI server), run the Flask dev server
if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    # Listen on all interfaces, port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)

