whidth = 1280
height = 720
fps = 60
scale_factor = 2
tile_size = 128  # ширина и высота одной клетки(коэффициент)
player_coordinates = (1400, 4300)
hands_coordinates = player_coordinates
player_current_x = 1400
player_current_y = 4300
planted=False
picked=False

planting_tiles = [[1, (2048, 2944), "plant_type", 0, "without.png", False],
                  [2, (2176, 2944), "plant_type", 0, "without.png", False],
                  [3, (2304, 2944), "plant_type", 0, "without.png", False],
                  [4, (2432, 2944), "plant_type", 0, "without.png", False],
                  [5, (2048, 3072), "plant_type", 0, "without.png", False],
                  [6, (2176, 3072), "plant_type", 0, "without.png", False],
                  [7, (2304, 3072), "plant_type", 0, "without.png", False],
                  [8, (2432, 3072), "plant_type", 0, "without.png", False],
                  [9, (2048, 3200), "plant_type", 0, "without.png", False],
                  [10, (2176, 3200), "plant_type", 0, "without.png", False],
                  [11, (2304, 3200), "plant_type", 0, "without.png", False],
                  [12, (2432, 3200), "plant_type", 0, "without.png", False],
                  [13, (2048, 3328), "plant_type", 0, "without.png", False],
                  [14, (2176, 3328), "plant_type", 0, "without.png", False],
                  [15, (2304, 3328), "plant_type", 0, "without.png", False],
                  [16, (2432, 3328), "plant_type", 0, "without.png", False],
                  ]
# разбитие карты на учаски через значение клеток в массиве
planting_tiles_coords = []
p_tile_obljects =[]
#пустые списки не трогать!!!
#они заполняются во время работы программы

#enemies
monster_data={"jack":{"health":100,"damage":1,"attack_type":"slash","attack_sound:":"...","speed":3,"resistance":3,"attack_radius":80,"notice_radius":80}}
enemies=[]
enemies_pos=[[5888, 1792], [5632, 1920], [4608, 2560], [4864, 2560], [6528, 2560], [6784, 2560], [4736, 2816], [6528, 2816], [6784, 2816], [4352, 3328], [4608, 3456], [6400, 3968], [6656, 3968], [4864, 4096], [4608, 4224], [4864, 4352], [5632, 4352], [6016, 4480]]

sprite_offset=0