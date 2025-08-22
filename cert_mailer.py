#!/usr/bin/env python3
"""
Certificate Generator & Mailer (Name + Email only)
---------------------------------------------------
- Places only the NAME on your Canva PNG template
- Saves as PDF
- Emails the certificate to each user in Excel
"""

import os
import re
import pandas as pd
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import smtplib
from email.message import EmailMessage

# ========================= USER SETTINGS =========================
TEMPLATE_PATH = "certificate_template.png"   # Canva export PNG
EXCEL_PATH = "users.xlsx"
OUTPUT_DIR = "output_certificates"

# Text position (adjust this for your design)
NAME_BOX   = (1025, 2539, 3386, 2763)   # (x1, y1, x2, y2)

# Fonts (edit path if needed)
PREFERRED_FONTS = [
    r"C:\Windows\Fonts\arialbd.ttf",   # Arial Bold
    r"C:\Windows\Fonts\calibri.ttf",
]
NAME_MAX_SIZE = 140
MIN_FONT_SIZE = 24

# Email sending (Gmail)
SEND_EMAIL = True  # <-- Set False to only generate
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "mail@gmail.com"     # <-- change
SENDER_APP_PASSWORD = "mail_password" # <-- create App Password in Google

EMAIL_SUBJECT = "Your Certificate"
EMAIL_BODY = """Dear {name},

Congratulations! Please find your certificate attached.

Best regards,
Team EIC
"""

# =================================================================

def first_existing_font(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    return None

def slugify(value):
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE).strip().lower()
    return re.sub(r"[-\s]+", "-", value)

def fit_text_into_box(draw, text, box, font_path, max_size, min_size):
    """Return font sized to fit text inside box."""
    x1, y1, x2, y2 = box
    width = x2 - x1
    height = y2 - y1

    size = max_size
    while size >= min_size:
        if font_path and os.path.exists(font_path):
            font = ImageFont.truetype(font_path, size=size)
        else:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        if tw <= width and th <= height:
            return font
        size -= 2

    if font_path and os.path.exists(font_path):
        return ImageFont.truetype(font_path, size=min_size)
    return ImageFont.load_default()

def draw_centered_text(draw, text, box, font):
    x1, y1, x2, y2 = box
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = x1 + (x2 - x1 - tw) // 2
    y = y1 + (y2 - y1 - th) // 2
    draw.text((x, y), text, font=font, fill=(0,0,0))  # black text

def generate_certificate(bg_path, name, out_pdf_path):
    img = Image.open(bg_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    font_path = first_existing_font(PREFERRED_FONTS)
    name_font = fit_text_into_box(draw, name, NAME_BOX, font_path, NAME_MAX_SIZE, MIN_FONT_SIZE)

    draw_centered_text(draw, name, NAME_BOX, name_font)

    img.save(out_pdf_path, "PDF", resolution=300.0)

def send_email_with_attachment(to_email, subject, body, attachment_path, name):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg.set_content(body.format(name=name))

    with open(attachment_path, "rb") as f:
        data = f.read()
    msg.add_attachment(
        data,
        maintype="application",
        subtype="pdf",
        filename=os.path.basename(attachment_path)
    )

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
        smtp.send_message(msg)

def main():
    tpl = Path(TEMPLATE_PATH)
    if not tpl.exists():
        raise SystemExit(f"Template not found: {tpl.resolve()}")
    outdir = Path(OUTPUT_DIR)
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_excel(EXCEL_PATH)
    cols = {c.lower().strip(): c for c in df.columns}
    for m in ["name", "email"]:
        if m not in cols:
            raise SystemExit(f"Missing column in Excel: {m}")

    for _, row in df.iterrows():
        name = str(row[cols["name"]]).strip()
        email = str(row[cols["email"]]).strip()

        pdf_name = slugify(name) + ".pdf"
        out_pdf = str(Path(OUTPUT_DIR) / pdf_name)

        print(f"Generating: {out_pdf}")
        generate_certificate(str(tpl), name, out_pdf)

        if SEND_EMAIL and email and "@" in email:
            print(f"  -> emailing to {email}")
            send_email_with_attachment(email, EMAIL_SUBJECT, EMAIL_BODY, out_pdf, name)

    print("Done. Check folder:", outdir.resolve())

if __name__ == "__main__":
    main()
