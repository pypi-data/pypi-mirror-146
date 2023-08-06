from numbers import Number
from tank_game.gun import Gun


class Ammo:
    

    def __init__(self, gun: Gun, ammo_type:str):
        self.gun = gun
        self.ammo_type = ammo_type

        
    def get_damage(self):
        dmg = self.gun.caliber * 3
        return dmg

    def get_penetration(self):
        return self.gun.caliber


class HECartridge(Ammo):
    def __init__(self, gun: Gun):
        super().__init__(gun, 'фугасный')

    def get_damage(self):
        return super().get_damage()



class HEATCartridge(Ammo):
    def __init__(self, gun: Gun):
        super().__init__(gun, 'кумулятивный')
    
    def get_damage(self):
        return super().get_damage() * 0.6


class APCartridge(Ammo):
    def __init__(self, gun: Gun):
        super().__init__(gun, 'подкалиберный')
    
    def get_damage(self):
        return super().get_damage() * 0.3

    


        

