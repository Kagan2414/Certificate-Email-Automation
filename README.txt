
STEP-BY-STEP: Canva Template → Certificates → Email
===================================================

1) In Canva
-----------
- Open your certificate design.
- Remove placeholder texts like {NAME} so you have a clean background.
- Download as PNG (Recommended: A4 size 3508x2480 px, 300 DPI) and name it:
  certificate_template.png

2) Put files in one folder
--------------------------
- This script folder should contain:
  - certificate_template.png
  - users.xlsx  (columns: Name, Email, Course, Date)
  - cert_mailer.py

3) Install Python packages (Windows)
------------------------------------
If pip is missing:
    py -m ensurepip --upgrade

Then:
    py -m pip install --upgrade pip
    py -m pip install pandas pillow openpyxl

4) Run the script
-----------------
    python cert_mailer.py

It will create PDFs in the 'output_certificates' folder.

5) Adjust text positions
------------------------
- Open certificate_template.png in MS Paint.
- Hover the mouse to see X,Y in the status bar.
- In cert_mailer.py, tweak NAME_BOX, COURSE_BOX, DATE_BOX values:
    NAME_BOX   = (x1, y1, x2, y2)
- Re-run until the text lands perfectly.

6) Email sending (optional)
---------------------------
- In cert_mailer.py, set SEND_EMAIL = True
- Use Gmail:
  - Create a Google "App Password" (Account → Security → 2-Step Verification → App Passwords).
  - Fill SENDER_EMAIL and SENDER_APP_PASSWORD.
- Re-run the script to email each PDF.

Troubleshooting
---------------
- If fonts look off, set a specific .ttf in PREFERRED_FONTS (e.g. Arial Bold):
  C:\Windows\Fonts\arialbd.ttf
- Ensure your Excel has the exact columns: Name, Email, Course, Date.
- If dates appear as numbers, change Excel cell format to Date OR the script will try parsing ISO format.

Good luck!
