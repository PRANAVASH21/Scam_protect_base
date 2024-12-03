from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Complaint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complaints.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

# Admin credentials
ADMIN_USERNAME = "Admin"
ADMIN_PASSWORD_HASH = generate_password_hash("Pass")  # Secure password storage

db.init_app(app)  # Initialize SQLAlchemy with the app

@app.before_first_request
def create_tables():
    db.create_all()  # Creates database tables if they don't exist

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/scam', methods=['GET', 'POST'])
def scam():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        scam_type = request.form['scam_type']
        incident = request.form['incident']
        complaint = Complaint(type='SCAM', name=name, address=address, scam_type=scam_type, incident=incident)
        db.session.add(complaint)
        db.session.commit()
        print("Received SCAM report: {}, {}, {}, {}".format(name, address, scam_type, incident))
        return redirect(url_for('submitted'))
    return render_template('scam_form.html')

@app.route('/phishing', methods=['GET', 'POST'])
def phishing():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phishing_type = request.form['phishing_type']
        incident = request.form['incident']
        complaint = Complaint(type='PHISHING', name=name, address=address, phishing_type=phishing_type, incident=incident)
        db.session.add(complaint)
        db.session.commit()
        print("Received PHISHING report: {}, {}, {}, {}".format(name, address, phishing_type, incident))
        return redirect(url_for('submitted'))
    return render_template('phishing_form.html')

@app.route('/extortion', methods=['GET', 'POST'])
def extortion():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        extortion_type = request.form['extortion_type']
        incident = request.form['incident']
        complaint = Complaint(type='EXTORTION', name=name, address=address, extortion_type=extortion_type, incident=incident)
        db.session.add(complaint)
        db.session.commit()
        print("Received EXTORTION report: {}, {}, {}, {}".format(name, address, extortion_type, incident))
        return redirect(url_for('submitted'))
    return render_template('extortion_form.html')

@app.route('/others', methods=['GET', 'POST'])
def others():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        incident = request.form['incident']
        complaint = Complaint(type='OTHER', name=name, address=address, incident=incident)
        db.session.add(complaint)
        db.session.commit()
        print("Received OTHER report: {}, {}, {}".format(name, address, incident))
        return redirect(url_for('submitted'))
    return render_template('others_form.html')

@app.route('/submitted')
def submitted():
    return render_template('submitted.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid credentials, please try again!", 401
    return render_template('admin_login.html')

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))

    complaints = Complaint.query.all()  # Fetch all complaints from the database

    # Handle individual delete form submission
    if request.method == 'POST':
        complaint_id = request.form.get('complaint_id')  # Get complaint_id from the form
        if complaint_id:
            complaint = Complaint.query.get(complaint_id)
            if complaint:
                db.session.delete(complaint)
                db.session.commit()
                return redirect(url_for('admin_dashboard'))

    return render_template('admin_dashboard.html', complaints=complaints)

@app.route('/admin/edit/<int:complaint_id>', methods=['GET', 'POST'])
def edit_complaint(complaint_id):
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))

    complaint = Complaint.query.get_or_404(complaint_id)  # Get complaint by ID

    if request.method == 'POST':
        complaint.name = request.form['name']
        complaint.address = request.form['address']
        complaint.scam_type = request.form.get('scam_type')
        complaint.phishing_type = request.form.get('phishing_type')
        complaint.extortion_type = request.form.get('extortion_type')
        complaint.incident = request.form['incident']
        
        db.session.commit()  # Save changes to the database
        return redirect(url_for('admin_dashboard'))

    return render_template('edit_complaint.html', complaint=complaint)

@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
