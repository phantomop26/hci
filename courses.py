

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
