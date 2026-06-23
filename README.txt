P&C Solutions - Flask Website (Blue/Dark Theme)
--------------------------------------------------

What's included:
- app.py - Flask application
- templates/ - Jinja2 templates (base, index, services, contact)
- static/style.css - site CSS
- sent_messages.txt (created automatically if SMTP not configured) - fallback storage for messages

How to run (development):
1. Create a Python virtual environment and install Flask:
   python -m venv venv
   source venv/bin/activate  # on Windows use `venv\Scripts\activate`
   pip install Flask

2. (Optional) Configure SMTP to enable real email sending. The app reads SMTP settings from environment variables:
   - CONTACT_EMAIL (default: pcsolutions800@gmail.com)
   - SMTP_HOST
   - SMTP_PORT (default: 587)
   - SMTP_USERNAME
   - SMTP_PASSWORD
   - SMTP_USE_TLS (True/False)
   - FLASK_SECRET_KEY (to override the default secret key)

   Example (Linux/macOS):
   export SMTP_HOST=smtp.example.com
   export SMTP_PORT=587
   export SMTP_USERNAME=your_smtp_username
   export SMTP_PASSWORD=your_smtp_password
   export CONTACT_EMAIL=pcsolutions800@gmail.com
   export FLASK_SECRET_KEY=change-me

3. Run the app:
   python app.py
   Open http://127.0.0.1:5000 in your browser.

Notes:
- If SMTP is not configured the contact form saves messages to `sent_messages.txt` in the project root.
- For production use, configure a proper WSGI server (gunicorn/uwsgi) and secure your secret keys and SMTP credentials.
