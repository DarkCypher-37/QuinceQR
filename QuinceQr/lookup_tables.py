import pickle

from enumerations import ErrorCorrectionLevel, ModeIndicator, SizeLevel


def load_pickle_file(filepath: str):
    """
    load a file as a pickle object

    Parameters
    ----------
    filepath
        the filepath to the picklefile

    Returns
    -------
    Any
        the object form the file
    """
    with open(filepath, 'rb') as file:
        data = pickle.load(file)
    return data


version_dict = [
    {
        ErrorCorrectionLevel.L: [41, 25, 17, 10],
        ErrorCorrectionLevel.M: [34, 20, 14, 8],
        ErrorCorrectionLevel.Q: [27, 16, 11, 7],
        ErrorCorrectionLevel.H: [17, 10, 7, 4]
    },
    {
        ErrorCorrectionLevel.L: [77, 47, 32, 20],
        ErrorCorrectionLevel.M: [63, 38, 26, 16],
        ErrorCorrectionLevel.Q: [48, 29, 20, 12],
        ErrorCorrectionLevel.H: [34, 20, 14, 8]
    },
    {
        ErrorCorrectionLevel.L: [127, 77, 53, 32],
        ErrorCorrectionLevel.M: [101, 61, 42, 26],
        ErrorCorrectionLevel.Q: [77, 47, 32, 20],
        ErrorCorrectionLevel.H: [58, 35, 24, 15]
    },
    {
        ErrorCorrectionLevel.L: [187, 114, 78, 48],
        ErrorCorrectionLevel.M: [149, 90, 62, 38],
        ErrorCorrectionLevel.Q: [111, 67, 46, 28],
        ErrorCorrectionLevel.H: [82, 50, 34, 21]
    },
    {
        ErrorCorrectionLevel.L: [255, 154, 106, 65],
        ErrorCorrectionLevel.M: [202, 122, 84, 52],
        ErrorCorrectionLevel.Q: [144, 87, 60, 37],
        ErrorCorrectionLevel.H: [106, 64, 44, 27]
    },
    {
        ErrorCorrectionLevel.L: [322, 195, 134, 82],
        ErrorCorrectionLevel.M: [255, 154, 106, 65],
        ErrorCorrectionLevel.Q: [178, 108, 74, 45],
        ErrorCorrectionLevel.H: [139, 84, 58, 36]
    },
    {
        ErrorCorrectionLevel.L: [370, 224, 154, 95],
        ErrorCorrectionLevel.M: [293, 178, 122, 75],
        ErrorCorrectionLevel.Q: [207, 125, 86, 53],
        ErrorCorrectionLevel.H: [154, 93, 64, 39]
    },
    {
        ErrorCorrectionLevel.L: [461, 279, 192, 118],
        ErrorCorrectionLevel.M: [365, 221, 152, 93],
        ErrorCorrectionLevel.Q: [259, 157, 108, 66],
        ErrorCorrectionLevel.H: [202, 122, 84, 52]
    },
    {
        ErrorCorrectionLevel.L: [552, 335, 230, 141],
        ErrorCorrectionLevel.M: [432, 262, 180, 111],
        ErrorCorrectionLevel.Q: [312, 189, 130, 80],
        ErrorCorrectionLevel.H: [235, 143, 98, 60]
    },
    {
        ErrorCorrectionLevel.L: [652, 395, 271, 167],
        ErrorCorrectionLevel.M: [513, 311, 213, 131],
        ErrorCorrectionLevel.Q: [364, 221, 151, 93],
        ErrorCorrectionLevel.H: [288, 174, 119, 74]
    },
    {
        ErrorCorrectionLevel.L: [772, 468, 321, 198],
        ErrorCorrectionLevel.M: [604, 366, 251, 155],
        ErrorCorrectionLevel.Q: [427, 259, 177, 109],
        ErrorCorrectionLevel.H: [331, 200, 137, 85]
    },
    {
        ErrorCorrectionLevel.L: [883, 535, 367, 226],
        ErrorCorrectionLevel.M: [691, 419, 287, 177],
        ErrorCorrectionLevel.Q: [489, 296, 203, 125],
        ErrorCorrectionLevel.H: [374, 227, 155, 96]
    },
    {
        ErrorCorrectionLevel.L: [1022, 619, 425, 262],
        ErrorCorrectionLevel.M: [796, 483, 331, 204],
        ErrorCorrectionLevel.Q: [580, 352, 241, 149],
        ErrorCorrectionLevel.H: [427, 259, 177, 109]
    },
    {
        ErrorCorrectionLevel.L: [1101, 667, 458, 282],
        ErrorCorrectionLevel.M: [871, 528, 362, 223],
        ErrorCorrectionLevel.Q: [621, 376, 258, 159],
        ErrorCorrectionLevel.H: [468, 283, 194, 120]
    },
    {
        ErrorCorrectionLevel.L: [1250, 758, 520, 320],
        ErrorCorrectionLevel.M: [991, 600, 412, 254],
        ErrorCorrectionLevel.Q: [703, 426, 292, 180],
        ErrorCorrectionLevel.H: [530, 321, 220, 136]
    },
    {
        ErrorCorrectionLevel.L: [1408, 854, 586, 361],
        ErrorCorrectionLevel.M: [1082, 656, 450, 277],
        ErrorCorrectionLevel.Q: [775, 470, 322, 198],
        ErrorCorrectionLevel.H: [602, 365, 250, 154]
    },
    {
        ErrorCorrectionLevel.L: [1548, 938, 644, 397],
        ErrorCorrectionLevel.M: [1212, 734, 504, 310],
        ErrorCorrectionLevel.Q: [876, 531, 364, 224],
        ErrorCorrectionLevel.H: [674, 408, 280, 173]
    },
    {
        ErrorCorrectionLevel.L: [1725, 1046, 718, 442],
        ErrorCorrectionLevel.M: [1346, 816, 560, 345],
        ErrorCorrectionLevel.Q: [948, 574, 394, 243],
        ErrorCorrectionLevel.H: [746, 452, 310, 191]
    },
    {
        ErrorCorrectionLevel.L: [1903, 1153, 792, 488],
        ErrorCorrectionLevel.M: [1500, 909, 624, 384],
        ErrorCorrectionLevel.Q: [1063, 644, 442, 272],
        ErrorCorrectionLevel.H: [813, 493, 338, 208]
    },
    {
        ErrorCorrectionLevel.L: [2061, 1249, 858, 528],
        ErrorCorrectionLevel.M: [1600, 970, 666, 410],
        ErrorCorrectionLevel.Q: [1159, 702, 482, 297],
        ErrorCorrectionLevel.H: [919, 557, 382, 235]
    },
    {
        ErrorCorrectionLevel.L: [2232, 1352, 929, 572],
        ErrorCorrectionLevel.M: [1708, 1035, 711, 438],
        ErrorCorrectionLevel.Q: [1224, 742, 509, 314],
        ErrorCorrectionLevel.H: [969, 587, 403, 248]
    },
    {
        ErrorCorrectionLevel.L: [2409, 1460, 1003, 618],
        ErrorCorrectionLevel.M: [1872, 1134, 779, 480],
        ErrorCorrectionLevel.Q: [1358, 823, 565, 348],
        ErrorCorrectionLevel.H: [1056, 640, 439, 270]
    },
    {
        ErrorCorrectionLevel.L: [2620, 1588, 1091, 672],
        ErrorCorrectionLevel.M: [2059, 1248, 857, 528],
        ErrorCorrectionLevel.Q: [1468, 890, 611, 376],
        ErrorCorrectionLevel.H: [1108, 672, 461, 284]
    },
    {
        ErrorCorrectionLevel.L: [2812, 1704, 1171, 721],
        ErrorCorrectionLevel.M: [2188, 1326, 911, 561],
        ErrorCorrectionLevel.Q: [1588, 963, 661, 407],
        ErrorCorrectionLevel.H: [1228, 744, 511, 315]
    },
    {
        ErrorCorrectionLevel.L: [3057, 1853, 1273, 784],
        ErrorCorrectionLevel.M: [2395, 1451, 997, 614],
        ErrorCorrectionLevel.Q: [1718, 1041, 715, 440],
        ErrorCorrectionLevel.H: [1286, 779, 535, 330]
    },
    {
        ErrorCorrectionLevel.L: [3283, 1990, 1367, 842],
        ErrorCorrectionLevel.M: [2544, 1542, 1059, 652],
        ErrorCorrectionLevel.Q: [1804, 1094, 751, 462],
        ErrorCorrectionLevel.H: [1425, 864, 593, 365]
    },
    {
        ErrorCorrectionLevel.L: [3517, 2132, 1465, 902],
        ErrorCorrectionLevel.M: [2701, 1637, 1125, 692],
        ErrorCorrectionLevel.Q: [1933, 1172, 805, 496],
        ErrorCorrectionLevel.H: [1501, 910, 625, 385]
    },
    {
        ErrorCorrectionLevel.L: [3669, 2223, 1528, 940],
        ErrorCorrectionLevel.M: [2857, 1732, 1190, 732],
        ErrorCorrectionLevel.Q: [2085, 1263, 868, 534],
        ErrorCorrectionLevel.H: [1581, 958, 658, 405]
    },
    {
        ErrorCorrectionLevel.L: [3909, 2369, 1628, 1002],
        ErrorCorrectionLevel.M: [3035, 1839, 1264, 778],
        ErrorCorrectionLevel.Q: [2181, 1322, 908, 559],
        ErrorCorrectionLevel.H: [1677, 1016, 698, 430]
    },
    {
        ErrorCorrectionLevel.L: [4158, 2520, 1732, 1066],
        ErrorCorrectionLevel.M: [3289, 1994, 1370, 843],
        ErrorCorrectionLevel.Q: [2358, 1429, 982, 604],
        ErrorCorrectionLevel.H: [1782, 1080, 742, 457]
    },
    {
        ErrorCorrectionLevel.L: [4417, 2677, 1840, 1132],
        ErrorCorrectionLevel.M: [3486, 2113, 1452, 894],
        ErrorCorrectionLevel.Q: [2473, 1499, 1030, 634],
        ErrorCorrectionLevel.H: [1897, 1150, 790, 486]
    },
    {
        ErrorCorrectionLevel.L: [4686, 2840, 1952, 1201],
        ErrorCorrectionLevel.M: [3693, 2238, 1538, 947],
        ErrorCorrectionLevel.Q: [2670, 1618, 1112, 684],
        ErrorCorrectionLevel.H: [2022, 1226, 842, 518]
    },
    {
        ErrorCorrectionLevel.L: [4965, 3009, 2068, 1273],
        ErrorCorrectionLevel.M: [3909, 2369, 1628, 1002],
        ErrorCorrectionLevel.Q: [2805, 1700, 1168, 719],
        ErrorCorrectionLevel.H: [2157, 1307, 898, 553]
    },
    {
        ErrorCorrectionLevel.L: [5253, 3183, 2188, 1347],
        ErrorCorrectionLevel.M: [4134, 2506, 1722, 1060],
        ErrorCorrectionLevel.Q: [2949, 1787, 1228, 756],
        ErrorCorrectionLevel.H: [2301, 1394, 958, 590]
    },
    {
        ErrorCorrectionLevel.L: [5529, 3351, 2303, 1417],
        ErrorCorrectionLevel.M: [4343, 2632, 1809, 1113],
        ErrorCorrectionLevel.Q: [3081, 1867, 1283, 790],
        ErrorCorrectionLevel.H: [2361, 1431, 983, 605]
    },
    {
        ErrorCorrectionLevel.L: [5836, 3537, 2431, 1496],
        ErrorCorrectionLevel.M: [4588, 2780, 1911, 1176],
        ErrorCorrectionLevel.Q: [3244, 1966, 1351, 832],
        ErrorCorrectionLevel.H: [2524, 1530, 1051, 647]
    },
    {
        ErrorCorrectionLevel.L: [6153, 3729, 2563, 1577],
        ErrorCorrectionLevel.M: [4775, 2894, 1989, 1224],
        ErrorCorrectionLevel.Q: [3417, 2071, 1423, 876],
        ErrorCorrectionLevel.H: [2625, 1591, 1093, 673]
    },
    {
        ErrorCorrectionLevel.L: [6479, 3927, 2699, 1661],
        ErrorCorrectionLevel.M: [5039, 3054, 2099, 1292],
        ErrorCorrectionLevel.Q: [3599, 2181, 1499, 923],
        ErrorCorrectionLevel.H: [2735, 1658, 1139, 701]
    },
    {
        ErrorCorrectionLevel.L: [6743, 4087, 2809, 1729],
        ErrorCorrectionLevel.M: [5313, 3220, 2213, 1362],
        ErrorCorrectionLevel.Q: [3791, 2298, 1579, 972],
        ErrorCorrectionLevel.H: [2927, 1774, 1219, 750]
    },
    {
        ErrorCorrectionLevel.L: [7089, 4296, 2953, 1817],
        ErrorCorrectionLevel.M: [5596, 3391, 2331, 1435],
        ErrorCorrectionLevel.Q: [3993, 2420, 1663, 1024],
        ErrorCorrectionLevel.H: [3057, 1852, 1273, 784]
    }
]

