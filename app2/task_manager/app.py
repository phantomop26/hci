# from flask import Flask, render_template, request, redirect, url_for
# import sqlite3
# import os
# import csv
# from flask import jsonify, request
# app = Flask(__name__)

# # Database setup
# DATABASE = 'task_manager.db'

# def get_db():
#     """Returns a connection to the SQLite database."""
#     conn = sqlite3.connect(DATABASE)
#     conn.row_factory = sqlite3.Row
#     return conn

# # Helper function to initialize the database (you should run this only once)
# def init_db():
#     with get_db() as conn:


#         conn.execute('''CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY,
#             name TEXT,
#             email TEXT
#         )''')
#         conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
#         id INTEGER PRIMARY KEY,
#         title TEXT,
#         description TEXT,
#         assigned_to INTEGER,
#         status TEXT,
#         shared_with TEXT,
#         FOREIGN KEY (assigned_to) REFERENCES users(id)
#     );''')
#         conn.execute('''CREATE TABLE IF NOT EXISTS messages (
#             id INTEGER PRIMARY KEY,
#             sender_email TEXT,
#             receiver_email TEXT,
#             message TEXT,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#             group_name TEXT
#         )''')
#         conn.execute('''
#             CREATE TABLE IF NOT EXISTS task_assignments (
#                 task_id INTEGER,
#                 user_id INTEGER,
#                 FOREIGN KEY (task_id) REFERENCES tasks (id),
#                 FOREIGN KEY (user_id) REFERENCES users (id),
#                 PRIMARY KEY (task_id, user_id)
#             )
#             ''')
        
#         conn.execute('''
#     CREATE TABLE IF NOT EXISTS tasks_new (
#         id INTEGER PRIMARY KEY,
#         title TEXT,
#         description TEXT,
#         assigned_to INTEGER,
#         status TEXT,
#         shared_with TEXT,
#         FOREIGN KEY (assigned_to) REFERENCES users(id)
#     );
#     ''')

#     # Copy data from the old table to the new one (if any)
#     conn.execute('''
#     INSERT INTO tasks_new (id, title, description, assigned_to, status, shared_with)
#     SELECT id, title, description, assigned_to, status, shared_with FROM tasks;
#     ''')

#     # Drop the old table
#     conn.execute('DROP TABLE IF EXISTS tasks')

#     # Rename the new table to the original table name
#     conn.execute('ALTER TABLE tasks_new RENAME TO tasks')

#     print("Database initialized!")

# @app.route('/')
# def home():
#     """Home page."""
#     return render_template("home.html")

# @app.route('/dashboard')
# def dashboard():
#     """Dashboard page."""
#     return render_template("dashboard.html")

# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size: 16 MB

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return "No file part"
#     file = request.files['file']
#     if file.filename == '':
#         return "No selected file"
#     if file and allowed_file(file.filename):
#         filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         file.save(filename)
#         return "File uploaded successfully"
#     return "Invalid file type"

# @app.route('/messages', methods=['GET', 'POST'])
# def messages():
#     """Messages page where users can chat."""
#     if request.method == 'POST':
#         sender_email = request.form['sender_email']
#         receiver_email = request.form['receiver_email']
#         message = request.form['message']
#         group_name = request.form.get('group_name', None)

#         # Insert the message into the database
#         with get_db() as conn:
#             conn.execute('''INSERT INTO messages (sender_email, receiver_email, message, group_name) 
#                              VALUES (?, ?, ?, ?)''', (sender_email, receiver_email, message, group_name))

#         return redirect(url_for('messages'))
#         # Fetch all messages to display
#     with get_db() as conn:
#         messages = conn.execute("SELECT * FROM messages ORDER BY timestamp DESC").fetchall()

#     # Fetch users for private chat
#     with get_db() as conn:
#         users = conn.execute("SELECT * FROM users").fetchall()
    
#     # Fetch available group chats
#     with get_db() as conn:
#         groups = conn.execute("SELECT DISTINCT group_name FROM messages WHERE group_name IS NOT NULL").fetchall()

#     return render_template("messages.html", users=users, groups=groups, messages=messages)


# @app.route('/teams')
# def teams():
#     """Teams page."""
#     return render_template("teams.html")


# @app.route('/help')
# def help_page():
#     """Help page."""
#     return render_template("help.html")

# @app.route('/users', methods=['GET', 'POST'])
# def manage_users():
#     """Manage users."""
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']

