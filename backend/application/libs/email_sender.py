import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path)

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


def enviar_email_convite(destinatario_email: str, destinatario_nome: str, token: str) -> None:
    """
    Envia o e-mail de convite para criação de senha no primeiro acesso.

    Espera receber:
    - `destinatario_email`: str - e-mail do destinatário
    - `destinatario_nome`: str - nome do destinatário
    - `token`: str - token UUID único de redefinição de senha

    Lança exceção em caso de falha no envio.
    """
    link = f"{FRONTEND_URL}/primeiro-acesso?token={token}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Bem-vindo! Crie sua senha de acesso"
    msg["From"] = SMTP_USER
    msg["To"] = destinatario_email

    corpo_html = f"""
    <html>
      <body>
        <p>Olá, <strong>{destinatario_nome}</strong>!</p>
        <p>Seu cadastro foi realizado com sucesso.</p>
        <p>Clique no link abaixo para criar sua senha de acesso:</p>
        <p><a href="{link}">{link}</a></p>
        <p>Este link é de uso único e não possui data de expiração.</p>
      </body>
    </html>
    """

    msg.attach(MIMEText(corpo_html, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, destinatario_email, msg.as_string())