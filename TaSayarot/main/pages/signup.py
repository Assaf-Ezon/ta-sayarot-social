from hashlib import sha256
from django.shortcuts import render, redirect
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sqlalchemy.orm import sessionmaker
from .models import PendingUsers, Users
from .template_page import MainPage
import json
import logging
import os


class Signup(MainPage):
    with open(os.path.join(os.path.dirname(__file__), 'config.json'), "r", encoding='utf-8') as config_file:
        configuration = json.load(config_file)

    @classmethod
    def view(cls, response) -> render:
        if response.method == "POST":
            Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
            session = Session()  # creates a session
            if not Signup._is_used_password(sha256(response.POST["pass"].encode()).hexdigest()):
                new_user_request = PendingUsers(name=response.POST["username"],
                                                mail=response.POST["mail"],
                                                role=response.POST["role"],
                                                release_date=response.POST["release-date"],
                                                password_hash=sha256(response.POST["pass"].encode()).hexdigest())
                session.add(new_user_request)
                session.commit()
                Signup._send_pending_mail(response.POST["mail"])
                session.close()
                return redirect('/login/')

            else:
                return render(response, "main/register-page.html", {"failed": 1})

        return render(response, "main/register-page.html", {"failed": 0})

    @staticmethod
    def _is_used_password(password) -> bool:
        Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
        session = Session()  # creates a session

        user = session.query(Users.password_hash).all()
        user_list = [value for (value,) in user]

        if password in user_list:
            return True

        return False

    @staticmethod
    def _send_pending_mail(email: str) -> None:
        message = Mail(
            from_email="tasayarot@gmail.com",
            to_emails=email,
            subject="יצירת משתמש נקלטה במערכת",
            html_content="<table width='100%' bgcolor='#f2f2f2'>"
                         "<tr>"
                         "<td></td>"
                         "<td style='background-color: #ffffff; padding: 20px;'>"
                         "<img src=" + Signup.configuration["general"]["LOGO_URL"] +
                         " alt='Your Logo' style='width: 200px;'>"
                         "<h1>ברוכים הבאים למדור סיירות!</h1>"
                         "<p>תודה שביקשת להירשם לאתרנו. הבקשה שלך נקלטה במערכת.</p>"
                         "<p>כאשר הבקשה תאושר, נשלח לך הודעה אישית.</p>"
                         "<p>תודה על בחירתך בנו.</p>"
                         "<p>בברכה,<br>מפעיל האתר</p>"
                         "</td>"
                         "<td></td>"
                         "</tr>"
                         "</table>")

        logger = logging.getLogger("mylogger")
        try:
            sg = SendGridAPIClient(api_key=Signup.configuration["sendgrid"]["API_KEY"])
            response = sg.send(message)
            logger.info(f"response status code: {response.status_code} data: {response.body}")

        except Exception as e:
            logger.info(f"Error message: {e}")
