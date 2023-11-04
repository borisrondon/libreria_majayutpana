from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

# Serializar el login
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  @classmethod
  def get_token(cls, user):
    token = super().get_token(user)

    token['is_staff'] = user.is_staff
    token['first_name'] = user.first_name
    token['last_name'] = user.last_name

    return token


class MyTokenObtainPairView(TokenObtainPairView):
  serializer_class = MyTokenObtainPairSerializer


# Reseteo de contraseña
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
  # Se envía el correo con el token
  subject, from_email, to = [
    'Restablecer contraseña - Institución Educativa Indígena Rural (I.E.I.R) #4',
    settings.EMAIL_HOST_USER,
    reset_password_token.user.email
  ]
  
  text_content = f"""Hemos recibido una solicitud de cambio de contraseña
    Ingresa este código en la aplicación y tu nueva contraseña para continuar: { reset_password_token.key }
    """
  html_content = f"""
    <center style="width: 100%;">
      Hemos recibido una solicitud de cambio de contraseña 
    </center>

    <p style="width: 100%; text-align: center;">
      Ingresa este código en la aplicación y tu nueva contraseña para continuar: <strong>
        { reset_password_token.key }
      </strong>
    </p>
    """
  msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
  msg.attach_alternative(html_content, "text/html")
  try:
    msg.send()
  except Exception as e: print(e)
