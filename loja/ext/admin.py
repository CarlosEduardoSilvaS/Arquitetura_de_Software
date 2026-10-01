from flask import abort
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_babel import Babel
from flask_login import current_user

from loja.ext.authentication import login_manager
from loja.ext.database import db
from loja.model import Product


class AdminAccessMixin:
    """Regra única de acesso ao painel: autenticado E administrador.

    Toda view do admin deve herdar deste mixin; assim a política fica em um
    só lugar e nenhuma view nova nasce desprotegida por esquecimento.
    """

    def is_accessible(self):
        return (
            current_user.is_authenticated
            and current_user.is_active
            and current_user.is_admin
        )

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            # 401 => manda para o login e volta para cá depois (?next=...)
            return login_manager.unauthorized()
        # Autenticado, mas sem permissão (não é admin) => 403.
        abort(403)


class SecureAdminIndexView(AdminAccessMixin, AdminIndexView):
    pass


class SecureModelView(AdminAccessMixin, ModelView):
    # Proteção CSRF nos formulários de criar/editar/excluir do admin.
    form_base_class = SecureForm


def init_app(app):
    babel = Babel(app)
    admin = Admin(app, index_view=SecureAdminIndexView())
    admin.add_view(SecureModelView(Product, db.session))
