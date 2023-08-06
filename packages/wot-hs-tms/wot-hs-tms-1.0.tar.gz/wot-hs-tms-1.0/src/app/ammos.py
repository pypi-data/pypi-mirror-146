from numbers import Number

from app.guns import Gun


class Ammo:
    def __init__(self, gun: Gun, ammo_type: str) -> None:
        self.gun = gun
        self.ammo_type = ammo_type
    
    def get_demage(self) -> int:
        return self.gun.caliber * 3
    
    def get_penetration(self):
        return self.gun.caliber


class HECartridge(Ammo):
    def __init__(self, gun: Gun) -> None:
        super().__init__(gun, 'фугасный')
    

class HEATCartridge(Ammo):
    def __init__(self, gun: Gun) -> None:
        super().__init__(gun, 'кумулятивный')
    
    def get_demage(self):
        return super().get_demage() * 0.6
    

class APCartridge(Ammo):
    def __init__(self, gun: Gun) -> None:
        super().__init__(gun, 'подкалиберный')
    
    def get_demage(self) -> float:
        return super().get_demage() * 0.3