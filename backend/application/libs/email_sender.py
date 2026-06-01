import os
import time
import logging
import smtplib
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Tempo máximo (em segundos) de espera por cada operação SMTP, evitando que um
# servidor lento estoure o limite de 2 minutos para o envio (US-03-RNF1).
SMTP_TIMEOUT = int(os.getenv("SMTP_TIMEOUT", 30))
# Número de tentativas de envio antes de desistir.
SMTP_TENTATIVAS = int(os.getenv("SMTP_TENTATIVAS", 3))


def _enviar_mensagem(msg: MIMEMultipart, destinatario: str) -> None:
    """
    Envia uma mensagem MIME via SMTP com timeout e novas tentativas.

    Reenvia em caso de falha transitória (até `SMTP_TENTATIVAS`), aplicando um
    pequeno intervalo entre as tentativas. Levanta a última exceção caso todas
    as tentativas falhem.
    """
    ultimo_erro = None

    for tentativa in range(1, SMTP_TENTATIVAS + 1):
        try:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=SMTP_TIMEOUT) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.sendmail(SMTP_USER, destinatario, msg.as_string())
            return
        except Exception as e:
            ultimo_erro = e
            logger.warning(
                "Falha ao enviar e-mail para %s (tentativa %d/%d): %s",
                destinatario, tentativa, SMTP_TENTATIVAS, e,
            )
            if tentativa < SMTP_TENTATIVAS:
                time.sleep(2 * tentativa)

    # `ultimo_erro` só é None se o laço nunca executou (SMTP_TENTATIVAS <= 0);
    # nesse caso levantamos um erro explícito em vez de `raise None` (TypeError).
    if ultimo_erro is not None:
        raise ultimo_erro
    raise RuntimeError(
        f"Falha ao enviar e-mail para {destinatario}: nenhuma tentativa foi executada "
        f"(SMTP_TENTATIVAS={SMTP_TENTATIVAS})."
    )


def enviar_email_convite_async(destinatario_email: str, destinatario_nome: str, token: str) -> None:
    """
    Dispara o e-mail de convite em uma thread separada.

    Garante que o cadastro do usuário responda imediatamente, enquanto o envio
    (com timeout e novas tentativas) ocorre em segundo plano dentro da janela de
    2 minutos exigida pelo requisito (US-03-RNF1). Falhas definitivas são
    registradas em log.
    """
    def _run():
        try:
            enviar_email_convite(destinatario_email, destinatario_nome, token)
        except Exception as e:
            logger.error("Erro ao enviar e-mail de convite para %s: %s", destinatario_email, e)

    threading.Thread(target=_run, daemon=True).start()


