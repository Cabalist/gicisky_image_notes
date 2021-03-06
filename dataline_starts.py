from typing import List, Tuple

data_line_start_coords = [(0, 0),  # 1
                          (112, 1),  # 2
                          (224, 2),
                          (336, 3),
                          (48, 5),
                          (160, 6),
                          (272, 7),
                          (384, 8),
                          (96, 10),
                          (208, 11),
                          (320, 12),
                          (32, 14),  # 12
                          (144, 15),
                          (256, 16),
                          (368, 17),
                          (80, 19),
                          (192, 20),
                          (304, 21),
                          (16, 23),
                          (128, 24),  # 20
                          (240, 25),  # 21
                          (352, 26),  # 22
                          (64, 28),  # 23
                          (176, 29),  # 24
                          (288, 30),  # 25
                          (0, 32),  # 26
                          (112, 33),
                          (224, 34),
                          (336, 35),
                          (48, 37),
                          (160, 38),
                          (272, 39),
                          (384, 40),
                          (96, 42),
                          (208, 43),
                          (320, 44),
                          (32, 46),
                          (144, 47),
                          (256, 48),
                          (368, 49),
                          (80, 51),  # 41
                          (192, 52),
                          (304, 53),
                          (16, 55),
                          (128, 56),
                          (240, 57),
                          (352, 58),  # 47
                          (64, 60),
                          (176, 61),
                          (288, 62),
                          (0, 64),  # 51
                          (112, 65),
                          (224, 66),
                          (336, 67),
                          (48, 69),
                          (160, 70),
                          (272, 71),
                          (384, 72),
                          (96, 74),
                          (208, 75),
                          (320, 76),
                          (32, 78),
                          (144, 79),
                          (256, 80),
                          (368, 81),
                          (80, 83),
                          (192, 84),
                          (304, 85),
                          (16, 87),
                          (128, 88),
                          (240, 89),
                          (352, 90),
                          (64, 92),
                          (176, 93),
                          (288, 94),
                          (0, 96),  # #####
                          (112, 97),
                          (224, 98),
                          (336, 99),
                          (48, 101),
                          (160, 102),
                          (272, 103),
                          (384, 104),
                          (96, 106),
                          (208, 107),
                          (320, 108),
                          (32, 110),
                          (144, 111),
                          (256, 112),
                          (368, 113),
                          (80, 115),
                          (192, 116),
                          (304, 117),
                          (16, 119),
                          (128, 120),
                          (240, 121),
                          (352, 122),
                          (64, 124),
                          (176, 125),
                          (288, 126),
                          (0, 128),  # ###
                          (112, 129),
                          (224, 130),
                          (336, 131),
                          (48, 133),
                          (160, 134),
                          (272, 135),
                          (384, 136),
                          (96, 138),
                          (208, 139),
                          (320, 140),
                          (32, 142),
                          (144, 143),
                          (256, 144),
                          (368, 145),
                          (80, 147),
                          (192, 148),
                          (304, 149),
                          (16, 151),
                          (128, 152),
                          (240, 153),
                          (352, 154),
                          (64, 156),
                          (176, 157),
                          (288, 158),
                          (0, 160),  # ######
                          (112, 161),
                          (224, 162),
                          (336, 163),
                          (48, 165),
                          (160, 166),
                          (272, 167),
                          (384, 168),
                          (96, 170),
                          (208, 171),
                          (320, 172),
                          (32, 174),
                          (144, 175),
                          (256, 176),
                          (368, 177),
                          (80, 179),
                          (192, 180),
                          (304, 181),
                          (16, 183),
                          (128, 184),
                          (240, 185),
                          (352, 186),
                          (64, 188),
                          (176, 189),
                          (288, 190),
                          (0, 192),  # ##
                          (112, 193),
                          (224, 194),
                          (336, 195),
                          (48, 197),
                          (160, 198),
                          (272, 199),
                          (384, 200),
                          (96, 202),
                          (208, 203),
                          (320, 204),
                          (32, 206),
                          (144, 207),
                          (256, 208),
                          (368, 209),
                          (80, 211),
                          (192, 212),
                          (304, 213),
                          (16, 215),
                          (128, 216),
                          (240, 217),
                          (352, 218),
                          (64, 220),
                          (176, 221),
                          (288, 222),
                          (0, 224),  # ####
                          (112, 225),
                          (224, 226),
                          (336, 227),
                          (48, 229),
                          (160, 230),
                          (272, 231),
                          (384, 232),
                          (96, 234),
                          (208, 235),
                          (320, 236),
                          (32, 238),
                          (144, 239),
                          (256, 240),
                          (368, 241),
                          (80, 243),
                          (192, 244),
                          (304, 245),
                          (16, 247),
                          (128, 248),
                          (240, 249),
                          (352, 250),
                          (64, 252),
                          (176, 253),
                          (288, 254),
                          (0, 256),  # ###
                          (112, 257),
                          (224, 258),
                          (336, 259),
                          (48, 261),
                          (160, 262),
                          (272, 263),
                          (384, 264),
                          (96, 266),
                          (208, 267),
                          (320, 268),
                          (32, 270),
                          (144, 271),
                          (256, 272),
                          (368, 273),
                          (80, 275),
                          (192, 276),
                          (304, 277),
                          (16, 279),
                          (128, 280),
                          (240, 281),
                          (352, 282),
                          (64, 284),
                          (176, 285),
                          (288, 286),
                          (0, 288),  # ##
                          (112, 289),
                          (224, 290),
                          (336, 291),
                          (48, 293),
                          (160, 294),
                          (272, 295),
                          (384, 296),
                          (96, 298),
                          (208, 299)]


def get_dataline_coords(start: Tuple[int, int], line_length: int) -> List[Tuple[int, int]]:
    x, y = start
    line = x + line_length
    end_point = (line % 400, line // 400 + y)

    point_list = [start]

    curr_x = x
    while curr_x < 400:
        curr_x += 1

    return [end_point]


for coords in data_line_start_coords:
    print(f"Start point = {coords}")
    end_point = get_dataline_coords(coords, 512)[0]
    print(f"End point = {end_point}")
    assert end_point[0] <= 400
    assert end_point[1] <= 300