error_correction_table = {
    ( 1, ErrorCorrectionLevel.L): (19, 7, 1, 19, 0, 0),
    ( 1, ErrorCorrectionLevel.M): (16, 10, 1, 16, 0, 0),
    ( 1, ErrorCorrectionLevel.Q): (13, 13, 1, 13, 0, 0),
    ( 1, ErrorCorrectionLevel.H): (9, 17, 1, 9, 0, 0),
    ( 2, ErrorCorrectionLevel.L): (34, 10, 1, 34, 0, 0),
    ( 2, ErrorCorrectionLevel.M): (28, 16, 1, 28, 0, 0),
    ( 2, ErrorCorrectionLevel.Q): (22, 22, 1, 22, 0, 0),
    ( 2, ErrorCorrectionLevel.H): (16, 28, 1, 16, 0, 0),
    ( 3, ErrorCorrectionLevel.L): (55, 15, 1, 55, 0, 0),
    ( 3, ErrorCorrectionLevel.M): (44, 26, 1, 44, 0, 0),
    ( 3, ErrorCorrectionLevel.Q): (34, 18, 2, 17, 0, 0),
    ( 3, ErrorCorrectionLevel.H): (26, 22, 2, 13, 0, 0),
    ( 4, ErrorCorrectionLevel.L): (80, 20, 1, 80, 0, 0),
    ( 4, ErrorCorrectionLevel.M): (64, 18, 2, 32, 0, 0),
    ( 4, ErrorCorrectionLevel.Q): (48, 26, 2, 24, 0, 0),
    ( 4, ErrorCorrectionLevel.H): (36, 16, 4, 9, 0, 0),
    ( 5, ErrorCorrectionLevel.L): (108, 26, 1, 108, 0, 0),
    ( 5, ErrorCorrectionLevel.M): (86, 24, 2, 43, 0, 0),
    ( 5, ErrorCorrectionLevel.Q): (62, 18, 2, 15, 2, 16),
    ( 5, ErrorCorrectionLevel.H): (46, 22, 2, 11, 2, 12),
    ( 6, ErrorCorrectionLevel.L): (136, 18, 2, 68, 0, 0),
    ( 6, ErrorCorrectionLevel.M): (108, 16, 4, 27, 0, 0),
    ( 6, ErrorCorrectionLevel.Q): (76, 24, 4, 19, 0, 0),
    ( 6, ErrorCorrectionLevel.H): (60, 28, 4, 15, 0, 0),
    ( 7, ErrorCorrectionLevel.L): (156, 20, 2, 78, 0, 0),
    ( 7, ErrorCorrectionLevel.M): (124, 18, 4, 31, 0, 0),
    ( 7, ErrorCorrectionLevel.Q): (88, 18, 2, 14, 4, 15),
    ( 7, ErrorCorrectionLevel.H): (66, 26, 4, 13, 1, 14),
    ( 8, ErrorCorrectionLevel.L): (194, 24, 2, 97, 0, 0),
    ( 8, ErrorCorrectionLevel.M): (154, 22, 2, 38, 2, 39),
    ( 8, ErrorCorrectionLevel.Q): (110, 22, 4, 18, 2, 19),
    ( 8, ErrorCorrectionLevel.H): (86, 26, 4, 14, 2, 15),
    ( 9, ErrorCorrectionLevel.L): (232, 30, 2, 116, 0, 0),
    ( 9, ErrorCorrectionLevel.M): (182, 22, 3, 36, 2, 37),
    ( 9, ErrorCorrectionLevel.Q): (132, 20, 4, 16, 4, 17),
    ( 9, ErrorCorrectionLevel.H): (100, 24, 4, 12, 4, 13),
    (10, ErrorCorrectionLevel.L): (274, 18, 2, 68, 2, 69),
    (10, ErrorCorrectionLevel.M): (216, 26, 4, 43, 1, 44),
    (10, ErrorCorrectionLevel.Q): (154, 24, 6, 19, 2, 20),
    (10, ErrorCorrectionLevel.H): (122, 28, 6, 15, 2, 16),
    (11, ErrorCorrectionLevel.L): (324, 20, 4, 81, 0, 0),
    (11, ErrorCorrectionLevel.M): (254, 30, 1, 50, 4, 51),
    (11, ErrorCorrectionLevel.Q): (180, 28, 4, 22, 4, 23),
    (11, ErrorCorrectionLevel.H): (140, 24, 3, 12, 8, 13),
    (12, ErrorCorrectionLevel.L): (370, 24, 2, 92, 2, 93),
    (12, ErrorCorrectionLevel.M): (290, 22, 6, 36, 2, 37),
    (12, ErrorCorrectionLevel.Q): (206, 26, 4, 20, 6, 21),
    (12, ErrorCorrectionLevel.H): (158, 28, 7, 14, 4, 15),
    (13, ErrorCorrectionLevel.L): (428, 26, 4, 107, 0, 0),
    (13, ErrorCorrectionLevel.M): (334, 22, 8, 37, 1, 38),
    (13, ErrorCorrectionLevel.Q): (244, 24, 8, 20, 4, 21),
    (13, ErrorCorrectionLevel.H): (180, 22, 12, 11, 4, 12),
    (14, ErrorCorrectionLevel.L): (461, 30, 3, 115, 1, 116),
    (14, ErrorCorrectionLevel.M): (365, 24, 4, 40, 5, 41),
    (14, ErrorCorrectionLevel.Q): (261, 20, 11, 16, 5, 17),
    (14, ErrorCorrectionLevel.H): (197, 24, 11, 12, 5, 13),
    (15, ErrorCorrectionLevel.L): (523, 22, 5, 87, 1, 88),
    (15, ErrorCorrectionLevel.M): (415, 24, 5, 41, 5, 42),
    (15, ErrorCorrectionLevel.Q): (295, 30, 5, 24, 7, 25),
    (15, ErrorCorrectionLevel.H): (223, 24, 11, 12, 7, 13),
    (16, ErrorCorrectionLevel.L): (589, 24, 5, 98, 1, 99),
    (16, ErrorCorrectionLevel.M): (453, 28, 7, 45, 3, 46),
    (16, ErrorCorrectionLevel.Q): (325, 24, 15, 19, 2, 20),
    (16, ErrorCorrectionLevel.H): (253, 30, 3, 15, 13, 16),
    (17, ErrorCorrectionLevel.L): (647, 28, 1, 107, 5, 108),
    (17, ErrorCorrectionLevel.M): (507, 28, 10, 46, 1, 47),
    (17, ErrorCorrectionLevel.Q): (367, 28, 1, 22, 15, 23),
    (17, ErrorCorrectionLevel.H): (283, 28, 2, 14, 17, 15),
    (18, ErrorCorrectionLevel.L): (721, 30, 5, 120, 1, 121),
    (18, ErrorCorrectionLevel.M): (563, 26, 9, 43, 4, 44),
    (18, ErrorCorrectionLevel.Q): (397, 28, 17, 22, 1, 23),
    (18, ErrorCorrectionLevel.H): (313, 28, 2, 14, 19, 15),
    (19, ErrorCorrectionLevel.L): (795, 28, 3, 113, 4, 114),
    (19, ErrorCorrectionLevel.M): (627, 26, 3, 44, 11, 45),
    (19, ErrorCorrectionLevel.Q): (445, 26, 17, 21, 4, 22),
    (19, ErrorCorrectionLevel.H): (341, 26, 9, 13, 16, 14),
    (20, ErrorCorrectionLevel.L): (861, 28, 3, 107, 5, 108),
    (20, ErrorCorrectionLevel.M): (669, 26, 3, 41, 13, 42),
    (20, ErrorCorrectionLevel.Q): (485, 30, 15, 24, 5, 25),
    (20, ErrorCorrectionLevel.H): (385, 28, 15, 15, 10, 16),
    (21, ErrorCorrectionLevel.L): (932, 28, 4, 116, 4, 117),
    (21, ErrorCorrectionLevel.M): (714, 26, 17, 42, 0, 0),
    (21, ErrorCorrectionLevel.Q): (512, 28, 17, 22, 6, 23),
    (21, ErrorCorrectionLevel.H): (406, 30, 19, 16, 6, 17),
    (22, ErrorCorrectionLevel.L): (1006, 28, 2, 111, 7, 112),
    (22, ErrorCorrectionLevel.M): (782, 28, 17, 46, 0, 0),
    (22, ErrorCorrectionLevel.Q): (568, 30, 7, 24, 16, 25),
    (22, ErrorCorrectionLevel.H): (442, 24, 34, 13, 0, 0),
    (23, ErrorCorrectionLevel.L): (1094, 30, 4, 121, 5, 122),
    (23, ErrorCorrectionLevel.M): (860, 28, 4, 47, 14, 48),
    (23, ErrorCorrectionLevel.Q): (614, 30, 11, 24, 14, 25),
    (23, ErrorCorrectionLevel.H): (464, 30, 16, 15, 14, 16),
    (24, ErrorCorrectionLevel.L): (1174, 30, 6, 117, 4, 118),
    (24, ErrorCorrectionLevel.M): (914, 28, 6, 45, 14, 46),
    (24, ErrorCorrectionLevel.Q): (664, 30, 11, 24, 16, 25),
    (24, ErrorCorrectionLevel.H): (514, 30, 30, 16, 2, 17),
    (25, ErrorCorrectionLevel.L): (1276, 26, 8, 106, 4, 107),
    (25, ErrorCorrectionLevel.M): (1000, 28, 8, 47, 13, 48),
    (25, ErrorCorrectionLevel.Q): (718, 30, 7, 24, 22, 25),
    (25, ErrorCorrectionLevel.H): (538, 30, 22, 15, 13, 16),
    (26, ErrorCorrectionLevel.L): (1370, 28, 10, 114, 2, 115),
    (26, ErrorCorrectionLevel.M): (1062, 28, 19, 46, 4, 47),
    (26, ErrorCorrectionLevel.Q): (754, 28, 28, 22, 6, 23),
    (26, ErrorCorrectionLevel.H): (596, 30, 33, 16, 4, 17),
    (27, ErrorCorrectionLevel.L): (1468, 30, 8, 122, 4, 123),
    (27, ErrorCorrectionLevel.M): (1128, 28, 22, 45, 3, 46),
    (27, ErrorCorrectionLevel.Q): (808, 30, 8, 23, 26, 24), 
    (27, ErrorCorrectionLevel.H): (628, 30, 12, 15, 28, 16),
    (28, ErrorCorrectionLevel.L): (1531, 30, 3, 117, 10, 118),
    (28, ErrorCorrectionLevel.M): (1193, 28, 3, 45, 23, 46),
    (28, ErrorCorrectionLevel.Q): (871, 30, 4, 24, 31, 25),
    (28, ErrorCorrectionLevel.H): (661, 30, 11, 15, 31, 16),
    (29, ErrorCorrectionLevel.L): (1631, 30, 7, 116, 7, 117),
    (29, ErrorCorrectionLevel.M): (1267, 28, 21, 45, 7, 46),
    (29, ErrorCorrectionLevel.Q): (911, 30, 1, 23, 37, 24),
    (29, ErrorCorrectionLevel.H): (701, 30, 19, 15, 26, 16),
    (30, ErrorCorrectionLevel.L): (1735, 30, 5, 115, 10, 116),
    (30, ErrorCorrectionLevel.M): (1373, 28, 19, 47, 10, 48),
    (30, ErrorCorrectionLevel.Q): (985, 30, 15, 24, 25, 25),
    (30, ErrorCorrectionLevel.H): (745, 30, 23, 15, 25, 16),
    (31, ErrorCorrectionLevel.L): (1843, 30, 13, 115, 3, 116),
    (31, ErrorCorrectionLevel.M): (1455, 28, 2, 46, 29, 47),
    (31, ErrorCorrectionLevel.Q): (1033, 30, 42, 24, 1, 25),
    (31, ErrorCorrectionLevel.H): (793, 30, 23, 15, 28, 16),
    (32, ErrorCorrectionLevel.L): (1955, 30, 17, 115, 0, 0),
    (32, ErrorCorrectionLevel.M): (1541, 28, 10, 46, 23, 47),
    (32, ErrorCorrectionLevel.Q): (1115, 30, 10, 24, 35, 25),
    (32, ErrorCorrectionLevel.H): (845, 30, 19, 15, 35, 16),
    (33, ErrorCorrectionLevel.L): (2071, 30, 17, 115, 1, 116),
    (33, ErrorCorrectionLevel.M): (1631, 28, 14, 46, 21, 47),
    (33, ErrorCorrectionLevel.Q): (1171, 30, 29, 24, 19, 25),
    (33, ErrorCorrectionLevel.H): (901, 30, 11, 15, 46, 16),
    (34, ErrorCorrectionLevel.L): (2191, 30, 13, 115, 6, 116),
    (34, ErrorCorrectionLevel.M): (1725, 28, 14, 46, 23, 47),
    (34, ErrorCorrectionLevel.Q): (1231, 30, 44, 24, 7, 25),
    (34, ErrorCorrectionLevel.H): (961, 30, 59, 16, 1, 17),
    (35, ErrorCorrectionLevel.L): (2306, 30, 12, 121, 7, 122),
    (35, ErrorCorrectionLevel.M): (1812, 28, 12, 47, 26, 48),
    (35, ErrorCorrectionLevel.Q): (1286, 30, 39, 24, 14, 25),
    (35, ErrorCorrectionLevel.H): (986, 30, 22, 15, 41, 16),
    (36, ErrorCorrectionLevel.L): (2434, 30, 6, 121, 14, 122),
    (36, ErrorCorrectionLevel.M): (1914, 28, 6, 47, 34, 48),
    (36, ErrorCorrectionLevel.Q): (1354, 30, 46, 24, 10, 25),
    (36, ErrorCorrectionLevel.H): (1054, 30, 2, 15, 64, 16),
    (37, ErrorCorrectionLevel.L): (2566, 30, 17, 122, 4, 123), 
    (37, ErrorCorrectionLevel.M): (1992, 28, 29, 46, 14, 47),
    (37, ErrorCorrectionLevel.Q): (1426, 30, 49, 24, 10, 25),
    (37, ErrorCorrectionLevel.H): (1096, 30, 24, 15, 46, 16),
    (38, ErrorCorrectionLevel.L): (2702, 30, 4, 122, 18, 123),
    (38, ErrorCorrectionLevel.M): (2102, 28, 13, 46, 32, 47),
    (38, ErrorCorrectionLevel.Q): (1502, 30, 48, 24, 14, 25),
    (38, ErrorCorrectionLevel.H): (1142, 30, 42, 15, 32, 16),
    (39, ErrorCorrectionLevel.L): (2812, 30, 20, 117, 4, 118),
    (39, ErrorCorrectionLevel.M): (2216, 28, 40, 47, 7, 48),
    (39, ErrorCorrectionLevel.Q): (1582, 30, 43, 24, 22, 25),
    (39, ErrorCorrectionLevel.H): (1222, 30, 10, 15, 67, 16),
    (40, ErrorCorrectionLevel.L): (2956, 30, 19, 118, 6, 119),
    (40, ErrorCorrectionLevel.M): (2334, 28, 18, 47, 31, 48),
    (40, ErrorCorrectionLevel.Q): (1666, 30, 34, 24, 34, 25),
    (40, ErrorCorrectionLevel.H): (1276, 30, 20, 15, 61, 16)
}

