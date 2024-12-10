
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