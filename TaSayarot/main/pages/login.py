from hashlib import sha256
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from sqlalchemy.orm import sessionmaker
from .models import Users
from .template_page import MainPage
import json
import os


class Login(MainPage):
    with open(os.path.join(os.path.dirname(__file__), 'config.json'), "r", encoding='utf-8') as config_file:
        configuration = json.load(config_file)

    @classmethod
    def view(cls, response) -> render:
        if response.method == "POST":
            username = response.POST["username"]
            password = response.POST["pass"]

            user = authenticate(username=username, password=sha256(password.encode()).hexdigest())

            if user is not None:
                Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
                session = Session()  # creates a session
                remember_me = response.POST.get("rememberMe")
                if remember_me:
                    response.session.set_expiry(604800)

                login(response, user)
                status_user = session.query(Users).filter_by(name=user.username).first()
                status_user.status = 1
                session.commit()
                session.close()
                return redirect('/')

            else:
                return render(response, "main/login-page.html", {"failed": 1})

        return render(response, "main/login-page.html", {"failed": 0})

    @classmethod
    def authenticate_user(cls, username, password) -> bool:
        Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
        session = Session()  # creates a session

        column_values = session.query(Users.name).all()
        values_list = [value for (value,) in column_values]

        if username in values_list:
            user = session.query(Users).filter_by(name=username).first()
            session.close()
            if user:
                if user.password_hash == sha256(password.encode()).hexdigest():
                    return True

        session.close()
        return False
