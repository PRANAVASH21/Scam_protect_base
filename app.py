from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# SCAM Report Form Route
@app.route('/scam_form', methods=['GET', 'POST'])
def scam_form():
    if request.method == 'POST':
        # Capture form data
        name = request.form['name']
        address = request.form['address']
        scammer_number = request.form['scammer_number']  # Now it's a text input
        scam_type = request.form['scam_type']
        incident = request.form['incident']
        
        # Print received data
        print("Received SCAM report: {}, {}, {}, {}, {}".format(name, address, scammer_number, scam_type, incident))
        
        # Redirect to submission success page
        return redirect(url_for('submission_success'))
    
    return render_template('scam_form.html')

# PHISHING Report Form Route
@app.route('/phishing_form', methods=['GET', 'POST'])
def phishing_form():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phisher_number = request.form['phisher_number']  # Now it's a text input
        phishing_type = request.form['phishing_type']
        incident = request.form['incident']
        
        print("Received PHISHING report: {}, {}, {}, {}, {}".format(name, address, phisher_number, phishing_type, incident))
        
        return redirect(url_for('submission_success'))
    
    return render_template('phishing_form.html')

# EXTORTION Report Form Route
@app.route('/extortion_form', methods=['GET', 'POST'])
def extortion_form():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        extortionist_number = request.form['extortionist_number']  # Now it's a text input
        extortion_type = request.form['extortion_type']
        incident = request.form['incident']
        
        print("Received EXTORTION report: {}, {}, {}, {}, {}".format(name, address, extortionist_number, extortion_type, incident))
        
        return redirect(url_for('submission_success'))
    
    return render_template('extortion_form.html')

# OTHER Report Form Route
@app.route('/other_form', methods=['GET', 'POST'])
def other_form():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        incident = request.form['incident']
        
        print("Received OTHER report: {}, {}, {}".format(name, address, incident))
        
        return redirect(url_for('submission_success'))
    
    return render_template('other_form.html')

# Submission Success Page
@app.route('/submission_success')
def submission_success():
    return render_template('submission_success.html')

if __name__ == '__main__':
    app.run(debug=True)
