import smtplib

class SendEmail:
    def __init__(self) -> None:
        self.session = smtplib.SMTP('smtp.gmail.com', 587)
        self.session.starttls()
        self.session.login('octopay123@gmail.com','MyOctopus1!')
    
    def send_message(self, url, email):
        msg = f"""
        Subject: Payment Request\n
        Your payment Linke - {url}\n Octopus Team
        """
        
        self.session.sendmail('octopay123@gmail.com', email, msg,)