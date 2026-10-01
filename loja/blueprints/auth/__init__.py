from flask import Blueprint
from flask_login import current_user

from .forms import LogoutForm
from .views import login, logout

bp = Blueprint("auth", __name__, template_folder="templates",
               url_prefix="/auth",
    )

bp.add_url_rule("/login", view_func=login, endpoint="login",
                methods=["GET", "POST"])
# Logout só por POST (+ CSRF): um link/imagem de terceiros não desloga ninguém.
bp.add_url_rule("/logout", view_func=logout, endpoint="logout",
                methods=["POST"])


@bp.app_context_processor
def inject_logout_form():
    """Disponibiliza `logout_form` nos templates (botão "Sair" da navbar).

    Atenção: NÃO expor uma função global chamada `csrf_token`. O Flask-Admin
    injeta um <input name="csrf_token"> extra quando ela existe, o que
    duplica o campo e quebra os formulários do painel.
    """
    if current_user.is_authenticated:
        return {"logout_form": LogoutForm()}
    return {}


def init_app(app):
    app.register_blueprint(bp)