remainder_bits_table = [0, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0]

alignment_pattern_locations_table = {
    2: [6, 18],
    3: [6, 22],
    4: [6, 26],
    5: [6, 30],
    6: [6, 34],
    7: [6, 22, 38],
    8: [6, 24, 42],
    9: [6, 26, 46],
    10: [6, 28, 50],
    11: [6, 30, 54],
    12: [6, 32, 58],
    13: [6, 34, 62],
    14: [6, 26, 46, 66],
    15: [6, 26, 48, 70],
    16: [6, 26, 50, 74],
    17: [6, 30, 54, 78],
    18: [6, 30, 56, 82],
    19: [6, 30, 58, 86],
    20: [6, 34, 62, 90],
    21: [6, 28, 50, 72, 94],
    22: [6, 26, 50, 74, 98],
    23: [6, 30, 54, 78, 102],
    24: [6, 28, 54, 80, 106],
    25: [6, 32, 58, 84, 110],
    26: [6, 30, 58, 86, 114],
    27: [6, 34, 62, 90, 118],
    28: [6, 26, 50, 74, 98, 122],
    29: [6, 30, 54, 78, 102, 126],
    30: [6, 26, 52, 78, 104, 130],
    31: [6, 30, 56, 82, 108, 134],
    32: [6, 34, 60, 86, 112, 138],
    33: [6, 30, 58, 86, 114, 142],
    34: [6, 34, 62, 90, 118, 146],
    35: [6, 30, 54, 78, 102, 126, 150],
    36: [6, 24, 50, 76, 102, 128, 154],
    37: [6, 28, 54, 80, 106, 132, 158],
    38: [6, 32, 58, 84, 110, 136, 162],
    39: [6, 26, 54, 82, 110, 138, 166],
    40: [6, 30, 58, 86, 114, 142, 170]
}

