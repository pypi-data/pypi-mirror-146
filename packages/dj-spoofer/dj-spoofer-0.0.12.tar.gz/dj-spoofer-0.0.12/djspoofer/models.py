import datetime
import random

from django.db import models
from django.utils import timezone
from djstarter.models import BaseModel

from . import const, managers


class Proxy(BaseModel):
    objects = managers.ProxyManager()

    url = models.TextField(unique=True, blank=False)
    mode = models.IntegerField(default=const.ProxyModes.GENERAL.value, choices=const.ProxyModes.choices())
    country = models.CharField(max_length=3, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    last_used = models.DateTimeField(blank=True, null=True)
    used_count = models.IntegerField(default=0)
    cooldown = models.DurationField(default=datetime.timedelta(minutes=10))

    class Meta:
        db_table = 'djspoofer_proxy'
        ordering = ['url']
        app_label = 'djspoofer'

    def __str__(self):
        return f'Proxy -> url: {self.url}, mode: {self.pretty_mode}'

    @property
    def http_url(self):
        if self.credentials:
            return f'http://{self.credentials}@{self.url}'
        return f'http://{self.url}'

    @property
    def https_url(self):
        if self.credentials:
            return f'https://{self.credentials}@{self.url}'
        return f'https://{self.url}'

    @property
    def credentials(self):
        if '@' in self.url:
            return None
        if PROXY_USERNAME and PROXY_PASSWORD:
            return f'{PROXY_USERNAME}:{PROXY_PASSWORD}'
        return None

    @property
    def is_on_cooldown(self):
        if self.last_used:
            return self.last_used > timezone.now() - self.cooldown
        return False

    @property
    def pretty_mode(self):
        return self.get_mode_display()

    def set_last_used(self):
        self.last_used = timezone.now()
        self.used_count += 1
        self.save()


class TLSFingerprint(BaseModel):
    objects = managers.FingerprintManager()

    browser = models.CharField(max_length=32)
    extensions = models.IntegerField()
    ciphers = models.TextField()

    class Meta:
        db_table = 'djspoofer_tls_fingerprint'
        ordering = ['-created']
        app_label = 'djspoofer'

        indexes = [
            models.Index(fields=['browser', ], name='tls_fp_browser_index'),
        ]

    def generate_chrome_desktop_cipher_str(self):
        grease_cipher = f'TLS_GREASE_IS_THE_WORD_{random.randint(1, 8)}A'
        return ':'.join(
            [grease_cipher] + [c.value for c in self.shuffled_ciphers(ciphers=const.ChromeDesktopCiphers, start_idx=4)]
        )

    def generate_firefox_desktop_cipher_str(self):
        return ':'.join([c.value for c in self.shuffled_ciphers(ciphers=const.FirefoxDesktopCiphers, start_idx=3)])

    DESKTOP_CLIENT_CIPHER_MAP = {
        'Chrome': generate_chrome_desktop_cipher_str,
        'Firefox': generate_firefox_desktop_cipher_str
    }

    @staticmethod
    def shuffled_ciphers(ciphers, start_idx=0, min_k=6):
        first_ciphers = ciphers[:start_idx]
        rem_ciphers = ciphers[start_idx:]
        k = random.randint(min_k, len(rem_ciphers))
        return first_ciphers + random.sample(rem_ciphers, k=k)

    @staticmethod
    def random_tls_extension_int(min_k=4):
        k = random.randint(min_k, len(const.TLS_EXTENSIONS))
        ext_val = 0
        for ext in random.sample(const.TLS_EXTENSIONS, k=k):
            ext_val |= ext
        return int(ext_val)

    def save(self, *args, **kwargs):
        if not self.ciphers:
            self.ciphers = self.DESKTOP_CLIENT_CIPHER_MAP[self.browser](self)
        if not self.extensions:
            self.extensions = self.random_tls_extension_int()
        super().save(*args, **kwargs)


class Fingerprint(BaseModel):
    objects = managers.FingerprintManager()

    browser = models.CharField(max_length=32)
    device_category = models.CharField(max_length=32)
    os = models.CharField(max_length=32)
    platform = models.CharField(max_length=32)
    screen_height = models.IntegerField()
    screen_width = models.IntegerField()
    user_agent = models.TextField()
    viewport_height = models.IntegerField()
    viewport_width = models.IntegerField()

    proxy = models.ForeignKey(
        to=Proxy,
        related_name='fingerprints',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    tls_fingerprint = models.ForeignKey(
        to=TLSFingerprint,
        related_name='fingerprints',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'djspoofer_fingerprint'
        ordering = ['-created']
        app_label = 'djspoofer'

        indexes = [
            models.Index(fields=['browser', ], name='fp_browser_index'),
            models.Index(fields=['device_category', ], name='fp_device_category_index'),
            models.Index(fields=['platform', ], name='fp_platform_index'),
        ]

    def __str__(self):
        return f'Fingerprint -> user_agent: {self.user_agent}'


