
import random



class Gun:

    def __init__(self, caliber: int, turret_length: int) -> None:
        self.caliber = caliber
        self.turett_length = turret_length



    def is_on_target(self, dice = (random.randint(1,6))):
        result = self.caliber * dice > 100
      
        return result 




    
    
    

