"""Pengiriman email transaksional melalui Resend tanpa menaruh secret di kode."""

from __future__ import annotations

import asyncio
import json
from urllib.error import URLError
from urllib.request import Request, urlopen

from config import get_settings


async def send_password_reset_email(recipient: str, reset_url: str) -> bool:
    """Kirim tautan reset. False bila provider belum dikonfigurasi atau gagal."""
    settings = get_settings()
    if not settings.resend_api_key or not settings.email_from:
        return False

    payload = json.dumps(
        {
            "from": settings.email_from,
            "to": [recipient],
            "subject": "Atur ulang kata sandi BioChemVerse",
            "html": (
                "<p>Kami menerima permintaan untuk mengatur ulang kata sandi BioChemVerse.</p>"
                f'<p><a href="{reset_url}">Atur ulang kata sandi</a></p>'
                "<p>Tautan ini berlaku selama 1 jam dan hanya dapat digunakan sekali. "
                "Abaikan email ini bila Anda tidak memintanya.</p>"
            ),
        }
    ).encode("utf-8")

    def post() -> bool:
        request = Request(
            "https://api.resend.com/emails",
            data=payload,
            headers={
                "Authorization": f"Bearer {settings.resend_api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=10) as response:
                return 200 <= response.status < 300
        except (URLError, TimeoutError):
            return False

    return await asyncio.to_thread(post)
