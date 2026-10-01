from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from loja.ext.database import db, SerializerMixin, mapped_column, Mapped

MIN_PASSWORD_LENGTH = 8


class Product(db.Model, SerializerMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(unique=True)
    price: Mapped[float]


class User(db.Model, UserMixin):
    """Usuário do sistema.

    A senha nunca é guardada em texto puro: só o hash (salgado e com custo
    computacional, via scrypt) fica em `password_hash`. Esta classe NÃO usa o
    SerializerMixin de propósito, para que o hash jamais vá parar num to_dict().
    """

    # "user" é palavra reservada em alguns SGBDs (PostgreSQL); evita o problema.
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False)
    # Sobrescreve a propriedade de UserMixin: permite desativar uma conta
    # sem apagá-la.
    is_active: Mapped[bool] = mapped_column(default=True)

    def set_password(self, raw_password: str) -> None:
        if len(raw_password) < MIN_PASSWORD_LENGTH:
            raise ValueError(
                f"A senha deve ter ao menos {MIN_PASSWORD_LENGTH} caracteres."
            )
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)


def populate_db():
    products = [
        Product(id=1, description="Resistor 470 ohms", price=0.05),
        Product(id=2, description="Arduino Nano R3", price=50.00),
        Product(id=3, description="Raspberry PI 3", price=200.00),
    ]

    db.session.add_all(products)
    db.session.commit()
