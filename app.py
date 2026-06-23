from flask import Flask, render_template, request, redirect, flash, url_for
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()


# ============================
# App Setup
# ============================
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-me-for-production")

# ============================
# Configuration
# ============================
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "pcsolutions800@gmail.com")
SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
SMTP_USE_TLS = os.environ.get("SMTP_USE_TLS", "True").lower() in ("1", "true", "yes")

# ============================
# Helper function to send email
# ============================
def send_email(subject, body, sender_email):
    """
    Sends an email to CONTACT_EMAIL using SMTP if configured.
    If SMTP is not configured, saves the message to a local file for development.
    """
    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = CONTACT_EMAIL
    msg["Subject"] = f"[P&C Solutions] {subject}"
    msg.set_content(body)

    if SMTP_HOST:
        try:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
                if SMTP_USE_TLS:
                    server.starttls()
                if SMTP_USERNAME and SMTP_PASSWORD:
                    server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(msg)
            return True, "Message sent successfully!"
        except Exception as e:
            return False, f"Failed to send message: {e}"
    else:
        # Fallback: save locally for development
        try:
            fallback_path = os.path.join(os.path.dirname(__file__), "sent_messages.txt")
            with open(fallback_path, "a") as f:
                f.write("-----\n")
                f.write(f"To: {CONTACT_EMAIL}\n")
                f.write(f"{body}\n")
            return False, "SMTP not configured. Message saved locally for development."
        except Exception as e:
            return False, f"Failed to save message locally: {e}"

# ============================
# Routes
# ============================
@app.route("/")
def home():
    return render_template("index.html", site_name="P&C Solutions", contact_email=CONTACT_EMAIL)

@app.route("/services")
def services():
    return render_template("services.html", site_name="P&C Solutions")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        subject = request.form.get("subject", "Service Request").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("Please fill in your name, email, and message.", "danger")
            return redirect(url_for("contact"))

        # Compose email
        body = f"""New contact form submission from {name} <{email}>

Phone: {phone}
Subject: {subject}

Message:
{message}
"""
        msg = EmailMessage()
        msg["From"] = email
        msg["To"] = CONTACT_EMAIL
        msg["Subject"] = f"[P&C Solutions] {subject}"
        msg.set_content(body)

        # Attempt sending email
        try:
            if SMTP_HOST:
                try:
                    # Try TLS first
                    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)
                    if SMTP_USE_TLS:
                        server.starttls()
                    if SMTP_USERNAME and SMTP_PASSWORD:
                        server.login(SMTP_USERNAME, SMTP_PASSWORD)
                    server.send_message(msg)
                    server.quit()
                    flash("Message sent successfully!", "success")
                except Exception as e_tls:
                    # If TLS fails, try SSL
                    try:
                        server = smtplib.SMTP_SSL(SMTP_HOST, 465, timeout=10)
                        if SMTP_USERNAME and SMTP_PASSWORD:
                            server.login(SMTP_USERNAME, SMTP_PASSWORD)
                        server.send_message(msg)
                        server.quit()
                        flash("Message sent successfully via SSL!", "success")
                    except Exception as e_ssl:
                        flash(f"Failed to send email.\nTLS error: {e_tls}\nSSL error: {e_ssl}", "danger")
            else:
                # Fallback for development
                fallback_path = os.path.join(os.path.dirname(__file__), "sent_messages.txt")
                with open(fallback_path, "a") as f:
                    f.write("-----\n")
                    f.write(f"To: {CONTACT_EMAIL}\n")
                    f.write(f"{body}\n")
                flash("SMTP not configured. Message saved locally for development.", "warning")
        except Exception as e:
            flash(f"Unexpected error: {e}", "danger")

        return redirect(url_for("contact"))

    return render_template("contact.html", site_name="P&C Solutions", contact_email=CONTACT_EMAIL)

@app.route('/about')
def about():
    return render_template('about.html', site_name="P&C Solutions", contact_email="pcsolutions800@gmail.com")


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

# ============================
# Run app
# ============================
if __name__ == "__main__":
    app.run(debug=True)
