# https://www.thonky.com/qr-code-tutorial/character-capacities

import pickle
from enum import Enum

class ErrorCorrectionLevel(Enum):
    L = 1
    M = 2
    Q = 3
    H = 4

# version_dict[version-1][ErrorCorrectionLevel.XX][ModeIndicator.YY]
# XX: L, M, H, Q
# YY: numeric, alphanumeric, byte, kanji
version_dict = [{
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

filepath = "resources/version.pickle"
# filepath = "notebooks/scripts/version.pickle"

# JSON
# with open(filepath, "w") as file:
#     json.dump(version_dict, file, indent=2)

# PICKLE
with open(filepath, 'wb') as file:
    pickle.dump(version_dict, file, protocol=pickle.HIGHEST_PROTOCOL)