format_information_string = {
    (ErrorCorrectionLevel.L, 0): '111011111000100',
    (ErrorCorrectionLevel.L, 1): '111001011110011',
    (ErrorCorrectionLevel.L, 2): '111110110101010',
    (ErrorCorrectionLevel.L, 3): '111100010011101',
    (ErrorCorrectionLevel.L, 4): '110011000101111',
    (ErrorCorrectionLevel.L, 5): '110001100011000',
    (ErrorCorrectionLevel.L, 6): '110110001000001',
    (ErrorCorrectionLevel.L, 7): '110100101110110',
    (ErrorCorrectionLevel.M, 0): '101010000010010',
    (ErrorCorrectionLevel.M, 1): '101000100100101',
    (ErrorCorrectionLevel.M, 2): '101111001111100',
    (ErrorCorrectionLevel.M, 3): '101101101001011',
    (ErrorCorrectionLevel.M, 4): '100010111111001',
    (ErrorCorrectionLevel.M, 5): '100000011001110',
    (ErrorCorrectionLevel.M, 6): '100111110010111',
    (ErrorCorrectionLevel.M, 7): '100101010100000',
    (ErrorCorrectionLevel.Q, 0): '011010101011111',
    (ErrorCorrectionLevel.Q, 1): '011000001101000',
    (ErrorCorrectionLevel.Q, 2): '011111100110001',
    (ErrorCorrectionLevel.Q, 3): '011101000000110',
    (ErrorCorrectionLevel.Q, 4): '010010010110100',
    (ErrorCorrectionLevel.Q, 5): '010000110000011',
    (ErrorCorrectionLevel.Q, 6): '010111011011010',
    (ErrorCorrectionLevel.Q, 7): '010101111101101',
    (ErrorCorrectionLevel.H, 0): '001011010001001',
    (ErrorCorrectionLevel.H, 1): '001001110111110',
    (ErrorCorrectionLevel.H, 2): '001110011100111',
    (ErrorCorrectionLevel.H, 3): '001100111010000',
    (ErrorCorrectionLevel.H, 4): '000011101100010',
    (ErrorCorrectionLevel.H, 5): '000001001010101',
    (ErrorCorrectionLevel.H, 6): '000110100001100',
    (ErrorCorrectionLevel.H, 7): '000100000111011'
}

