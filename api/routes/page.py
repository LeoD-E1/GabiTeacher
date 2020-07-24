from flask import render_template, session, send_file
import json
from api.routes.auth import auth
from api.commons.env import env
from api.database import controller


def contact(req):
    return render_template("contact.html", contact_emails=env.get("CONTACT_EMAILS"))


def favicon(req):
    return send_file("public/img/favicon.png")


def home(req):

    # card = controller.mongo.db.learn.find_one({'title':'Verb Tenses'})
    card = controller.mongo.db.learn.aggregate(
        [
            {
                "$project": {
                    "items": {
                        "$filter": {
                            "input": "$tenses",
                            "as": "item",
                            "cond": {"$eq": ["$$item.title", "Presente Simple"]},
                        }
                    }
                }
            }
        ]
    )
    for doc in card:
        print(doc)
    return render_template("index.html", card=card)


def get_started(req):
    return render_template("get_started.html")


def grammar(req):
    return render_template("grammar.html")


def simple_present(req):
    return render_template("simple_present.html")


@auth
def dashboard(req):
    return render_template(
        "profile-user.html",
        userinfo=session["profile"],
        userinfo_pretty=json.dumps(session["jwt_payload"], indent=4),
    )
