import random


class Gun:

    def __init__(self, caliber: int, barrel_length: int) -> None:
        self._caliber = caliber
        self._barrel_length = barrel_length

    def is_on_target(self) -> bool:
        dice = random.uniform(0, 1)
        return self._barrel_length * dice > 100