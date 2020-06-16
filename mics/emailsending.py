import smtplib,email,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def linksend(email,link):
    try:
        msg = MIMEMultipart()
        msg['From'] = 'kvir411@gmail.com'
        msg['To'] = email
        msg['Subject'] = "Verification Email"
        msg.attach(MIMEText(link,'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('kvir411@gmail.com', 'he4rtonfire')
        #text=msg.as_string()
        server.sendmail(msg['From'],msg['To'] ,msg.as_string())
        server.quit()
        return True
    except:
        return False

def otpsend(email,otp):
    try:
        msg = MIMEMultipart()
        msg['From'] = 'kvir411@gmail.com'
        msg['To'] = email
        msg['Subject'] = "OTP"
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('kvir411@gmail.com', 'he4rtonfire')

        server.sendmail(msg['From'], msg['To'],otp)
        server.quit()
        return True
    except:
        return False