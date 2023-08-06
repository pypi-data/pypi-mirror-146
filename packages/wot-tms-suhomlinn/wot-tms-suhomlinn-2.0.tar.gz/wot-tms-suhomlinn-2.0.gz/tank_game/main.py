from ast import Pass
from tank_game import gun, ammo, armor


if __name__ == '__main__':
    gun = gun.Gun(120,40)
    HEAT_ammo = ammo.HEATCartridge(gun)
    armor = armor.HArmour(120)

    pass 

    print(HEAT_ammo.get_damage())
    