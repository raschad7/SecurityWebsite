from flask import Blueprint, request, render_template, redirect, url_for, flash, session
import requests

auth = Blueprint('auth', __name__)

FIREBASE_API_KEY = 'AIzaSyC6iVcb6xk25qwVmbYDW6CFvrnNNCIq8UQ'  # ← Replace with your real key

@auth.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        try:
            r = requests.post(
                f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}",
                json=payload
            )
            data = r.json()

            if 'idToken' in data:
                session['user'] = data['email']
                flash('Login successful', 'success')
                return redirect(url_for('views.dashboard'))
            else:
                flash(data.get('error', {}).get('message', 'Login failed'), 'danger')

        except Exception as e:
            flash(str(e), 'danger')

    return render_template('login.html')

@auth.route('/logout')
def logout_view():
    session.pop('user', None)
    flash('Logged out successfully', 'info')
    return redirect(url_for('auth.login_view'))
