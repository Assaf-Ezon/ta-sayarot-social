from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sqlalchemy.orm import sessionmaker
from .models import PendingUsers, Users, Posts, Comments, Likes
from .template_page import MainPage
import json
import logging
import os


class Admin(MainPage):
    with open(os.path.join(os.path.dirname(__file__), 'config.json'), "r", encoding='utf-8') as config_file:
        configuration = json.load(config_file)

    @classmethod
    def view(cls, response) -> render:
        if response.user.username == Admin.configuration["admin"]["NAME"]:
            Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
            session = Session()  # creates a session

            if response.method == "POST":
                if response.POST.get("delete-post"):
                    try:
                        post_id = response.POST["delete-box"]
                        delete_likes = session.query(Likes).filter_by(post_id=post_id).all()
                        for like in delete_likes:
                            session.delete(like)

                        delete_comments = session.query(Comments).filter_by(post_id=post_id).all()
                        for comment in delete_comments:
                            session.delete(comment)

                        post = session.query(Posts).filter_by(post_id=post_id).first()
                        session.delete(post)

                        session.commit()

                    except Exception as e:
                        logger = logging.getLogger("mylogger")
                        logger.info(f"Error message: {e}")

                for (key, value) in Admin._get_pending_accounts().items():
                    if response.POST.get(f"action{key}") == "accept":
                        Admin._add_to_users(key)
                        Admin._send_approved_mail(session.query(PendingUsers).filter_by(personID=key).first().mail)
                        Admin._delete_from_pending(key)
                    if response.POST.get(f"action{key}") == "decline":
                        Admin._send_unapproved_mail(
                            session.query(PendingUsers).filter_by(personID=key).first().mail)
                        Admin._delete_from_pending(key)

            account = session.query(Users).filter_by(name=response.user.username).first()

            session.close()
            return render(response, "main/admin-page.html", {"pending": Admin._get_pending_accounts(),
                                                             "online": Admin._get_online_users(),
                                                             "offline": Admin._get_offline_users(),
                                                             "name": response.user.username,
                                                             "role": account.role,
                                                             "image": account.profile_image,
                                                             "username_list_json": Admin._get_all_users()})

        else:
            return redirect('/')

    @classmethod
    def _get_pending_accounts(cls) -> dict:
        Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
        session = Session()  # creates a session

        pending_accounts = session.query(PendingUsers).all()

        accounts = {}
        for account in pending_accounts:
            accounts[account.personID] = f"{account.release_date} | {account.mail} | {account.name} | {account.role}"

        session.close()
        return accounts

    @classmethod
    def _delete_from_pending(cls, key: str) -> None:
        Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
        session = Session()  # creates a session

        pending_accounts = session.query(PendingUsers).filter_by(personID=key).first()
        session.delete(pending_accounts)
        session.commit()

        session.close()

    @classmethod
    def _add_to_users(cls, key: str) -> None:
        Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
        session = Session()  # creates a session

        pending_accounts = session.query(PendingUsers).filter_by(personID=key).first()

        user = User.objects.create_user(username=pending_accounts.name, password=pending_accounts.password_hash)
        user.save()

        new_user = Users(name=pending_accounts.name,
                         email=pending_accounts.mail,
                         role=pending_accounts.role,
                         release_date=pending_accounts.release_date,
                         profile_image=Admin.configuration["general"]["DEFAULT_URL"],
                         password_hash=pending_accounts.password_hash,
                         posts_num=0,
                         likes_num=0,
                         status=0)
        session.add(new_user)
        session.commit()

        session.close()

    @staticmethod
    def _send_approved_mail(email: str) -> None:
        message = Mail(
            from_email="tasayarot@gmail.com",
            to_emails=email,
            subject="נוצר משתמש בהצלחה",
            html_content="<table width='100%' bgcolor='#f2f2f2'>"
                         "<tr>"
                         "<td></td>"
                         "<td style='background-color: #ffffff; padding: 20px;'>"
                         "<img src=" + Admin.configuration["general"]["LOGO_URL"] +
                         " alt='Your Logo' style='width: 200px;'>"
                         "<h1>ברוכים הבאים למדור סיירות!</h1>"
                         "<p>ההרשמה שלך אושרה בהצלחה. עכשיו תוכל להתחבר ולהנות מהשירותים שלנו</p>"
                         "<p>מקווים לראותך בקרוב!</p>"
                         "<p>תודה על בחירתך בנו.</p>"
                         "<p>בברכה,<br>מפעיל האתר</p>"
                         "</td>"
                         "<td></td>"
                         "</tr>"
                         "</table>")

        logger = logging.getLogger("mylogger")
        try:
            sg = SendGridAPIClient(Admin.configuration["sendgrid"]["API_KEY"])
            response = sg.send(message)
            logger.info(f"response status code: {response.status_code}")

        except Exception as e:
            logger.info(f"Error message: {e}")

    @staticmethod
    def _send_unapproved_mail(email: str) -> None:
        message = Mail(
            from_email="tasayarot@gmail.com",
            to_emails=email,
            subject="משתמש מדור סיירות נדחה",
            html_content="<table width='100%' bgcolor='#f2f2f2'>"
                         "<tr>"
                         "<td></td>"
                         "<td style='background-color: #ffffff; padding: 20px;'>"
                         "<img src=" + Admin.configuration["general"]["LOGO_URL"] +
                         " alt='Your Logo' style='width: 200px;'>"
                         "<h1>ברוכים הבאים למדור סיירות!</h1>"
                         "<p>שלום רב,</p>"
                         "<p>אנו מתנצלים לבשר לך שההרשמה שלך נדחתה. עשויות לכך מספר סיבות שונות.</p>"
                         "<p>אנא צור איתנו קשר אם יש לך שאלות או בקשות נוספות.</p>"
                         "<p>בברכה,<br>מפעיל האתר</p>"
                         "</td>"
                         "<td></td>"
                         "</tr>"
                         "</table>")

        logger = logging.getLogger("mylogger")
        try:
            sg = SendGridAPIClient(Admin.configuration["sendgrid"]["API_KEY"])
            response = sg.send(message)
            logger.info(f"response status code: {response.status_code}")

        except Exception as e:
            logger.info(f"Error message: {e}")
