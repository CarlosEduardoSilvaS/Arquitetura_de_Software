from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField(
        "Usuário",
        validators=[DataRequired(message="Informe o usuário."), Length(max=64)],
    )
    # max=128: evita processar senhas absurdamente longas (abuso de CPU).
    password = PasswordField(
        "Senha",
        validators=[DataRequired(message="Informe a senha."), Length(max=128)],
    )


class LogoutForm(FlaskForm):
    """Formulário vazio: existe só para validar o token CSRF do logout."""