version_information_string = {
    7: '000111110010010100',
    8: '001000010110111100',
    9: '001001101010011001',
    10: '001010010011010011',
    11: '001011101111110110',
    12: '001100011101100010',
    13: '001101100001000111',
    14: '001110011000001101',
    15: '001111100100101000',
    16: '010000101101111000',
    17: '010001010001011101',
    18: '010010101000010111',
    19: '010011010100110010',
    20: '010100100110100110',
    21: '010101011010000011',
    22: '010110100011001001',
    23: '010111011111101100',
    24: '011000111011000100',
    25: '011001000111100001',
    26: '011010111110101011',
    27: '011011000010001110',
    28: '011100110000011010',
    29: '011101001100111111',
    30: '011110110101110101',
    31: '011111001001010000',
    32: '100000100111010101',
    33: '100001011011110000',
    34: '100010100010111010',
    35: '100011011110011111',
    36: '100100101100001011',
    37: '100101010000101110',
    38: '100110101001100100',
    39: '100111010101000001',
    40: '101000110001101001'
}

char_count_byte_length_for_version_and_mode = {
    SizeLevel.small : {
        ModeIndicator.numeric_mode : 10,
        ModeIndicator.alphanumeric_mode : 9,
        ModeIndicator.byte_mode : 8,
        ModeIndicator.kanji_mode : 8
    },
    SizeLevel.medium : {
        ModeIndicator.numeric_mode : 12,
        ModeIndicator.alphanumeric_mode : 11,
        ModeIndicator.byte_mode : 16,
        ModeIndicator.kanji_mode : 10
    },
    SizeLevel.large : {
        ModeIndicator.numeric_mode : 14,
        ModeIndicator.alphanumeric_mode : 13,
        ModeIndicator.byte_mode : 16,
        ModeIndicator.kanji_mode : 12
    }
}

