from app.ammos import Ammo, HEATCartridge, HECartridge


class Armour:
    def __init__(self, thickness, armour_type) -> None:
        self.thickness = thickness
        self.armour_type = armour_type
    
    def is_penetrated(self, ammo: Ammo) -> bool:
        return ammo.get_penetration() > self.thickness


class HArmour(Armour):
    def __init__(self, thickness) -> None:
        super().__init__(thickness, 'гомогенная')
    
    def is_penetrated(self, ammo: Ammo) -> bool:
        # можно сделать лучше
        if ammo is HECartridge:
            ammo_factor = 1.2
        elif ammo is HEATCartridge:
            ammo_factor = 1
        else:
            ammo_factor = 0.7
        
        return ammo.get_penetration() > self.thickness * ammo_factor


class SArmour(Armour):
    def __init__(self, thickness) -> None:
        super().__init__(thickness, 'Стальная')
    
    def is_penetrated(self, ammo: Ammo) -> bool:
        # можно сделать лучше
        if ammo is HECartridge:
            ammo_factor = 1.5
        elif ammo is HEATCartridge:
            ammo_factor = 1.2
        else:
            ammo_factor = 0.9
        
        return ammo.get_penetration() > self.thickness * ammo_factor
