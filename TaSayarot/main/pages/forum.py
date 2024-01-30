from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from sqlalchemy.orm import sessionmaker
from .models import Users, Forums
from .template_page import MainPage
import datetime as dt


class Forum(MainPage):
    selected_forum_name = "sayarot"

    @staticmethod
    @login_required(login_url="/login/")
    def view(response) -> render:
        Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
        session = Session()  # creates a session

        account = session.query(Users).filter_by(name=response.user.username).first()

        if response.method == "POST":
            if response.POST.get("submit") == "forum":
                Forum.selected_forum_name = response.POST["options"]

        session.close()
        return render(response, "main/forum-page.html", {"online": Forum._get_online_users(),
                                                         "offline": Forum._get_offline_users(),
                                                         "name": response.user.username,
                                                         "role": account.role,
                                                         "image": account.profile_image,
                                                         "username_list_json": Forum._get_all_users(),
                                                         "messeges": Forum._get_all_messeges(
                                                             Forum.selected_forum_name),
                                                         "option": Forum.selected_forum_name})

    @classmethod
    def _get_all_messeges(cls, forum_name) -> dict:
        Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
        session = Session()  # creates a session

        all_messeges = session.query(Forums).filter_by(forum_name=forum_name).all()
        my_dict = {}

        for messege in all_messeges:
            my_dict[f"{messege.message_id} | {messege.name}"] = messege.text

        session.close()
        return my_dict

    @classmethod
    def add_msg(cls, username: str, forum_name: str, msg: str) -> None:
        Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
        session = Session()  # creates a session

        account = session.query(Users).filter_by(name=username).first()

        new_msg = Forums(
            name=username,
            role=account.role,
            forum_name=forum_name,
            post_date=dt.date.today(),
            text=msg
        )
        session.add(new_msg)
        session.commit()
        session.close()
