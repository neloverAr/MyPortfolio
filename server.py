import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, send_file, request, redirect

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name, name=page_name)


@app.route('/download-cv')
def download_cv():
    return send_file('static/NeloverResume.pdf', as_attachment=True, download_name="My-CV.pdf")


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == "POST":
        data = request.form.to_dict()
        sender_email = "neloverar@gmail.com"
        name = data['cf-name']
        body = data['cf-message']
        receiver_email = data["cf-email"]
        password = "rqfl dgkk kqac hyla"

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = sender_email
        message["Subject"] = f"New contact Message from {name}:{receiver_email}"
        
        message.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()
            return render_template('/thankyou.html', name=name)
        except Exception as e:
            return f"Error {e}"


# commands:
# python3 -m venv venv --> create virtual env, recommended when using flask
# . web\ server/bin/activate --> to activate virtual env (\ is for the space)
# export FLASK_APP=server.py  --> To determine the server
# flask run   -->Run the server
# export FLASK_DEBUG=1  --> Enabeling the debug mode
