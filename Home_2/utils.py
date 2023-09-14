def is_mail(mail: str) -> bool:
    """Function for check @ in email"""
    mail = mail.split("@")
    if len(mail) != 2:
        return False
    return True
