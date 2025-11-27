import secrets
import string

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User

from dispositivos.models import Usuario


def generate_temp_password(length=12):
    if length < 8:
        length = 8

    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    specials = "!@#$%^&*()-_=+[]{};:,.?/"

    password_chars = [
        secrets.choice(upper),
        secrets.choice(lower),
        secrets.choice(digits),
        secrets.choice(specials),
    ]

    all_chars = upper + lower + digits + specials
    for _ in range(length - 4):
        password_chars.append(secrets.choice(all_chars))

    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


def send_temp_password_email(email, username, temp_password):
    login_url = getattr(settings, "SITE_LOGIN_URL", "")
    subject = "Clave provisoria de acceso - Dulcería Lili's"
    message_lines = [
        "Hola,",
        "",
        "Se ha creado una cuenta para ti en el sistema de Dulcería Lili's.",
        "",
        f"Usuario: {username}",
        f"Clave provisoria: {temp_password}",
        "",
        "Accede al sistema en la siguiente URL:",
        login_url,
        "",
        "Por seguridad, deberás cambiar tu clave al ingresar por primera vez.",
        "",
        "No respondas a este correo.",
    ]
    message = "\n".join(message_lines)
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)
    send_mail(subject, message, from_email, [email], fail_silently=False)


def create_user_with_temp_password(username, email, first_name, last_name, rol, estado="ACTIVO", mfa_habilitado="deshabilitado"):
    temp_password = generate_temp_password()

    django_user = User.objects.create_user(
        username=username,
        email=email,
        password=temp_password,
        first_name=first_name,
        last_name=last_name,
        is_active=True,
    )

    usuario, created = Usuario.objects.get_or_create(
        email=email,
        defaults={
            "username": username,
            "nombre": first_name,
            "apellido": last_name,
            "rol": rol,
            "estado": estado,
            "mfa_habilitado": mfa_habilitado,
            "avatar": "",
        },
    )

    usuario.password = django_user.password
    usuario.password_temporal = True
    usuario.save()

    send_temp_password_email(email=email, username=username, temp_password=temp_password)

    return django_user, usuario, temp_password
