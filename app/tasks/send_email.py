from app.celery_utils import celery_app
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


@celery_app.task
def send_email(
    subject: str,
    from_who: str,
    to_who: str,
    body_content: str,
    smtp_host: str,
    smtp_password_for_app: str,
):
    """
    Отправка письма по SMTP используя учетную запись почтового сервера Yandex
    """
    # Создаем сообщение
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = from_who
    msg["To"] = to_who
    # Прикрелпяем тело письма
    msg.attach(MIMEText(body_content, "plain"))
    # Отправляем через сервер Яндекса
    try:
        with smtplib.SMTP_SSL(smtp_host, 465) as server:
            server.login(from_who, smtp_password_for_app)
            server.send_message(msg)
            return "Письмо успешно отправлено!"
    except Exception as e:
        return str(e)
