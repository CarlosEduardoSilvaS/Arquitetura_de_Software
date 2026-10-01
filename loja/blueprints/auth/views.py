from urllib.parse import urlsplit

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from loja.ext.authentication import authenticate
from .forms import LoginForm, LogoutForm


def is_safe_redirect_target(target: str | None) -> bool:
    """Aceita apenas caminhos relativos do próprio site (evita open redirect)."""
    if not target or "\\" in target:
        return False
    parts = urlsplit(target)
    return (
        not parts.scheme
        and not parts.netloc
        and target.startswith("/")
        and not target.startswith("//")
    )


def _default_destination() -> str:
    if current_user.is_admin:
        return url_for("admin.index")
    return url_for("webui.index")


def _after_login_redirect():
    target = request.args.get("next")
    if is_safe_redirect_target(target):
        return redirect(target)
    return redirect(_default_destination())


def login():
    if current_user.is_authenticated:
        return _after_login_redirect()

    form = LoginForm()
    if form.validate_on_submit():
        user = authenticate(form.username.data, form.password.data)
        if user is not None and login_user(user):
            return _after_login_redirect()
        # Mensagem genérica: não revela se o usuário existe.
        flash("Usuário ou senha inválidos.", "danger")

    return render_template("login.html", form=form)


def logout():
    if LogoutForm().validate_on_submit():
        logout_user()
        flash("Você saiu da sua conta.", "info")
    else:
        flash("Não foi possível encerrar a sessão. Tente novamente.", "danger")
    return redirect(url_for("webui.index"))
