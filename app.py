from flask import Flask, request, session, redirect, render_template, flash
from twilio.rest import Client
import random
import os  # For secure key handling

app = Flask(__name__)  # Corrected this line
app.secret_key = '6bfa0a99ba9df85ad666f9dedab399f9'  # Replace with a secure key

# Twilio credentials
TWILIO_ACCOUNT_SID = 'ACfef1a05363eb0ec59b59385b3d937afc'
TWILIO_AUTH_TOKEN = '8f6940d9209485fdae5ec85cb9ee6780'
TWILIO_PHONE_NUMBER = '+18647321325'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

otp_store = {}  # Store OTPs temporarily (for demo purposes only)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    name = request.form.get('name')  # Get the user's name
    identifier = request.form.get('identifier')
    method = request.form.get('method')
    otp = random.randint(1000, 9999)
    otp_store[identifier] = otp

    # Store name and mobile number in user_data.txt
    with open('user_data.txt', 'a') as f:
        f.write(f'Name: {name}, Mobile: {identifier}\n')

    try:
        if method == 'mobile':
            client.messages.create(
                body=f'Your OTP is {otp}',
                from_=TWILIO_PHONE_NUMBER,
                to=f'+{identifier}'
            )
        elif method == 'email':
            flash(f'Simulated email: Your OTP is {otp}')
    except Exception as e:
        flash(f'Error: {str(e)}')
        return redirect('/')

    return render_template('verify.html', identifier=identifier, method=method)

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    identifier = request.form.get('identifier')
    user_otp = request.form.get('otp')

    if otp_store.get(identifier) == int(user_otp):
        session['user'] = identifier
        flash('Login successful!')
        return redirect('/dashboard')
    else:
        flash('Invalid OTP. Please try again.')
        return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Please login first.')
        return redirect('/')
    return render_template('dashboard.html', user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully.')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
