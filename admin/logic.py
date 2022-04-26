import smtplib

class SendEmail:
    def __init__(self) -> None:
        self.session = smtplib.SMTP('smtp.gmail.com', 587)
        self.session.starttls()
        self.session.login('testhackathon5@gmail.com','Octopus99!')
    
    def send_message(self, url, email):
        msg = f"""
        Subject: Payment Request\n
        Your payment Linke - {url}\n Octopus Team
        """
        
        self.session.sendmail('testhackathon5@gmail.com', email, msg,)