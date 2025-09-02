from django.core.mail.backends.smtp import EmailBackend
from .models import SMTPConfig

class DatabaseEmailBackend(EmailBackend):
    def __init__(self, *args, **kwargs):
        # Fetch the active configuration from the database
        config = SMTPConfig.objects.filter(is_active=True).first()

        if config:
            kwargs['host'] = config.smtp_host
            kwargs['port'] = config.smtp_port
            kwargs['username'] = config.smtp_user
            kwargs['password'] = config.smtp_password
            kwargs['use_tls'] = config.use_tls
            kwargs['use_ssl'] = config.use_ssl

        super().__init__(*args, **kwargs)
