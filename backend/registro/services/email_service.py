import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from django.conf import settings

from ..dtos import PollenDTO, PDFResultDTO
from ..interfaces import IEmailService


class EmailService(IEmailService):
    def enviar_bienvenida(
        self,
        destinatario: str,
        nombre: str,
        datos_polen: PollenDTO,
        pdf: PDFResultDTO | None,
    ) -> None:
        msg = MIMEMultipart('mixed')
        msg['Subject'] = '🌿 Bienvenido/a a TuAlergiahoy — Tu pronóstico personalizado'
        msg['From'] = settings.DEFAULT_FROM_EMAIL
        msg['To'] = destinatario

        mensaje_pdf = (
            'Adjunto encontrarás tu <strong>pronóstico personalizado de salud</strong> para esta semana.'
            if pdf else
            'El pronóstico personalizado estará disponible pronto en tu correo.'
        )

        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; color: #333;">
            <div style="background: #1a7f6e; padding: 30px; border-radius: 8px 8px 0 0; text-align: center;">
                <h1 style="color: white; margin: 0;">TuAlergiahoy.com</h1>
                <p style="color: #d4f5ef; margin: 8px 0 0;">Tu compañero de salud respiratoria</p>
            </div>
            <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px;">
                <h2>¡Bienvenido/a, {nombre}!</h2>
                <p>Nos alegra que formes parte de TuAlergiahoy.</p>
                <div style="background: white; border-left: 4px solid #1a7f6e; padding: 20px; margin: 20px 0; border-radius: 4px;">
                    <h3 style="margin-top: 0; color: #1a7f6e;">🌿 Niveles de polen actuales</h3>
                    <p><strong>Estado general:</strong> {datos_polen.estado}</p>
                    <p><strong>Principal alérgeno:</strong> {datos_polen.tipo_polen}</p>
                    <pre style="background: #f0f0f0; padding: 12px; border-radius: 4px; font-size: 13px;">{datos_polen.datos_detalle}</pre>
                </div>
                <p>{mensaje_pdf}</p>
                <p style="color: #888; font-size: 12px; margin-top: 30px; border-top: 1px solid #eee; padding-top: 15px;">
                    Este email es automático. Contacta siempre con tu especialista.<br>
                    © TuAlergiahoy.com
                </p>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, 'html'))

        if pdf:
            adjunto = MIMEBase('application', 'octet-stream')
            adjunto.set_payload(pdf.contenido)
            encoders.encode_base64(adjunto)
            adjunto.add_header('Content-Disposition', f'attachment; filename="{pdf.nombre_archivo}"')
            msg.attach(adjunto)

        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.send_message(msg)