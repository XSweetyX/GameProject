from random import *

# характеристики персонажа игрока
p_hp = 5
p_value_of_water = 5
p_speed = 5
p_money = 0
p_seeds = {"potato": 0, "onion": 0, "carrot": 0}

# враг hamster
hamster_hp = 5
hamster_speed = 3
# случайный дроп семян
hamster_seed_value = {choice(list(p_seeds.keys())): randint(1, 3)}
# print(hamster_seed_value)

# враг bombardier
bombardier_hp = 5
bombardier_speed = 4
bombardier_seed_value = {choice(list(p_seeds.keys())): randint(1, 2)}
