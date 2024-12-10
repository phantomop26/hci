def read_users():
    users = []
    with open('users.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            users.append(row)
    return users

@app.route('/find_peer')
def find_peer():
    return render_template('find_peer.html')

@app.route('/submit', methods=['POST'])
def submit():
    q1 = request.form['q1']
    q2 = request.form['q2']
    q3 = request.form['q3']
    q4 = request.form['q4']
    q5 = request.form['q5']
    q6 = request.form['q6']
    q7 = request.form['q7']

    users = read_users()
    matched_user = None
    for user in users:
        name, email, answers = user[0], user[1], user[2:]
        matches = sum([1 for i in range(5) if answers[i] == [q3, q4, q5, q6, q7][i]])

        if matches >= 2:
            matched_user = user
            break

    if not matched_user:
        warning_message = "No matches found with 1 or more answers."
        return render_template('find_peer.html', warning_message=warning_message)

    return render_template('find_peer.html', user=matched_user)

@app.route('/reject/<user_id>', methods=['GET'])
def reject(user_id):
    print(f"User with ID {user_id} was rejected.")
    return redirect(url_for('find_peer'))

@app.route('/accept/<user_id>', methods=['GET'])
def accept(user_id):
    print(f"User with ID {user_id} was accepted.")
    return redirect(url_for('find_peer'))

def get_users():
    conn = sqlite3.connect('peer_matching.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()
    return users