#         # Insert new user into the database
#         with get_db() as conn:
#             conn.execute('''INSERT INTO users (name, email) VALUES (?, ?)''', (name, email))
#         return redirect(url_for('manage_users'))

#     # Fetch existing users to display
#     with get_db() as conn:
#         users = conn.execute("SELECT * FROM users").fetchall()
#     return render_template("users.html", users=users)

# @app.route('/add_group', methods=['POST'])
# def add_group():
#     """Create a new group."""
#     group_name = request.form['group_name']

#     # Insert the new group into the database
#     with get_db() as conn:
#         conn.execute('''INSERT INTO messages (group_name) VALUES (?)''', (group_name,))

#     # Redirect back to the page where the action was initiated
#     return redirect(request.referrer or url_for('messages'))

# @app.route('/add_task', methods=['POST'])
# def add_task():
#     """Add a new task."""
#     title = request.form['title']
#     description = request.form['description']
#     assigned_to = request.form.get('assigned_to')  # Single user ID
#     shared_with = request.form.get('shared_with')  # Multiple user IDs (comma separated)

#     # Convert assigned_to to integer if it's not empty
#     try:
#         assigned_to = int(assigned_to) if assigned_to else None
#     except ValueError:
#         return "Error: 'assigned_to' must be a valid user ID.", 400

#     # Split shared_with into a list of integers
#     shared_user_ids = []
#     if shared_with:
#         # Split by commas and convert each to an integer
#         shared_user_ids = [int(user_id.strip()) for user_id in shared_with.split(',') if user_id.strip().isdigit()]

#     # Validate that all user IDs in 'assigned_to' and 'shared_with' exist in the database
#     with get_db() as conn:
#         valid_users = conn.execute('SELECT id FROM users').fetchall()
#         valid_user_ids = {user['id'] for user in valid_users}

#         # Check if the 'assigned_to' user is valid
#         if assigned_to and assigned_to not in valid_user_ids:
#             return "Error: Invalid 'assigned_to' user ID.", 400
        
#         # Check if all shared user IDs are valid
#         for user_id in shared_user_ids:
#             if user_id not in valid_user_ids:
#                 return f"Error: Invalid user ID in shared_with list: {user_id}", 400

#         # Insert the task into the database
#         conn.execute('''INSERT INTO tasks (title, description, assigned_to, status, shared_with) 
#                          VALUES (?, ?, ?, ?, ?)''', 
#                      (title, description, assigned_to, "Pending", ','.join(map(str, shared_user_ids))))
    
#     return redirect(url_for('collaboration'))




# @app.route('/mark_complete/<int:task_id>')
# def mark_complete(task_id):
#     """Mark a task as complete."""
#     with get_db() as conn:
#         conn.execute("UPDATE tasks SET status = ? WHERE id = ?", ("Complete", task_id))
#     return redirect(url_for('collaboration'))


# @app.route('/chat/<chat_type>/<chat_id>', methods=['GET', 'POST'])
# def open_chat(chat_type, chat_id):
#     """Open a specific chat based on chat type (private or group)"""
#     if request.method == 'POST':
#         # Handle form submission to send a message
#         sender_email = request.form['sender_email']
#         message = request.form['message']
#         file = request.files.get('file', None)  # Handle file uploads

#         # Insert the message into the database
#         with get_db() as conn:
#             conn.execute('''INSERT INTO messages (sender_email, receiver_email, message, group_name) 
#                              VALUES (?, ?, ?, ?)''', 
#                              (sender_email, chat_id, message, chat_type))

#             # If a file is uploaded, save it (you can handle file storage here)
#             if file:
#                 file.save(f'uploads/{file.filename}')  # Save the file in the 'uploads' folder

#         return redirect(url_for('open_chat', chat_type=chat_type, chat_id=chat_id))

#     # Fetch messages from the database for the chat
#     with get_db() as conn:
#         if chat_type == 'private':
#             messages = conn.execute('''SELECT * FROM messages WHERE receiver_email = ? AND group_name IS NULL ORDER BY timestamp ASC''', (chat_id,)).fetchall()
#         else:
#             messages = conn.execute('''SELECT * FROM messages WHERE group_name = ? ORDER BY timestamp ASC''', (chat_id,)).fetchall()

#     return render_template('chat.html', messages=messages, chat_type=chat_type, chat_id=chat_id)

