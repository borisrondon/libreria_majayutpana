import datetime
from pytz import timezone

from django_cron import CronJobBase, Schedule
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.db.models.expressions import F, Value
from django.db.models.functions import Concat

from api.models import Renta

tz = timezone("America/Bogota")


class SendExpiredRentAlerts(CronJobBase):
    schedule = Schedule(run_every_mins=settings.NOTIFICACIONES_CADA_MINUTOS)
    code = "api_cron_jobs.expired_rent_email.SendExpiredRentAlerts"  # a unique code

    def do(self):  # Se envía el correo con el token
        expired_rents_info = get_expired_rents_info()
        # print("expired_rents_info", expired_rents_info)

        for rent in expired_rents_info:
            try:
                msg = create_email(rent)
                msg.send()
                # print(rent)
            except Exception as e:
                print("[Send email error] Start --------------------------")
                print(e)
                print("[Send email error] End ----------------------------")


# Obtiene la lista de rentas vencidas, y la información del libro y estudiante
def get_expired_rents_info():
    date_now = datetime.datetime.now(tz=tz).date()
    all_expired_rents = Renta.objects.filter(
        fecha_entrega__date__lt=date_now, fecha_entregado__isnull=True
    )
    if all_expired_rents.exists():
        expired_rents_info = all_expired_rents.values(
            "estudiante__correo",
            "libro__isbn",
            "libro__nombre",
            "fecha_renta",
            "fecha_entrega",
        ).annotate(
            full_name=Concat(
                F("estudiante__nombres"), Value(" "), F("estudiante__apellidos")
            ),
            days_late=date_now - F("fecha_entrega__date"),
        )
        return expired_rents_info
    return False


# Se crea el correo a enviar
def create_email(rent_info):
    subject, from_email, to = [
        "Renta expirada - Institución Educativa Indígena Rural (I.E.I.R) #4",
        settings.EMAIL_HOST_USER,
        rent_info["estudiante__correo"],
    ]

    text_content = f"""
    Apreciada/o { rent_info["full_name"] },

    Te informamos que la renta del libro { rent_info["libro__nombre"] } con ISBN { rent_info["libro__isbn"] }
    realizada el día { rent_info["fecha_renta"].date() }, ha alcanzado la fecha límite de entrega
    y tiene { rent_info["days_late"].days } días de retraso (multa por {rent_info["days_late"].days * settings.PRECIO_POR_DIA} COP).
    """

    html_content = f"""
        <p style="width: 100%; text-align: left;">
            Apreciada/o <strong>{ rent_info["full_name"] }</strong>,

            <br><br>

            Te informamos que la renta del libro <strong>{ rent_info["libro__nombre"] }</strong>
            con <strong>ISBN { rent_info["libro__isbn"] }</strong>
            realizada el día <strong>{ rent_info["fecha_renta"].date() }</strong>, ha alcanzado la
            fecha límite de entrega y tiene <strong>{ rent_info["days_late"].days }</strong>
            días de retraso (multa por <strong>{rent_info["days_late"].days * settings.PRECIO_POR_DIA} COP</strong>).
        </p>
    """
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    return msg
