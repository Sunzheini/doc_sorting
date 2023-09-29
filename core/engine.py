import random


class Engine:
    def __init__(self, *args, **kwargs):
        pass

    def functions_bound_to_button1(self):
        random_list = ['red', 'green', 'yellow', 'gray']
        random1 = random.choice(random_list)
        return random1

    def functions_bound_to_button2(self):
        random_list = ['red', 'green', 'yellow', 'gray']
        random2 = random.choice(random_list)
        return random2

    def functions_bound_to_button3(self):
        random_list = ['red', 'green', 'yellow', 'gray']
        random3 = random.choice(random_list)
        return random3
