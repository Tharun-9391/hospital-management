from flask import Flask, render_template, request, redirect, url_for, session
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Helper functions to read and write CSV files
def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        return list(csv.DictReader(csvfile))

def write_csv(file_path, data, fieldnames):
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(data)

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        city = request.form['city']
        phone = request.form['phone']
        
        # Example of saving user to CSV (replace with actual saving logic)
        with open('patients.csv', 'a', newline='') as csvfile:
            fieldnames = ['name', 'age', 'gender', 'city', 'phone']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'name': name, 'age': age, 'gender': gender, 'city': city, 'phone': phone})
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username  # Store username in session
        return redirect(url_for('patient_dashboard'))
    
    return render_template('login.html')

# Route to render user dashboard
@app.route('/patient_dashboard')
def patient_dashboard():
    if 'username' in session:
        username = session['username']
        # Assuming user details are stored in 'patients.csv'
        patients = read_csv('patients.csv')
        user = next((patient for patient in patients if patient['name'] == username), None)
        
        if user:
            # Fetching appointments for the logged-in user from 'appointments.csv'
            appointments = read_csv('appointments.csv')
            user_appointments = [appt for appt in appointments if appt['logged_in_user'] == username]

            # Sample hospitals and descriptions
            hospitals = {
                "Tharun Speciality Hospitals": "we are with best top qualified doctors",
                "Jani Speciality Hospitals": "we are with best top qualified doctors",
                "Abhinay Speciality Hospitals": "we are with best top qualified doctors",
                "Karthik Speciality Hospitals": "we are with best top qualified doctors",
                "RVTS Speciality Hospitals": "we are with best top qualified doctors"
            }

            return render_template('patient_dashboard.html', name=user['name'], age=user['age'], gender=user['gender'],
                                   city=user['city'], phone=user['phone'], appointments=user_appointments, hospitals=hospitals)
    
    return redirect(url_for('login'))

# Route to show hospital details and book appointment form
@app.route('/hospital/<hospital_name>', methods=['GET', 'POST'])
def hospital(hospital_name):
    if 'username' in session:
        if request.method == 'POST':
            # Handle appointment booking logic here
            user = session['username']
            doctor = request.form['doctor']
            date = request.form['date']
            time = request.form['time']
            reason = request.form['reason']
            name = request.form['name']
            age = request.form['age']
            gender = request.form['gender']
            city = request.form['city']
            phone = request.form['phone']

            # Example of saving appointment to CSV (replace with actual saving logic)
            with open('appointments.csv', 'a', newline='') as csvfile:
                fieldnames = ['hospital', 'name', 'age', 'gender', 'city', 'phone', 'date', 'time', 'reason', 'doctor', 'logged_in_user']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({
                    'hospital': hospital_name,
                    'name': name,
                    'age': age,
                    'gender': gender,
                    'city': city,
                    'phone': phone,
                    'date': date,
                    'time': time,
                    'reason': reason,
                    'doctor': doctor,
                    'logged_in_user': user
                })

            return redirect(url_for('patient_dashboard'))

        # Fetching doctors for the hospital from 'doctors.csv'
        doctors = []
        with open('doctors.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['hospital'] == hospital_name:
                    doctors.append(row['name'])

        return render_template('appointment.html', hospital=hospital_name, doctors=doctors)

    return redirect(url_for('login'))
# Route for user logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Route for doctor login
@app.route('/doctor_login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        doctor_name = request.form['doctor_name']
        doctor_phone = request.form['doctor_phone']
        
        # Implement logic to verify doctor login (e.g., check against a doctor database)
        # Assuming doctor details are stored in 'doctors.csv'
        doctors = read_csv('doctors.csv')
        authenticated_doctor = next((doctor for doctor in doctors if doctor['name'] == doctor_name and doctor['phone'] == doctor_phone), None)
        
        if authenticated_doctor:
            session['doctor_name'] = authenticated_doctor['name']
            return redirect(url_for('doctor_dashboard'))
        else:
            return render_template('doctor_login.html', error=True)
    
    return render_template('doctor_login.html', error=False)

# Route to render doctor dashboard
@app.route('/doctor_dashboard')
def doctor_dashboard():
    if 'doctor_name' in session:
        doctor_name = session['doctor_name']
        # Assuming doctor appointments are stored in 'appointments.csv'
        appointments = read_csv('appointments.csv')
        doctor_appointments = [appt for appt in appointments if appt['doctor'] == doctor_name]

        return render_template('doctor_dashboard.html', doctor_name=doctor_name, appointments=doctor_appointments)
    
    return redirect(url_for('doctor_login'))

if __name__ == '__main__':
    app.run(debug=True)
