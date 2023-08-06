from tank_game.ammo import Ammo, HEATCartridge, HECartridge
from gun import Gun

class Armor:
    
    def __init__(self, thickness, type_armor) -> None:
        self.thickness = thickness
        self.type = type_armor

    def is_penetrated(self,ammo: Ammo) -> bool:
        return ammo.get_penetration() > self.thickness
          
    
class HArmor(Armor):
    def __init__(self, thickness, type_armor):
        super().__init__(self, thickness, type_armor)

    def is_penetrated(self,ammo: Ammo):
        AMMO_TYPES = {
        'HE_cartridge': 1.2,
        'HEAT_cartridge': 1,
        'AP_cartridge': 0.7,
            }

        return ammo.get_penetration() > self.thickness * AMMO_TYPES[ammo.ammo_type]


class SArmor(Armor):
    def __init__(self, thickness, type_armor):
        super().__init__(self, thickness, type_armor)

    def is_penetrated(self,ammo: Ammo):
        AMMO_TYPES = {
        'HE_cartridge': 0.9,
        'HEAT_cartridge': 1.3,
        'AP_cartridge': 1.6,
            }

        return ammo.get_penetration() > self.thickness * AMMO_TYPES[ammo.ammo_type]
        

class CArmor(Armor):
    def __init__(self, thickness, type_armor):
        super().__init__(thickness, type_armor)

    def is_penetrated(self,ammo: Ammo= None):
        AMMO_TYPES = {
            'HE_cartridge': 1.7,
            'HEAT_cartridge': 0.6,
            'AP_cartridge': 1.1,
        }


        return ammo.get_penetration() > self.thickness * AMMO_TYPES[ammo.ammo_type]















    
    