def enviar_email_convite(destinatario_email: str, destinatario_nome: str, token: str) -> None:
    """
    Envia o e-mail de convite para criação de senha no primeiro acesso.

    Espera receber:
    - `destinatario_email`: str - e-mail do destinatário
    - `destinatario_nome`: str - nome do destinatário
    - `token`: str - token UUID único de redefinição de senha

    Lança exceção em caso de falha no envio.
    """
    link = f"{FRONTEND_URL}/alterar-senha?token={token}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Bem-vindo! Crie sua senha de acesso"
    msg["From"] = SMTP_FROM
    msg["To"] = destinatario_email

    corpo_html = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    </head>
    <body style="margin:0;padding:0;background-color:#f0fdfa;font-family:'DM Sans',Arial,sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f0fdfa;padding:40px 16px;">
        <tr>
          <td align="center">
            <table width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;">

              <!-- Header -->
              <tr>
                <td align="center" style="padding-bottom:24px;">
                  <table cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="padding-right:10px;vertical-align:middle;">
                        <svg width="28" height="28" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M8 0L0 0L0 14.4L8 18M8 0L8 18M8 0L10 0M8 18L10 18M10 0L18 0L18 14.4L10 18M10 0L10 18M2 4.8L6 4.8M2 8.4L6 8.4M12 4.8L16 4.8M12 8.4L16 8.4"
                            fill="white" stroke="#f97316" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                      </td>
                      <td style="vertical-align:middle;">
                        <span style="font-size:22px;font-weight:700;color:#0f766e;letter-spacing:-0.5px;">Tutor</span>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- Card -->
              <tr>
                <td style="background-color:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">

                  <!-- Accent bar -->
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="background-color:#0d9488;height:5px;font-size:0;line-height:0;">&nbsp;</td>
                    </tr>
                  </table>

                  <!-- Body -->
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="padding:36px 40px 32px;">

                        <p style="margin:0 0 8px;font-size:22px;font-weight:700;color:#0f766e;">
                          Bem-vindo(a) ao Tutor, {destinatario_nome.split()[0]}! 👋
                        </p>

                        <p style="margin:0 0 20px;font-size:15px;color:#4b5563;line-height:1.6;">
                          Seu acesso foi criado com sucesso.
                        </p>

                        <p style="margin:0 0 20px;font-size:15px;color:#4b5563;line-height:1.6;">
                          O <strong style="color:#0f766e;">Tutor</strong> é a plataforma de aprendizado do IESB que conecta você
                          aos seus professores e conteúdos por meio de inteligência artificial — permitindo tirar dúvidas,
                          revisar matérias e acompanhar seu desempenho de forma personalizada.
                        </p>

                        <p style="margin:0 0 28px;font-size:15px;color:#4b5563;line-height:1.6;">
                          Para começar, crie sua senha de acesso clicando no botão abaixo:
                        </p>

                        <!-- Button -->
                        <table cellpadding="0" cellspacing="0">
                          <tr>
                            <td style="border-radius:8px;background-color:#0d9488;">
                              <a href="{link}"
                                 style="display:inline-block;padding:14px 32px;font-size:15px;font-weight:600;
                                        color:#ffffff;text-decoration:none;border-radius:8px;letter-spacing:0.2px;">
                                Criar minha senha
                              </a>
                            </td>
                          </tr>
                        </table>

                        <p style="margin:24px 0 0;font-size:12px;color:#9ca3af;line-height:1.5;">
                          Se o botão não funcionar, copie e cole o link abaixo no seu navegador:<br/>
                          <a href="{link}" style="color:#0d9488;word-break:break-all;">{link}</a>
                        </p>

                      </td>
                    </tr>
                  </table>

                  <!-- Footer -->
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="background-color:#f9fafb;border-top:1px solid #e5e7eb;padding:20px 40px;">
                        <p style="margin:0;font-size:12px;color:#9ca3af;line-height:1.5;">
                          Este link é de <strong>uso único</strong> e não possui data de expiração.<br/>
                          Caso tenha dificuldades, entre em contato com a coordenação do IESB.
                        </p>
                      </td>
                    </tr>
                  </table>

                </td>
              </tr>

              <!-- Bottom -->
              <tr>
                <td align="center" style="padding-top:24px;">
                  <p style="margin:0;font-size:12px;color:#9ca3af;">
                    © 2025 Tutor — IESB. Todos os direitos reservados.
                  </p>
                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """

    msg.attach(MIMEText(corpo_html, "html"))

    _enviar_mensagem(msg, destinatario_email)


def enviar_email_recuperacao_senha(destinatario_email: str, destinatario_nome: str, token: str) -> None:
    # reset=1 sinaliza à tela que é redefinição de senha (exibe a tag "Redefinir senha").
    link = f"{FRONTEND_URL}/alterar-senha?token={token}&reset=1"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Redefinição de senha — Tutor"
    msg["From"] = SMTP_FROM
    msg["To"] = destinatario_email

    corpo_html = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    </head>
    <body style="margin:0;padding:0;background-color:#f0fdfa;font-family:'DM Sans',Arial,sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f0fdfa;padding:40px 16px;">
        <tr>
          <td align="center">
            <table width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;">
              <tr>
                <td align="center" style="padding-bottom:24px;">
                  <table cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="padding-right:10px;vertical-align:middle;">
                        <svg width="28" height="28" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M8 0L0 0L0 14.4L8 18M8 0L8 18M8 0L10 0M8 18L10 18M10 0L18 0L18 14.4L10 18M10 0L10 18M2 4.8L6 4.8M2 8.4L6 8.4M12 4.8L16 4.8M12 8.4L16 8.4"
                            fill="white" stroke="#f97316" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                      </td>
                      <td style="vertical-align:middle;">
                        <span style="font-size:22px;font-weight:700;color:#0f766e;">Tutor</span>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
              <tr>
                <td style="background-color:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="background-color:#0d9488;height:5px;font-size:0;line-height:0;">&nbsp;</td>
                    </tr>
                  </table>
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="padding:36px 40px 32px;">
                        <p style="margin:0 0 8px;font-size:22px;font-weight:700;color:#0f766e;">
                          Olá, {destinatario_nome.split()[0]}!
                        </p>
                        <p style="margin:0 0 20px;font-size:15px;color:#4b5563;line-height:1.6;">
                          Recebemos uma solicitação para redefinir a senha da sua conta no <strong style="color:#0f766e;">Tutor</strong>.
                        </p>
                        <p style="margin:0 0 28px;font-size:15px;color:#4b5563;line-height:1.6;">
                          Clique no botão abaixo para criar uma nova senha:
                        </p>
                        <table cellpadding="0" cellspacing="0">
                          <tr>
                            <td style="border-radius:8px;background-color:#0d9488;">
                              <a href="{link}"
                                 style="display:inline-block;padding:14px 32px;font-size:15px;font-weight:600;
                                        color:#ffffff;text-decoration:none;border-radius:8px;">
                                Redefinir minha senha
                              </a>
                            </td>
                          </tr>
                        </table>
                        <p style="margin:24px 0 0;font-size:12px;color:#9ca3af;line-height:1.5;">
                          Se você não solicitou a redefinição, ignore este e-mail — sua senha permanece a mesma.<br/><br/>
                          Se o botão não funcionar, copie e cole o link abaixo:<br/>
                          <a href="{link}" style="color:#0d9488;word-break:break-all;">{link}</a>
                        </p>
                      </td>
                    </tr>
                  </table>
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="background-color:#f9fafb;border-top:1px solid #e5e7eb;padding:20px 40px;">
                        <p style="margin:0;font-size:12px;color:#9ca3af;line-height:1.5;">
                          Este link é de <strong>uso único</strong> e não possui data de expiração.
                        </p>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
              <tr>
                <td align="center" style="padding-top:24px;">
                  <p style="margin:0;font-size:12px;color:#9ca3af;">
                    © 2025 Tutor — IESB. Todos os direitos reservados.
                  </p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """

    msg.attach(MIMEText(corpo_html, "html"))

    _enviar_mensagem(msg, destinatario_email)
