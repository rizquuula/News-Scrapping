from .url_indo_cnn import UrlIndoCNN
from .url_kompas import UrlKompas
from .url_tempo import UrlTempo
from .url_turnbackhoax import UrlTurnBackHoax


class BaseUrl:
    indo_cnn = UrlIndoCNN()
    kompas = UrlKompas()
    tempo = UrlTempo()
    turnbackhoax = UrlTurnBackHoax()
