from random import *

# характеристики персонажа игрока
p_hp = 5
p_damage = 2
p_value_of_water = 5
p_speed = 10
p_money = 0
p_seeds = {"potato": 3, "onion": 0, "carrot": 0}
decreased = False
# враг hamster
jack_hp = 5
jack_speed = 3
# случайный дроп семян
jack_seed_value = randint(1, 3)

# враг bombardier
bombardier_hp = 5
bombardier_speed = 4
bombardier_seed_value = {choice(list(p_seeds.keys())): randint(1, 2)}


def get_seed_count():
    p_s = 0
    for k, v in p_seeds.items():
        p_s += v
    return p_s




