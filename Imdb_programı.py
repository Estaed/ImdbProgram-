import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QWidget,QApplication,QGridLayout,QLabel,QLineEdit,QTextEdit,QPushButton
import sys

class Pencere(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.rating_yazı = QLabel("Rating Puanını Giriniz:")
        self.rating = QLineEdit()
        self.filmler = QTextEdit()
        self.sırala = QPushButton("Filmleri Sırala")
        self.temizle = QPushButton("Temizle")

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.rating_yazı,1,0)
        grid.addWidget(self.rating,1,1)

        grid.addWidget(self.filmler,2,1)

        grid.addWidget(self.sırala,3,1)
        grid.addWidget(self.temizle,3,0)

        self.setLayout(grid)
        self.setWindowTitle("Imdb Film Listeleme Programı")
        self.sırala.clicked.connect(self.film_cek)
        self.temizle.clicked.connect(self.sil)
        self.show()

    def sil(self):
        self.rating.clear()
        self.filmler.clear()

    def film_cek(self):
        try:
            url = "https://www.imdb.com/chart/top"

            response = requests.get(url)
            html_içeriği = response.content

            soup = BeautifulSoup(html_içeriği, "html.parser")

            başlıklar = soup.find_all("td", {"class": "titleColumn"})
            ratingler = soup.find_all("td", {"class": "ratingColumn imdbRating"})

            değer = self.rating.text()

            for başlık,rating in zip(başlıklar,ratingler):
                başlık = başlık.text
                başlık = başlık.strip()
                başlık = başlık.replace("\n", "")

                rating = rating.text
                rating = rating.strip()
                rating = rating.replace("\n", "")

                film = "Film İsmi: {}\nFilm Ratingi: {}\n{}".format(başlık,rating,"****************************")
                if(rating >= değer):
                    self.filmler.append(film)

        except:
            sys.stderr.write("Bir Sorun Oluştu!")
            sys.stderr.flush()

app = QApplication(sys.argv)
pencere = Pencere()
sys.exit(app.exec_())