from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from sqlalchemy.orm import sessionmaker
from .models import Users
from .template_page import MainPage
import boto3


class Profile(MainPage):
    @staticmethod
    @login_required(login_url="/login/")
    def view(response) -> render:
        if response.method == "POST":
            if response.POST.get("log") == "logout":
                Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
                session = Session()  # creates a session
                status_user = session.query(Users).filter_by(name=response.user.username).first()
                status_user.status = 0
                session.commit()
                session.close()
                logout(response)
                return redirect('/login/')

            elif response.POST.get("change") == "picture":
                Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
                session = Session()  # creates a session
                file = response.FILES['file']
                file_path = f"assets/proflie-pages/{file.name}"
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )
                s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, file_path)
                status_user = session.query(Users).filter_by(name=response.user.username).first()
                status_user.profile_image = (f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3."
                                             f"{settings.AWS_S3_REGION_NAME}.amazonaws.com/{file_path}")
                session.commit()
                session.close()

        return render(response, "main/account-page.html", Profile._get_details(response.user.username))

    @classmethod
    def _get_details(cls, name) -> dict:
        Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
        session = Session()  # creates a session

        account = session.query(Users).filter_by(name=name).first()
        session.close()
        return {"name": account.name, "email": account.email, "role": account.role,
                "release_date": account.release_date, "posts": account.posts_num, "likes": account.likes_num,
                "online": Profile._get_online_users(), "offline": Profile._get_offline_users(),
                "image": account.profile_image, "username_list_json": Profile._get_all_users()}
