import datetime

from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album
from album import save
from album import find
from album import valid

#ЗАПРОС ПОИСКА АЛЬБОМОВ АРТИСТА
@route("/albums/<artist>")
def albums(artist):
    albums_list = find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Количество альбомов группы {0}: {1}\n".format(artist, len(album_names)) + "Список альбомов группы {}\n".format(artist)
        result += "\n".join(album_names)
    return result

#ПРОВЕРКА ВАЛИДНОСТИ ГОДА ВЫПУСКА
def valid_album(year):
    year = int(year)
    date = datetime.date.today()
    year_now = int(date.year)
    if year > year_now:
        return False
    else:
        return True
    

#ПОСТ-ЗАПРОС СОХРАНЕНИЯ НОВОГО АЛЬБОМА
@route("/albums", method="POST")
def album():
    if valid_album(request.forms.get("year")):
        album_data = {
            "year": request.forms.get("year"),
            "artist": request.forms.get("artist"),
            "genre": request.forms.get("genre"),
            "album": request.forms.get("album")
        }
        if valid(album_data):
            save(album_data)
            return "Данные успешно сохранены"
        else: 
            result = HTTPError(409, "Альбом уже в базе данных")
            return result
    else:
        result = HTTPError(400, "Недопустимое значение `year` ")
        return result

#http -f POST http://localhost:8080/albums year="2010" artist="New Artist" genre="Rock" album="Super"
#http -f POST http://localhost:8080/albums year="2030" artist="New Artist" genre="Rock" album="Super"

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
