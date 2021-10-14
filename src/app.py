from flask import Flask
from flask import render_template
from flask import request
from models import db, User, Tweet
from predict import predict_user
# import os
import spacy
from decouple import config
from twitter import add_or_update_user


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = config("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    # Create tables
    with app.app_context():
        db.create_all()
    nlp = spacy.load("my_model")

    def word2vect(text):
        return nlp(text).vector

    @app.route('/', methods=['GET', 'POST'])
    def main(message=""):
        name = request.form.get("name")
        if name:
            add_or_update_user(str(name))
        users = User.query.all()

        #     try:
        #         if request.method == 'POST':
        #             add_or_update_user(name)
        #             message = f"User @{name} successfully added!"
        #         tweets = User.query.filter(User.name == name).one().tweets
        #     except Exception as e:
        print(name)
        #         message = f"Error adding @{name}: {e}"
        #         tweets = []
        # title=name, tweets=tweets, message=message)
        return render_template('base.html', users=users)

    @ app.route('/refresh')
    def refresh():
        db.drop_all()
        db.create_all()
        return 'Database Refreshed'

    @ app.route('/compare', methods=["POST"])
    def compare():
        user0, user1 = sorted(
            [request.values['user0'], request.values["user1"]])

        if user0 == user1:
            message = "Cannot compare users to themselves!"

        else:
            # prediction returns a 0 or 1
            prediction = predict_user(
                user0, user1, request.values["tweet_text"])
            message = "'{}' is more likely to be said by {} than {}!".format(
                request.values["tweet_text"],
                user1 if prediction else user0,
                user0 if prediction else user1
            )

        return render_template('prediction.html',
                               title="Prediction", message=message)

    return app


if __name__ == "__main__":
    create_app().run()