# def get_users():
#     conn = sqlite3.connect('peer_matching.db')
#     c = conn.cursor()
#     c.execute('SELECT * FROM users')
#     users = c.fetchall()
#     conn.close()
#     return users

# # Function to find the best match for the user based on answers
# def find_best_match(user_answers):
#     users = get_users()
#     best_match = None
#     best_score = -1
    
#     for user in users:
#         score = sum([1 for i in range(1, 6) if user[i] == user_answers[i-1]])
#         if score > best_score:
#             best_score = score
#             best_match = user
#     return best_match

# # Route for the home page (user form)
# @app.route('/find_peer')
# def index():
#     return render_template('find_peer.html')

# # # Route to handle form submission and find a match
# # @app.route('/submit', methods=['POST'])
# # def submit():
# #     user_answers = [
# #         request.form['q1'],
# #         request.form['q2'],
# #         request.form['q3'],
# #         request.form['q4'],
# #         request.form['q5']
# #     ]
    
# #     best_match = find_best_match(user_answers)
    
# #     if best_match:
# #         return render_template('find_peer.html', user=best_match)
# #     return 'No match found'

# # Route to accept the match
# # @app.route('/accept/<user_id>')
# # def accept(user_id):
# #     return f"You have accepted the match with user {user_id}"


# @app.route('/collaboration')
# def collaboration():
#     """Collaboration page."""
#     # Fetch all tasks and users from the database
#     with get_db() as conn:
#         tasks = conn.execute("SELECT * FROM tasks").fetchall()
#         users = conn.execute("SELECT * FROM users").fetchall()

#     return render_template("collaboration.html", tasks=tasks, users=users)
# @app.route('/add_collaborator', methods=['POST'])
# def add_collaborator():
#     name = request.form['name']
#     email = request.form['email']
    
#     # Insert the new collaborator (user) into the users table
#     with get_db() as conn:
#         conn.execute('''INSERT INTO users (name, email) VALUES (?, ?)''', (name, email))
    
#     # Redirect back to the collaboration page (or any other page)
#     return redirect(url_for('collaboration'))


# def read_users():
#     users = []
#     with open('users.csv', mode='r') as file:
#         reader = csv.reader(file)
#         next(reader)  # Skip header
#         for row in reader:
#             users.append(row)
#     return users

# # Route for the "Find Peer" page
# @app.route('/find_peer')
# def find_peer():
#     return render_template('find_peer.html')

# # Route for handling form submission
# @app.route('/submit', methods=['POST'])
# def submit():
#     # Collect answers from the form
#     q1 = request.form['q1']  # Name
#     q2 = request.form['q2']  # Email
#     q3 = request.form['q3']  # Favorite programming language
#     q4 = request.form['q4']  # Favorite hobby
#     q5 = request.form['q5']  # Favorite book
#     q6 = request.form['q6']  # Favorite travel destination
#     q7 = request.form['q7']  # Favorite food


#     # Match with existing users (checking how many answers match)
#     users = read_users()
#     matched_user = None
#     for user in users:
#         name, email, answers = user[0], user[1], user[2:]  # Extract name, email, and answers from the CSV
#         matches = sum([1 for i in range(5) if answers[i] == [q3, q4, q5, q6, q7][i]])

#         if matches >= 2:  # At least 3 answers match
#             matched_user = user
#             break

#     # If no matches found
#     if not matched_user:
#         warning_message = "No matches found with 1 or more answers."
#         return render_template('find_peer.html', warning_message=warning_message)

#     # If a match is found, display the matched user's details
#     return render_template('find_peer.html', user=matched_user)

# @app.route('/reject/<user_id>', methods=['GET'])
# def reject(user_id):
#     # Handle rejection logic here (e.g., delete user, mark as rejected, etc.)
#     print(f"User with ID {user_id} was rejected.")
#     # After rejecting, you can either redirect or render a page
#     return redirect(url_for('find_peer'))  # Redirect to the main page or another page

# @app.route('/accept/<user_id>', methods=['GET'])
# def accept(user_id):
#     # Handle acceptance logic here (e.g., match user, etc.)
#     print(f"User with ID {user_id} was accepted.")
#     # After accepting, you can either redirect or render a page
#     return redirect(url_for('find_peer'))  # Redirect to the main page or another page


