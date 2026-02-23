import requests, selectorlib, smtplib, ssl, os, time, sqlite3
from dotenv import load_dotenv

URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

load_dotenv()

class Event:

    def scrape(self, url):
        """Scrape the page source from the URL"""
        response = requests.get(url, headers=HEADERS)
        source = response.text
        return source

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


class Email:

    def __init__(self, sender, password, receiver):
        self.sender = sender
        self.password = password
        self.receiver = receiver

    def send(self, message):
        host = "smtp.gmail.com"
        port = 465

        username = self.sender
        password = self.password
        receiver = self.receiver

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host=host, port=port, context=context) as server:
            server.login(user=username, password=password)
            server.sendmail(from_addr=username, to_addrs=receiver, msg=message)
        print("Email was sent!")


class Database:

    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path)

    def store_data(self, extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
        self.connection.commit()

    def read_database(self, extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        band, city, date = row
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
        rows = cursor.fetchall()
        # print(rows)
        return rows


if __name__ == "__main__":
    while True:
        event = Event()
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            database = Database(database_path="data.db")
            row = database.read_database(extracted)
            if not row:
                database.store_data(extracted)
                sender = os.getenv("SENDER_MAIL")
                password = os.getenv("MY_GMAIL_PASSWORD")
                receiver = os.getenv("RECEIVER_MAIL")
                email = Email(sender=sender, password=password, receiver=receiver)
                email.send(message="Subject: EVENT ALERT!"+"\n"+"Hey, new event was found!")
        time.sleep(2)