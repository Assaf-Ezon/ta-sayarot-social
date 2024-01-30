from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from sqlalchemy.orm import sessionmaker
from .models import Users
from .template_page import MainPage


class RandomProfile(MainPage):
    @staticmethod
    @login_required(login_url="/login/")
    def view(response, name) -> render:
        Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
        session = Session()  # creates a session
        account = session.query(Users).filter_by(name=name).first()
        connected_account = session.query(Users).filter_by(name=response.user.username).first()
        session.close()

        return render(response, "main/some-account-page.html", {
                                                                "connected_name": connected_account.name,
                                                                "connected_img": connected_account.profile_image,
                                                                "connected_role": connected_account.role,
                                                                "name": account.name,
                                                                "email": account.email,
                                                                "role": account.role,
                                                                "release_date": account.release_date,
                                                                "posts": account.posts_num,
                                                                "likes": account.likes_num,
                                                                "online": RandomProfile._get_online_users(),
                                                                "offline": RandomProfile._get_offline_users(),
                                                                "image": account.profile_image,
                                                                "username_list_json": RandomProfile._get_all_users()})
