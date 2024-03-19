from flask import Blueprint

from CTFd.models import Challenges, db, Flags
from CTFd.plugins import register_plugin_assets_directory
from CTFd.plugins.challenges import CHALLENGE_CLASSES, BaseChallenge
from CTFd.plugins.flags import FlagException, get_flag_class
from CTFd.plugins.dynamic_challenges.decay import DECAY_FUNCTIONS, logarithmic
from CTFd.plugins.migrations import upgrade

class ChoiceChallengeModel(Challenges):
    __mapper_args__ = {'polymorphic_identity': 'choice'}
    id = db.Column(None, db.ForeignKey('challenges.id', ondelete="CASCADE"), primary_key=True)
    # initial = db.Column(db.Integer)
    # minimum = db.Column(db.Integer)
    # decay = db.Column(db.Integer)

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
    def read(cls, challenge):
        challenge = cls.challenge_model.query.filter_by(id=challenge.id).first()
        data = {
            "id": challenge.id,
            "name": challenge.name,
            "value": challenge.value,
            "description": challenge.description,
            "connection_info": challenge.connection_info,
            "next_id": challenge.next_id,
            "category": challenge.category,
            "state": challenge.state,
            "max_attempts": challenge.max_attempts,
            "type": challenge.type,
            "type_data": {
                "id": cls.id,
                "name": cls.name,
                "templates": cls.templates,
                "scripts": cls.scripts,
            },
        }
        return data

    @classmethod
    def attempt(cls, challenge, request):
        """
        This method is used to check whether a given input is right or wrong. It does not make any changes and should
        return a boolean for correctness and a string to be shown to the user. It is also in charge of parsing the
        user's input from the request itself.

        :param challenge: The Challenge object from the database
        :param request: The request the user submitted
        :return: (boolean, string)
        """
        # data = request.form or request.get_json()
        # submission = data["submission"].strip()
        # flags = Flags.query.filter_by(challenge_id=challenge.id).all()
        # for flag in flags:
        #     try:
        #         if get_flag_class(flag.type).compare(flag, submission):
        #             return True, "Correct"
        #     except FlagException as e:
        #         return False, str(e)
        # return False, "Incorrect"
        print('============= attempt ============')
        print(challenge, request)
        return super().attempt(challenge, request)


    @classmethod
    def solve(cls, user, team, challenge, request):
        print('============= solve ============')
        print(user, team, challenge, request)
        super().solve(user, team, challenge, request)


def load(app):
    app.db.create_all()
    CHALLENGE_CLASSES['choice'] = ChoiceChallenge
    register_plugin_assets_directory(app, base_path='/plugins/ctfd-plugin-choice-challenge/assets/')