# # Function to get all users from the database
# def get_users():
#     conn = sqlite3.connect('peer_matching.db')
#     c = conn.cursor()
#     c.execute('SELECT * FROM users')
#     users = c.fetchall()
#     conn.close()
#     return users


# if __name__ == "__main__":
#     init_db()  # Initialize the database
#     app.run(debug=True, port=8080)


from flask import Flask, g, render_template, request, redirect, url_for
import sqlite3
import os
import csv
from flask import jsonify, request
app = Flask(__name__)

DATABASE = 'task_manager.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT
        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT,
        assigned_to INTEGER,
        status TEXT,
        shared_with TEXT,
        FOREIGN KEY (assigned_to) REFERENCES users(id)
    );''')
        conn.execute('''CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            sender_email TEXT,
            receiver_email TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            group_name TEXT
        )''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS task_assignments (
                task_id INTEGER,
                user_id INTEGER,
                FOREIGN KEY (task_id) REFERENCES tasks (id),
                FOREIGN KEY (user_id) REFERENCES users (id),
                PRIMARY KEY (task_id, user_id)
            )
            ''')
        
        conn.execute('''
    CREATE TABLE IF NOT EXISTS tasks_new (
        id INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT,
        assigned_to INTEGER,
        status TEXT,
        shared_with TEXT,
        FOREIGN KEY (assigned_to) REFERENCES users(id)
    );
    ''')

    conn.execute('''
    INSERT INTO tasks_new (id, title, description, assigned_to, status, shared_with)
    SELECT id, title, description, assigned_to, status, shared_with FROM tasks;
    ''')

    conn.execute('DROP TABLE IF EXISTS tasks')

    conn.execute('ALTER TABLE tasks_new RENAME TO tasks')

    print("Database initialized!")

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return "File uploaded successfully"
    return "Invalid file type"

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        sender_email = request.form['sender_email']
        receiver_email = request.form['receiver_email']
        message = request.form['message']
        group_name = request.form.get('group_name', None)

        with get_db() as conn:
            conn.execute('''INSERT INTO messages (sender_email, receiver_email, message, group_name) 
                             VALUES (?, ?, ?, ?)''', (sender_email, receiver_email, message, group_name))

        return redirect(url_for('messages'))
    with get_db() as conn:
        messages = conn.execute("SELECT * FROM messages ORDER BY timestamp DESC").fetchall()

    with get_db() as conn:
        users = conn.execute("SELECT * FROM users").fetchall()

    with get_db() as conn:
        groups = conn.execute("SELECT DISTINCT group_name FROM messages WHERE group_name IS NOT NULL").fetchall()

    return render_template("messages.html", users=users, groups=groups, messages=messages)

@app.route('/teams')
def teams():
    return render_template("teams.html")

@app.route('/help')
def help_page():
    return render_template("help.html")

@app.route('/users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        with get_db() as conn:
            conn.execute('''INSERT INTO users (name, email) VALUES (?, ?)''', (name, email))
        return redirect(url_for('manage_users'))

    with get_db() as conn:
        users = conn.execute("SELECT * FROM users").fetchall()
    return render_template("users.html", users=users)

@app.route('/add_group', methods=['POST'])
def add_group():
    group_name = request.form['group_name']

    with get_db() as conn:
        conn.execute('''INSERT INTO messages (group_name) VALUES (?)''', (group_name,))

    return redirect(request.referrer or url_for('messages'))


@app.route('/mark_complete/<int:task_id>')
def mark_complete(task_id):
    with get_db() as conn:
        conn.execute("UPDATE tasks SET status = ? WHERE id = ?", ("Complete", task_id))
    return redirect(url_for('collaboration'))

@app.route('/chat/<chat_type>/<chat_id>', methods=['GET', 'POST'])
def open_chat(chat_type, chat_id):
    if request.method == 'POST':
        sender_email = request.form['sender_email']
        message = request.form['message']
        file = request.files.get('file', None)

        with get_db() as conn:
            conn.execute('''INSERT INTO messages (sender_email, receiver_email, message, group_name) 
                             VALUES (?, ?, ?, ?)''', 
                             (sender_email, chat_id, message, chat_type))

            if file:
                file.save(f'uploads/{file.filename}')

        return redirect(url_for('open_chat', chat_type=chat_type, chat_id=chat_id))

    with get_db() as conn:
        if chat_type == 'private':
            messages = conn.execute('''SELECT * FROM messages WHERE receiver_email = ? AND group_name IS NULL ORDER BY timestamp ASC''', (chat_id,)).fetchall()
        else:
            messages = conn.execute('''SELECT * FROM messages WHERE group_name = ? ORDER BY timestamp ASC''', (chat_id,)).fetchall()

    return render_template('messages.html', messages=messages, chat_type=chat_type, chat_id=chat_id)

def get_users():
    conn = sqlite3.connect('peer_matching.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()
    return users

def find_best_match(user_answers):
    users = get_users()
    best_match = None
    best_score = -1
    
    for user in users:
        score = sum([1 for i in range(1, 6) if user[i] == user_answers[i-1]])
        if score > best_score:
            best_score = score
            best_match = user
    return best_match

@app.route('/find_peer')
def index():
    return render_template('find_peer.html')

@app.route('/collaboration', methods=['GET', 'POST'])
def collaboration():
    with get_db() as conn:
        # Handle collaborator addition
        if request.method == 'POST' and 'name' in request.form and 'email' in request.form:
            name = request.form['name']
            email = request.form['email']
            conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        
        # Handle task addition
        if request.method == 'POST' and 'title' in request.form and 'description' in request.form:
            title = request.form['title']
            description = request.form['description']
            assigned_to = request.form['assigned_to']
            shared_with = request.form['shared_with']
            conn.execute(
                "INSERT INTO tasks (title, description, assigned_to, status, shared_with) VALUES (?, ?, ?, ?, ?)",
                (title, description, assigned_to, 'Pending', shared_with)
            )
        
        # Fetch all tasks and collaborators
        tasks = conn.execute("SELECT * FROM tasks").fetchall()
        users = conn.execute("SELECT * FROM users").fetchall()

    return render_template('collaboration.html', tasks=tasks, users=users)

@app.route('/add_collaborator', methods=['POST'])
def add_collaborator():
    name = request.form['name']
    email = request.form['email']
    
    with get_db() as conn:
        conn.execute('''INSERT INTO users (name, email) VALUES (?, ?)''', (name, email))
    
    return redirect(url_for('collaboration'))

def read_users():
    users = []
    with open('users.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            users.append(row)
    return users

@app.route('/submit', methods=['POST'])
def submit():
    q1 = request.form['q1']
    q2 = request.form['q2']
    q3 = request.form['q3']
    q4 = request.form['q4']
    q5 = request.form['q5']
    
    user_answers = [q1, q2, q3, q4, q5]
    best_match = find_best_match(user_answers)

    return render_template('match_result.html', best_match=best_match)



def load_data():
    courses = {}
    students = {}

    with open('courses.csv') as courses_file:
        reader = csv.DictReader(courses_file)
        for row in reader:
            courses[row['course_id']] = row['course_name']

    with open('students.csv') as students_file:
        reader = csv.DictReader(students_file)
        for row in reader:
            course_id = row['course_id']
            if course_id not in students:
                students[course_id] = []
            students[course_id].append(row['student_name'])

    return courses, students

COURSES, STUDENTS = load_data()

@app.route('/classes')
def classes():
    class_list = [
        {"id": course_id, "name": course_name, "count": len(STUDENTS.get(course_id, []))}
        for course_id, course_name in COURSES.items()
    ]
    return render_template('classes.html', classes=class_list)

def load_students_from_csv():
    students_by_course = {}
    with open('students.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            course_id = row['course_id']
            student_info = {'name': row['student_name'], 'email': row['email']}
            if course_id not in students_by_course:
                students_by_course[course_id] = []
            students_by_course[course_id].append(student_info)
    return students_by_course

STUDENTS = load_students_from_csv()
@app.route('/class/<course_id>')
def class_details(course_id):
    course_name = COURSES.get(course_id, "Unknown Course")
    student_list = STUDENTS.get(course_id, [])
    return render_template('class_details.html', course_name=course_name, students=student_list)



events=[]

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/get_events', methods=['GET'])
def get_events():
   return jsonify(events)

@app.route('/add_event', methods=['POST'])
def add_event():
    event_data = request.get_json()
    

    new_event = {
        'title': event_data['name'],
        'location': event_data['location'],
        'start': event_data['start'],
        'end': event_data['end'],
        'color': event_data['color'],
    }
    events.append(new_event)

    return jsonify({'status': 'success'}), 200
if __name__ == '__main__':
    app.run(debug=True)
