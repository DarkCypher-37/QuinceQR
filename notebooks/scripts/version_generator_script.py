# https://www.thonky.com/qr-code-tutorial/character-capacities

import pickle
import json
from enum import Enum

class ErrorCorrectionLevel(Enum):
    L = 1
    M = 2
    Q = 3
    H = 4


# version_dict[version-1][ErrorCorrectionLevel.XX.value][ModeIndicator.YY]
# XX: L, M, H, Q
# YY: numeric, alphanumeric, byte, kanji
version_dict = [{
        ErrorCorrectionLevel.L.value: [41, 25, 17, 10],
        ErrorCorrectionLevel.M.value: [34, 20, 14, 8],
        ErrorCorrectionLevel.Q.value: [27, 16, 11, 7],
        ErrorCorrectionLevel.H.value: [17, 10, 7, 4]
    },
    {
        ErrorCorrectionLevel.L.value: [77, 47, 32, 20],
        ErrorCorrectionLevel.M.value: [63, 38, 26, 16],
        ErrorCorrectionLevel.Q.value: [48, 29, 20, 12],
        ErrorCorrectionLevel.H.value: [34, 20, 14, 8]
    },
    {
        ErrorCorrectionLevel.L.value: [127, 77, 53, 32],
        ErrorCorrectionLevel.M.value: [101, 61, 42, 26],
        ErrorCorrectionLevel.Q.value: [77, 47, 32, 20],
        ErrorCorrectionLevel.H.value: [58, 35, 24, 15]
    },
    {
        ErrorCorrectionLevel.L.value: [187, 114, 78, 48],
        ErrorCorrectionLevel.M.value: [149, 90, 62, 38],
        ErrorCorrectionLevel.Q.value: [111, 67, 46, 28],
        ErrorCorrectionLevel.H.value: [82, 50, 34, 21]
    },
    {
        ErrorCorrectionLevel.L.value: [255, 154, 106, 65],
        ErrorCorrectionLevel.M.value: [202, 122, 84, 52],
        ErrorCorrectionLevel.Q.value: [144, 87, 60, 37],
        ErrorCorrectionLevel.H.value: [106, 64, 44, 27]
    },
    {
        ErrorCorrectionLevel.L.value: [322, 195, 134, 82],
        ErrorCorrectionLevel.M.value: [255, 154, 106, 65],
        ErrorCorrectionLevel.Q.value: [178, 108, 74, 45],
        ErrorCorrectionLevel.H.value: [139, 84, 58, 36]
    },
    {
        ErrorCorrectionLevel.L.value: [370, 224, 154, 95],
        ErrorCorrectionLevel.M.value: [293, 178, 122, 75],
        ErrorCorrectionLevel.Q.value: [207, 125, 86, 53],
        ErrorCorrectionLevel.H.value: [154, 93, 64, 39]
    },
    {
        ErrorCorrectionLevel.L.value: [461, 279, 192, 118],
        ErrorCorrectionLevel.M.value: [365, 221, 152, 93],
        ErrorCorrectionLevel.Q.value: [259, 157, 108, 66],
        ErrorCorrectionLevel.H.value: [202, 122, 84, 52]
    },
    {
        ErrorCorrectionLevel.L.value: [552, 335, 230, 141],
        ErrorCorrectionLevel.M.value: [432, 262, 180, 111],
        ErrorCorrectionLevel.Q.value: [312, 189, 130, 80],
        ErrorCorrectionLevel.H.value: [235, 143, 98, 60]
    },
    {
        ErrorCorrectionLevel.L.value: [652, 395, 271, 167],
        ErrorCorrectionLevel.M.value: [513, 311, 213, 131],
        ErrorCorrectionLevel.Q.value: [364, 221, 151, 93],
        ErrorCorrectionLevel.H.value: [288, 174, 119, 74]
    },
    {
        ErrorCorrectionLevel.L.value: [772, 468, 321, 198],
        ErrorCorrectionLevel.M.value: [604, 366, 251, 155],
        ErrorCorrectionLevel.Q.value: [427, 259, 177, 109],
        ErrorCorrectionLevel.H.value: [331, 200, 137, 85]
    },
    {
        ErrorCorrectionLevel.L.value: [883, 535, 367, 226],
        ErrorCorrectionLevel.M.value: [691, 419, 287, 177],
        ErrorCorrectionLevel.Q.value: [489, 296, 203, 125],
        ErrorCorrectionLevel.H.value: [374, 227, 155, 96]
    },
    {
        ErrorCorrectionLevel.L.value: [1022, 619, 425, 262],
        ErrorCorrectionLevel.M.value: [796, 483, 331, 204],
        ErrorCorrectionLevel.Q.value: [580, 352, 241, 149],
        ErrorCorrectionLevel.H.value: [427, 259, 177, 109]
    },
    {
        ErrorCorrectionLevel.L.value: [1101, 667, 458, 282],
        ErrorCorrectionLevel.M.value: [871, 528, 362, 223],
        ErrorCorrectionLevel.Q.value: [621, 376, 258, 159],
        ErrorCorrectionLevel.H.value: [468, 283, 194, 120]
    },
    {
        ErrorCorrectionLevel.L.value: [1250, 758, 520, 320],
        ErrorCorrectionLevel.M.value: [991, 600, 412, 254],
        ErrorCorrectionLevel.Q.value: [703, 426, 292, 180],
        ErrorCorrectionLevel.H.value: [530, 321, 220, 136]
    },
    {
        ErrorCorrectionLevel.L.value: [1408, 854, 586, 361],
        ErrorCorrectionLevel.M.value: [1082, 656, 450, 277],
        ErrorCorrectionLevel.Q.value: [775, 470, 322, 198],
        ErrorCorrectionLevel.H.value: [602, 365, 250, 154]
    },
    {
        ErrorCorrectionLevel.L.value: [1548, 938, 644, 397],
        ErrorCorrectionLevel.M.value: [1212, 734, 504, 310],
        ErrorCorrectionLevel.Q.value: [876, 531, 364, 224],
        ErrorCorrectionLevel.H.value: [674, 408, 280, 173]
    },
    {
        ErrorCorrectionLevel.L.value: [1725, 1046, 718, 442],
        ErrorCorrectionLevel.M.value: [1346, 816, 560, 345],
        ErrorCorrectionLevel.Q.value: [948, 574, 394, 243],
        ErrorCorrectionLevel.H.value: [746, 452, 310, 191]
    },
    {
        ErrorCorrectionLevel.L.value: [1903, 1153, 792, 488],
        ErrorCorrectionLevel.M.value: [1500, 909, 624, 384],
        ErrorCorrectionLevel.Q.value: [1063, 644, 442, 272],
        ErrorCorrectionLevel.H.value: [813, 493, 338, 208]
    },
    {
        ErrorCorrectionLevel.L.value: [2061, 1249, 858, 528],
        ErrorCorrectionLevel.M.value: [1600, 970, 666, 410],
        ErrorCorrectionLevel.Q.value: [1159, 702, 482, 297],
        ErrorCorrectionLevel.H.value: [919, 557, 382, 235]
    },
    {
        ErrorCorrectionLevel.L.value: [2232, 1352, 929, 572],
        ErrorCorrectionLevel.M.value: [1708, 1035, 711, 438],
        ErrorCorrectionLevel.Q.value: [1224, 742, 509, 314],
        ErrorCorrectionLevel.H.value: [969, 587, 403, 248]
    },
    {
        ErrorCorrectionLevel.L.value: [2409, 1460, 1003, 618],
        ErrorCorrectionLevel.M.value: [1872, 1134, 779, 480],
        ErrorCorrectionLevel.Q.value: [1358, 823, 565, 348],
        ErrorCorrectionLevel.H.value: [1056, 640, 439, 270]
    },
    {
        ErrorCorrectionLevel.L.value: [2620, 1588, 1091, 672],
        ErrorCorrectionLevel.M.value: [2059, 1248, 857, 528],
        ErrorCorrectionLevel.Q.value: [1468, 890, 611, 376],
        ErrorCorrectionLevel.H.value: [1108, 672, 461, 284]
    },
    {
        ErrorCorrectionLevel.L.value: [2812, 1704, 1171, 721],
        ErrorCorrectionLevel.M.value: [2188, 1326, 911, 561],
        ErrorCorrectionLevel.Q.value: [1588, 963, 661, 407],
        ErrorCorrectionLevel.H.value: [1228, 744, 511, 315]
    },
    {
        ErrorCorrectionLevel.L.value: [3057, 1853, 1273, 784],
        ErrorCorrectionLevel.M.value: [2395, 1451, 997, 614],
        ErrorCorrectionLevel.Q.value: [1718, 1041, 715, 440],
        ErrorCorrectionLevel.H.value: [1286, 779, 535, 330]
    },
    {
        ErrorCorrectionLevel.L.value: [3283, 1990, 1367, 842],
        ErrorCorrectionLevel.M.value: [2544, 1542, 1059, 652],
        ErrorCorrectionLevel.Q.value: [1804, 1094, 751, 462],
        ErrorCorrectionLevel.H.value: [1425, 864, 593, 365]
    },
    {
        ErrorCorrectionLevel.L.value: [3517, 2132, 1465, 902],
        ErrorCorrectionLevel.M.value: [2701, 1637, 1125, 692],
        ErrorCorrectionLevel.Q.value: [1933, 1172, 805, 496],
        ErrorCorrectionLevel.H.value: [1501, 910, 625, 385]
    },
    {
        ErrorCorrectionLevel.L.value: [3669, 2223, 1528, 940],
        ErrorCorrectionLevel.M.value: [2857, 1732, 1190, 732],
        ErrorCorrectionLevel.Q.value: [2085, 1263, 868, 534],
        ErrorCorrectionLevel.H.value: [1581, 958, 658, 405]
    },
    {
        ErrorCorrectionLevel.L.value: [3909, 2369, 1628, 1002],
        ErrorCorrectionLevel.M.value: [3035, 1839, 1264, 778],
        ErrorCorrectionLevel.Q.value: [2181, 1322, 908, 559],
        ErrorCorrectionLevel.H.value: [1677, 1016, 698, 430]
    },
    {
        ErrorCorrectionLevel.L.value: [4158, 2520, 1732, 1066],
        ErrorCorrectionLevel.M.value: [3289, 1994, 1370, 843],
        ErrorCorrectionLevel.Q.value: [2358, 1429, 982, 604],
        ErrorCorrectionLevel.H.value: [1782, 1080, 742, 457]
    },
    {
        ErrorCorrectionLevel.L.value: [4417, 2677, 1840, 1132],
        ErrorCorrectionLevel.M.value: [3486, 2113, 1452, 894],
        ErrorCorrectionLevel.Q.value: [2473, 1499, 1030, 634],
        ErrorCorrectionLevel.H.value: [1897, 1150, 790, 486]
    },
    {
        ErrorCorrectionLevel.L.value: [4686, 2840, 1952, 1201],
        ErrorCorrectionLevel.M.value: [3693, 2238, 1538, 947],
        ErrorCorrectionLevel.Q.value: [2670, 1618, 1112, 684],
        ErrorCorrectionLevel.H.value: [2022, 1226, 842, 518]
    },
    {
        ErrorCorrectionLevel.L.value: [4965, 3009, 2068, 1273],
        ErrorCorrectionLevel.M.value: [3909, 2369, 1628, 1002],
        ErrorCorrectionLevel.Q.value: [2805, 1700, 1168, 719],
        ErrorCorrectionLevel.H.value: [2157, 1307, 898, 553]
    },
    {
        ErrorCorrectionLevel.L.value: [5253, 3183, 2188, 1347],
        ErrorCorrectionLevel.M.value: [4134, 2506, 1722, 1060],
        ErrorCorrectionLevel.Q.value: [2949, 1787, 1228, 756],
        ErrorCorrectionLevel.H.value: [2301, 1394, 958, 590]
    },
    {
        ErrorCorrectionLevel.L.value: [5529, 3351, 2303, 1417],
        ErrorCorrectionLevel.M.value: [4343, 2632, 1809, 1113],
        ErrorCorrectionLevel.Q.value: [3081, 1867, 1283, 790],
        ErrorCorrectionLevel.H.value: [2361, 1431, 983, 605]
    },
    {
        ErrorCorrectionLevel.L.value: [5836, 3537, 2431, 1496],
        ErrorCorrectionLevel.M.value: [4588, 2780, 1911, 1176],
        ErrorCorrectionLevel.Q.value: [3244, 1966, 1351, 832],
        ErrorCorrectionLevel.H.value: [2524, 1530, 1051, 647]
    },
    {
        ErrorCorrectionLevel.L.value: [6153, 3729, 2563, 1577],
        ErrorCorrectionLevel.M.value: [4775, 2894, 1989, 1224],
        ErrorCorrectionLevel.Q.value: [3417, 2071, 1423, 876],
        ErrorCorrectionLevel.H.value: [2625, 1591, 1093, 673]
    },
    {
        ErrorCorrectionLevel.L.value: [6479, 3927, 2699, 1661],
        ErrorCorrectionLevel.M.value: [5039, 3054, 2099, 1292],
        ErrorCorrectionLevel.Q.value: [3599, 2181, 1499, 923],
        ErrorCorrectionLevel.H.value: [2735, 1658, 1139, 701]
    },
    {
        ErrorCorrectionLevel.L.value: [6743, 4087, 2809, 1729],
        ErrorCorrectionLevel.M.value: [5313, 3220, 2213, 1362],
        ErrorCorrectionLevel.Q.value: [3791, 2298, 1579, 972],
        ErrorCorrectionLevel.H.value: [2927, 1774, 1219, 750]
    },
    {
        ErrorCorrectionLevel.L.value: [7089, 4296, 2953, 1817],
        ErrorCorrectionLevel.M.value: [5596, 3391, 2331, 1435],
        ErrorCorrectionLevel.Q.value: [3993, 2420, 1663, 1024],
        ErrorCorrectionLevel.H.value: [3057, 1852, 1273, 784]
    }
]

# filepath = "resources/version.pickle"
filepath = "notebooks/scripts/version.pickle"

# JSON
# with open(filepath, "w") as file:
#     json.dump(version_dict, file, indent=2)

# PICKLE
with open(filepath, 'wb') as file:
    pickle.dump(version_dict, file, protocol=pickle.HIGHEST_PROTOCOL)