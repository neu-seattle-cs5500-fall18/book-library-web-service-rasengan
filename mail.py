from flask_mail import Mail, Message

mail = Mail()


def send_reminder_mail(borrower_email, book_title):
    msg = Message(subject=book_title + " - Book Return - Reminder",
                  recipients=[borrower_email],
                  body="This is a reminder for you to return the borrowed book titled - " +
                       book_title + ", it's getting late bruh :(")
    mail.send(msg)
    print("Mail Sent To " + borrower_email)
