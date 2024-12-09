import math
import random

class CircleManager:

    def __enter__(self):
        print('Entering CircleManager')
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        print('Exiting CircleManager')

    def random_circle(self, a, b):
        test = pow(random.randint(a, b), 2) * math.pi
        print(f'Random circle: {test}')

    def circle(self, r) -> None:
        test = pow(r, 2) * math.pi
        print(f'Circle: {test}')

if __name__ == '__main__':
    
    with CircleManager() as cm:
        print('Inside the with block')

        cm.random_circle(1, 10)    
        cm.circle(2)    