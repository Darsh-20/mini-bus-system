from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

# App configuration
app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = '12345'

# MySQL Configuration
mysql = MySQL(app)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = generate_password_hash(request.form['password'])
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Users (Name, Email, Phone, Role, Password) VALUES (%s, %s, %s, 'Passenger', %s)",
                       (name, email, phone, password))
        mysql.connection.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE Email = %s", (email,))
        user = cursor.fetchone()
        if user and check_password_hash(user[5], password):  # Password is in column 5
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', name=session['user_name'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/schedules')
def schedules():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT s.ScheduleID, b.BusID, 
               CONCAT(r.Source, ' to ', r.Destination) AS Route, 
               s.DepartureTime, s.ArrivalTime, s.AvailableSeats
        FROM Schedules s
        JOIN Buses b ON s.BusID = b.BusID
        JOIN Routes r ON s.RouteID = r.RouteID
    """)
    schedules = cursor.fetchall()
    return render_template(
    'schedules.html',
    schedules=[
        dict(zip([desc[0] for desc in cursor.description], row)) for row in schedules
    ]
)


@app.route('/book_ticket', methods=['GET', 'POST'])
def book_ticket():
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        schedule_id = request.form['schedule_id']
        seat_number = request.form['seat_number']
        user_id = session.get('user_id')

        cursor.execute("SELECT AvailableSeats FROM Schedules WHERE ScheduleID = %s", (schedule_id,))
        available_seats = cursor.fetchone()[0]

        if available_seats > 0:
            cursor.execute("INSERT INTO Tickets (ScheduleID, UserID, SeatNumber, BookingDate) VALUES (%s, %s, %s, NOW())",
                           (schedule_id, user_id, seat_number))
            cursor.execute("UPDATE Schedules SET AvailableSeats = AvailableSeats - 1 WHERE ScheduleID = %s", (schedule_id,))
            mysql.connection.commit()
            flash('Ticket booked successfully!', 'success')
            return redirect(url_for('schedules'))
        else:
            flash('No available seats for this schedule!', 'danger')

    cursor.execute("""
        SELECT s.ScheduleID, b.BusID, 
               CONCAT(r.Source, ' to ', r.Destination) AS Route, 
               s.DepartureTime
        FROM Schedules s
        JOIN Buses b ON s.BusID = b.BusID
        JOIN Routes r ON s.RouteID = r.RouteID
    """)
    schedules = cursor.fetchall()
    return render_template(
    'book_ticket.html',
    schedules=[
        dict(zip([desc[0] for desc in cursor.description], row)) for row in schedules
    ]
)


if __name__ == '__main__':
    app.run(debug=True)
