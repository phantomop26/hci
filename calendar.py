
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