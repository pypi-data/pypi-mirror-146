from armor import Armor
from gun import Gun
from ammo import Ammo
from typing import List

class Tank:
    def __init__(self,model:str, gun: Gun, armors: List[Armor], ammos: List[Ammo], health: int,
    is_gun_loaded:bool):
        self.model = model
        self.gun = gun
        self.armors = armors
        self.ammos = ammos
        self.health = health
        self.is_gun_loaded = is_gun_loaded

    def _add_armors(self, width:int):
        adding_armors = self.armors.append(List[Armor](width = 100))
        return adding_armors
    

    def _load_ammos(self):
        for i in i:
            if i < 10:
                i + 1
        loading_ammos = self.ammos.append(List[Ammo])
        return loading_ammos
        
    

    def select_armor(armor_type:str):
        for x in x:
            if x < armor_type.count:
                x += 1
        
        


    def load_gun(ammo_type:str,is_gun_loaded):
        if is_gun_loaded == True:
            print('Орудие готово к бою!')
        else:
            print('У вас кончились патроны!')
        for a in a:
            if a < ammo_type.count:
                a += 1


    def ammo_shoot(self,is_gun_loaded):
        if is_gun_loaded != True:
            quit
        

    

    





      
    

        
    



