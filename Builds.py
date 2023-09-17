import string
from typing import Any


class Build:
    def __init__(self):
        self.uid = None
        self.prezzo = None
        self.fascia = None
        self.tipo_ram = None
        self.utilizzo = None
        self.componenti = None


    def __int__(self,uid ,prezzo ,fascia ,tipo_ram ,utilizzo, componenti):
        self.uid=uid
        self.prezzo=prezzo
        self.fascia=fascia
        self.tipo_ram=tipo_ram
        self.utilizzo=utilizzo
        self.componenti=componenti

    def __str__(self):
        return f"{self.uid}\n{self.prezzo}\n{self.fascia}\n{self.tipo_ram}\n{self.utilizzo}\n{self.componenti}"

    def get_uid(self):
        return self.uid

    def get_prezzo(self):
        return self.prezzo

    def get_fascia(self):
        return self.fascia

    def get_tipo_ram(self):
        return self.tipo_ram

    def get_utilizzo(self):
        return self.utilizzo

    def get_componenti(self):
        return self.componenti

    def set_uid(self,uid):
         self.uid=uid

    def set_prezzo(self, prezzo):
         self.prezzo=prezzo

    def set_fascia(self,fascia):
        self.fascia=fascia

    def set_tipo_ram(self,tipo_ram):
        self.tipo_ram=tipo_ram

    def set_utilizzo(self,utilizzo):
        self.utilizzo=utilizzo

    def set_componenti(self,componenti):
        self.componenti=componenti






