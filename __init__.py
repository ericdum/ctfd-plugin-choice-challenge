from flask import Blueprint

from CTFd.models import Challenges, db, Flags
from CTFd.plugins import register_plugin_assets_directory
from CTFd.plugins.challenges import CHALLENGE_CLASSES, BaseChallenge
from CTFd.plugins.flags import FlagException, get_flag_class
from CTFd.plugins.dynamic_challenges.decay import DECAY_FUNCTIONS, logarithmic
from CTFd.plugins.migrations import upgrade

class ChoiceChallengeModel(Challenges):

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


def load(app):
    app.db.create_all()
    CHALLENGE_CLASSES['choice'] = ChoiceChallenge
    register_plugin_assets_directory(app, base_path='/plugins/ctfd-plugin-choice-challenge/assets/')

