from app.ammo import Ammo, HEСartridge, HEATCartridge, APCartridge


class Tank:
    
    def __init__(self, model: str, gun: object, armors: list, ammos: list, health: int):
        self._model = model
        self._gun = gun
        self._armors = armors if armors else self._load_armours(100)
        self._ammos = ammos if ammos else self._load_ammos(10)
        self._health = health
        self._selected_armour = armors[0]
        self._loaded_ammo = None

    def _load_armours(self, armour_width):
        self._armors = [cls(armour_width) for cls in [HArmour, SArmour, CArmour]]

    def _load_ammos(self, ammo_count = 10):
        for ammo_cls in [HEСartridge, HEATCartridge, APCartridge]:
            for _ in range(ammo_count):
                self._ammos.append(ammo_cls(self._gun))
    
    def select_armour(self, armour_type: str):
        self._selected_armour = list(
            filter(lambda x: x.armour_type == armour_type, self._armors)
        )[0]
    
    def load_gun(self, ammo_type: str):
        searched_ammos = list(
            filter(lambda x: x.ammo_type == ammo_type, self._ammos)
        )

        if searched_ammos:
            self._loaded_ammo = searched_ammos[0]
        else:
            raise Exception(f'{ammo_type} not exist')
    
    def _remove_loaded_ammo(self):
        self._ammos.remove(self._loaded_ammo)
        self._loaded_ammo = None
    
    def shoot(self) -> Optional[Ammo]:
        if not self._loaded_ammo:
            raise Exception(f'Gun {self._gun} must be loaded!')
        
        fired_ammo = copy(self._loaded_ammo)
        self._remove_loaded_ammo()

        is_on_target = self._gun.is_on_target()

        if is_on_target:
            print('Попадание')
            return fired_ammo
    
    def handle_hit(self, ammo: Ammo):
        if self._selected_armour.is_penetrated(ammo):
            self._health -= ammo.get_demage()
        else:
            print('Броня не пробита!')