mode_indicator_mapping = {
    ModeIndicator.numeric_mode: "0001", 
    ModeIndicator.alphanumeric_mode: "0010", 
    ModeIndicator.byte_mode: "0100", 
    ModeIndicator.kanji_mode: "1000"
}

def main():
    version_dict_file = load_pickle_file("resources/version.pickle")
    assert version_dict_file == version_dict, "version_dict is not correct"

    error_correction_table_file = load_pickle_file("resources/error_correction_table.pickle")
    assert error_correction_table_file == error_correction_table, "error_correction_table is not correct"

    remainder_bits_table_file = load_pickle_file("resources/remainder_bits.pickle")
    assert remainder_bits_table_file == remainder_bits_table, "remainder_bits_table is not correct"

    alignment_pattern_locations_table_file = load_pickle_file("resources/alignment_pattern_locations_table.pickle")
    assert alignment_pattern_locations_table_file == alignment_pattern_locations_table, "alignment_pattern_locations_table is not correct"
    
    format_information_string_file = load_pickle_file("resources/format_information_string.pickle")
    assert format_information_string_file == format_information_string, "format_information_string is not correct"
    
    version_information_string_file = load_pickle_file("resources/version_information_string.pickle")
    assert version_information_string_file == version_information_string, "version_information_string is not correct"

if __name__ == "__main__":
    main()