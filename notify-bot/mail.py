#!/usr/bin/env python3
""" Notification via SMTP Mail
"""
# Usage: python3 mail.py <gh_issue_number> <smtp_user>
#                   <smtp_password> <smtp_server> <sent_from> <to_email>

from jinja2 import Environment, FileSystemLoader
from email.message import EmailMessage
from gh_issue import get_issue
from sys import argv
import markdown
import smtplib
import string


def clean_text(str_to_cleaned: str) -> str:
    """ Remove non-ASCII characters in a string
    Args:
        str_to_cleaned (str): String to be cleaned
    Returns:
        (str): String without non-ASCII characters
    """
    printable = set(string.printable)
    return ''.join(filter(lambda x: x in printable, str_to_cleaned))


def email_notification(
    gh_issue_number: str,
    smtp_user: str,
    smtp_password: str,
    smtp_server: str,
    sent_from: str,
    to_email: str
) -> None:
    """ Send an Email Notification
    Args:
        gh_issue_number (str): GitHub Issue Number
        smtp_user (str): SMTP user
        smtp_password (str): SMTP password
        smtp_server (str): SMTP server
        sent_from (str): Email to send from
        to_email (str): Email to send to
    """
    title, created_at, description, label = get_issue(gh_issue_number)
    template_path = "alert.html.j2"

    subject = f"{ title } #{gh_issue_number}"
    description = description.replace("\n", "<br>")
    content = f"{ markdown.markdown(description) }"
    # There maybe a bug in the Status Issue template in Uptime
    content = content.replace("&lt;br&gt;", "")
    style = {
        "<p>": '<p style="Margin:0;-webkit-text-size-adjust:none;\
                -ms-text-size-adjust:none;mso-line-height-rule:exactly;\
                font-family:lato, \'helvetica neue\', helvetica, arial, \
                sans-serif;line-height:27px;color:#666666;font-size:18px">'
    }
    # Lazy Style adjustments
    for old_tag, new_tag in style.items():
        content = content.replace(old_tag, new_tag)

    # Choose colors based on labels
    colors = {
        "maintenance": "#ffa73b",
        "status": "#EC6D64",
        "others": "#7c72dc"
    }

    # Render HTML as email body
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template(template_path)
    html_body = template.render(
        title=subject, preheader=subject, heading=subject, body=content,
        color=colors[label], gh_issue_number=gh_issue_number)

    # Prepare Payload to send
    message_html = EmailMessage()
    message_html.add_alternative(html_body, subtype='html')
    message_html['X-Face'] = "https://thekrishna.in/assets/img/avatars/avatar_bot_48.jpg"
    message_html['X-Image-Url'] = "https://thekrishna.in/assets/img/avatars/avatar_bot_64.jpg"
    message_html['Subject'] = subject
    message_html['From'] = f"Robokeks - Uptime <{ sent_from }>"
    message_html['To'] = to_email

    try:
        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.ehlo()
        server.login(smtp_user, smtp_password)
        server.send_message(message_html)
        server.close()
        print('Email Successfully sent')
    except Exception as e:
        print(f'The following error occured while sending email: {e}')


if __name__ == "__main__":
    email_notification(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6])
