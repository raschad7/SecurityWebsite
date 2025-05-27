from flask import Blueprint, render_template, session, redirect, url_for, Response, stream_with_context, jsonify
import requests, time, psutil, os

views = Blueprint('views', __name__)

# ──────────────────────────────────────────────
#  CAMERA PROXY  (MJPEG forwarded from Pi)
# ──────────────────────────────────────────────
@views.route('/cam')
def camera_proxy():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    try:
        stream = requests.get(
            "http://192.168.1.107:5000/",  # Pi stream URL
            stream=True,
            timeout=5
        )
        return Response(
            stream_with_context(stream.iter_content(chunk_size=1024)),
            content_type=stream.headers.get("Content-Type", "multipart/x-mixed-replace")
        )
    except requests.exceptions.RequestException:
        return "Camera feed unavailable", 503




# ──────────────────────────────────────────────
#  STANDARD PAGES
# ──────────────────────────────────────────────
@views.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('index.html')


@views.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')
