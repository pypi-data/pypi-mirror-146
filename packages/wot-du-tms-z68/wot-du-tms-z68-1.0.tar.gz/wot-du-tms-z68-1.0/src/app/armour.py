from app.ammo import Ammo, HEСartridge, HEATCartridge, APCartridge


class Armour:

    def __init__(self, thickness: int, type_armour: str) -> None:
        self._thickness = thickness
        self._type_armour = type_armour

    def is_penetrated(self, ammo: object) -> bool():
        return ammo.get_penetration() > self._thickness


class HArmour(Armour):

    ammo_type_coef = {
        
        'HEСartridge': 1.2,
        'HEATCartridge': 1,
        'APCartridge': 0.7,
    }

    def __init__(self, thickness: int) -> None:
        super().__init__(thickness, 'гомогенная')

    def is_penetrated(self, ammo: object) -> bool:
        return ammo.get_penetration() > self._thickness * self.ammo_type_coef[str(ammo.__class__.__name__)]


class SArmour(Armour):

    ammo_type_coef = {

        'HEСartridge': 1.5,
        'HEATCartridge': 1.2,
        'APCartridge': 0.9,
    }

    def __init__(self, thickness: int) -> None:
        super().__init__(thickness, 'cтальная')

    def is_penetrated(self, ammo: object) -> bool:
        return ammo.get_penetration() > self._thickness * self.ammo_type_coef[str(ammo.__class__.__name__)]


class CArmour(Armour):

    ammo_type_coef = {

        'HEСartridge': 1.2,
        'HEATCartridge': 1,
        'APCartridge': 0.7,
    }

    def __init__(self, thickness: int) -> None:
        super().__init__(thickness, 'керамическая')

    def is_penetrated(self, ammo: object) -> bool:
        return ammo.get_penetration() > self._thickness * self.ammo_type_coef[str(ammo.__class__.__name__)]
