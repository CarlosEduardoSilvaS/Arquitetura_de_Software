from functools import cache

from flask_login import LoginManager
from werkzeug.security import check_password_hash, generate_password_hash

from loja.ext.database import db
from loja.model import User

login_manager = LoginManager()


@cache
def _dummy_hash() -> str:
    return generate_password_hash("senha-inexistente")


def normalize_username(username: str) -> str:
    return (username or "").strip().lower()


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    """Recarrega o usuário a cada requisição a partir do id guardado na sessão.

    Conta desativada => retorna None, então a sessão dela deixa de valer
    imediatamente (não precisa esperar o cookie expirar).
    """
    user = db.session.get(User, int(user_id))
    return user if user and user.is_active else None


def authenticate(username: str, password: str) -> User | None:
    """Devolve o usuário se as credenciais forem válidas; senão, None."""
    user = db.session.execute(
        db.select(User).filter_by(username=normalize_username(username))
    ).scalar()

    if user is None:
        # Gasta o mesmo tempo de uma verificação real: evita que a diferença
        # de tempo de resposta revele quais usernames existem.
        check_password_hash(_dummy_hash(), password or "")
        return None

    if not user.is_active or not user.check_password(password or ""):
        return None
    return user


def ensure_admin_user(app) -> None:
    """Garante a existência do administrador inicial (idempotente).

    As credenciais vêm da configuração (ADMIN_USERNAME / ADMIN_PASSWORD),
    nunca do código-fonte. Se o usuário já existe, não é alterado.
    """
    username = normalize_username(app.config.get("ADMIN_USERNAME", ""))
    password = app.config.get("ADMIN_PASSWORD", "")

    if not username or not password:
        app.logger.warning(
            "ADMIN_USERNAME/ADMIN_PASSWORD não configurados: "
            "nenhum administrador foi criado."
        )
        return

    with app.app_context():
        exists = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar()
        if exists:
            return
        admin = User(username=username, is_admin=True)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()


def init_app(app):
    if not app.config.get("SECRET_KEY"):
        raise RuntimeError(
            "SECRET_KEY não configurada. Defina-a em .secrets.toml (dev) ou na "
            "variável de ambiente FLASK_SECRET_KEY (produção)."
        )

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Faça login para acessar esta página."
    login_manager.login_message_category = "warning"
    login_manager.session_protection = "strong"

    ensure_admin_user(app)
