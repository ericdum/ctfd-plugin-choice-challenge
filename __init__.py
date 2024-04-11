from flask import Blueprint

from CTFd.models import Challenges, db, Flags, Solves, Fails
from CTFd.plugins import register_plugin_assets_directory
from CTFd.plugins.challenges import CHALLENGE_CLASSES, BaseChallenge
from CTFd.plugins.flags import FlagException, get_flag_class
from CTFd.plugins.dynamic_challenges.decay import DECAY_FUNCTIONS, logarithmic
from CTFd.plugins.migrations import upgrade
import json
from CTFd.utils.user import get_ip

class ChoiceChallengeModel(Challenges):
    __mapper_args__ = {"polymorphic_identity": "choice"}

    id = db.Column(
        db.Integer, db.ForeignKey("challenges.id", ondelete="CASCADE"), primary_key=True
    )

    def __init__(self, *args, **kwargs):
        super(ChoiceChallengeModel, self).__init__(**kwargs)

class ChoiceChallenge(BaseChallenge):
    id = "choice"
    name = "choice"
    templates = (
        {  # Handlebars templates used for each aspect of challenge editing & viewing
            "create": "/plugins/ctfd-plugin-choice-challenge/assets/create.html",
            "update": "/plugins/ctfd-plugin-choice-challenge/assets/update.html",
            "view": "/plugins/ctfd-plugin-choice-challenge/assets/view.html",
        }
    )
    scripts = {  # Scripts that are loaded when a template is loaded
        "create": "/plugins/ctfd-plugin-choice-challenge/assets/create.js",
        "update": "/plugins/ctfd-plugin-choice-challenge/assets/update.js",
        "view": "/plugins/ctfd-plugin-choice-challenge/assets/view.js",
    }
    route = '/plugins/ctfd-plugin-choice-challenge/assets/'
    blueprint = Blueprint(
        "ctfd-plugin-choice-challenge",
        __name__,
        template_folder="templates",
        static_folder="assets",
    )
    challenge_model = ChoiceChallengeModel

    @classmethod
    def calc_attemp(self, challenge, request):
        data = request.form or request.get_json()
        submission = [data["submission"].strip()] if isinstance(data["submission"], str) else data["submission"]
        flags = Flags.query.filter_by(challenge_id=challenge.id).all()
        total = len(flags)
        correct = 0
        wrong = 0
        for sub in submission:
            try:
                found = False
                for flag in flags:
                    if get_flag_class(flag.type).compare(flag, sub):
                        found = True
                if found:
                    correct += 1
                else:
                    wrong += 1
            except FlagException as e:
                return False, str(e)
        return (total, correct, wrong)

    @classmethod
    def attempt(cls, challenge, request):
        (total, correct, wrong) = cls.calc_attemp(challenge, request)
        if wrong == 0 and correct == total:
            return True, 'Correct'
        return False, f"Incorrect ({wrong}), Correct ({correct}), Missing({total-correct})"

    @classmethod
    def solve(cls, user, team, challenge, request):
        (total, correct, wrong) = cls.calc_attemp(challenge, request)
        data = request.form or request.get_json()

        if correct >= 1:
            score = challenge.value * (correct-wrong)/total

            fails = Fails.query.filter_by(
                account_id=user.account_id, challenge_id=challenge.id
            ).count()

            challenge.value = score - (fails * challenge.value/2)

            solve = Solves(
                user_id=user.id,
                team_id=team.id if team else None,
                challenge_id=challenge.id,
                ip=get_ip(req=request),
                provided=json.dumps(data),
            )

            db.session.add(solve)
            db.session.commit()

def load(app):
    app.db.create_all()
    CHALLENGE_CLASSES['choice'] = ChoiceChallenge
    register_plugin_assets_directory(app, base_path='/plugins/ctfd-plugin-choice-challenge/assets/')

