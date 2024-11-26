from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Mock database
users = ["Alice", "Bob", "Charlie"]
groups = {
    "General": [],
    "Team": [],
}
messages = {
    "Alice": [],
    "Bob": [],
    "Charlie": [],
    "General": [],
    "Team": [],
}


@app.route('/')
def index():
    # Available chats to join
    available_chats = {
        "Private Chats": users,
        "Group Chats": list(groups.keys()),
    }
    return render_template('index.html', available_chats=available_chats, users=users, groups=groups)


@app.route('/chat/<recipient>', methods=['GET', 'POST'])
def chat(recipient):
    if request.method == 'POST':
        message = request.form['message']
        messages[recipient].append({
            'sender': 'You',
            'text': message,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return redirect(url_for('chat', recipient=recipient))

    chat_messages = messages.get(recipient, [])
    return render_template('chat.html', recipient=recipient, messages=chat_messages)


@app.route('/group/<group_name>', methods=['GET', 'POST'])
def group_chat(group_name):
    if request.method == 'POST':
        message = request.form['message']
        messages[group_name].append({
            'sender': 'You',
            'text': message,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return redirect(url_for('group_chat', group_name=group_name))

    group_messages = messages.get(group_name, [])
    return render_template('chat.html', recipient=group_name, messages=group_messages)


@app.route('/join/<group_name>')
def join_group(group_name):
    # Redirect the user to the group chat page after "joining"
    if group_name in groups:
        return redirect(url_for('group_chat', group_name=group_name))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)