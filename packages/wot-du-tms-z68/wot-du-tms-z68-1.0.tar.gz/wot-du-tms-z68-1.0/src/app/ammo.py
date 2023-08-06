from app.gun import Gun


class Ammo:

    def __init__(self, gun: object, ammo_type: str) -> None:
        self._gun = gun
        self._ammo_type = ammo_type

    def get_demage(self) -> int:
        return self._gun._caliber * 3

    def get_penetration(self) -> int:
        return self._gun._caliber


class HEСartridge(Ammo):

    def __init__(self, gun: Gun) -> None:
        super().__init__(gun, 'фугасный')


class HEATCartridge(Ammo):

    def __init__(self, gun: Gun) -> None:
        super().__init__(gun, 'кумулятивный')

    def get_demage(self) -> float:
        return super().get_demage() * 0.6


class APCartridge(Ammo):

    def __init__(self, gun: Gun) -> None:
        super().__init__(gun, 'подкалиберный')

    def get_demage(self) -> float:
        return super().get_demage() * 0.3