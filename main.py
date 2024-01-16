 
# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Create a Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maintenance_records.db'
db = SQLAlchemy(app)

# Define the MaintenanceRecord model
class MaintenanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    engine_hours = db.Column(db.Integer, nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)

# Create the database tables
db.create_all()

# Define the main route
@app.route('/')
def index():
    return render_template('index.html')

# Define the route for adding a new maintenance record
@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        # Get the form data
        engine_hours = request.form['engine_hours']
        service_type = request.form['service_type']
        date = request.form['date']

        # Create a new maintenance record
        new_record = MaintenanceRecord(engine_hours=engine_hours, service_type=service_type, date=date)

        # Add the new record to the database
        db.session.add(new_record)
        db.session.commit()

        # Redirect to the main page
        return redirect(url_for('index'))

    return render_template('add_record.html')

# Define the route for viewing the maintenance records
@app.route('/view_records')
def view_records():
    # Get all the maintenance records from the database
    records = MaintenanceRecord.query.all()

    # Render the view records page
    return render_template('view_records.html', records=records)

# Run the app
if __name__ == '__main__':
    app.run()
