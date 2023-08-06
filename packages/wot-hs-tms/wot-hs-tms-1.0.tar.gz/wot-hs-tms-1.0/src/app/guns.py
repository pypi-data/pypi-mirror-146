from random import randint


class Gun:
    def __init__(self, caliber, barrel_length) -> None:
        self.caliber = caliber
        self.barrel_length = barrel_length
    
    def is_on_target(self):
        return self.barrel_length * randint(1, 6) > 100
