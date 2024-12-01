import numpy as np
from enum import Enum
import time


# np_array = np.array([
#     [1, 2, 3],
#     [4, 5, 6],
#     [7, 8, 9],
# ])
# print(f"np_array:\n{np_array}")
# print(f"np_array.sum(): {np_array.sum()}")
# np_array = np.flip(np_array)
# print(f"reverse of np_array:\n{np_array}")


""" Matris vektörel işlem performansı test """
# size_x = 1000
# size_y = 1000
# arr = np.zeros((size_x, size_y), dtype=int)
#
# current_time = time.time()
# print(current_time)
# for y in range(size_y):
#     for x in range(size_x):
#         arr[y][x] = 6 - arr[y][x]
# print(f"Normal döngü içerisidneki işlem süresi: {time.time() - current_time}")
# print(arr[-5:][-5:])
#
# current_time = time.time()
# arr = 6 - arr
# print(f"Vektörel kullanım içerisidneki işlem süresi: {time.time() - current_time}")
# print(arr[-5:][-5:])



# """ Matris skor hesaplama yöntemlerinin performans testleri """
#
# SCORE_DICT = {
#     3: np.zeros((8, 8), dtype=int),
#     1: np.array([
#         [0, 0, 0, 0, 0, 0, 0, 0],
#         [-15, -10, -10, -10, -10, -10, -10, -15],
#         [-18, -12, -12, -12, -12, -12, -12, -18],
#         [-21, -14, -14, -14, -14, -14, -14, -21],
#         [-24, -16, -16, -16, -16, -16, -16, -24],
#         [-27, -18, -18, -18, -18, -18, -18, -27],
#         [-30, -20, -20, -20, -20, -20, -20, -30],
#         [0, 0, 0, 0, 0, 0, 0, 0],
#     ], dtype=int),
#     2: np.array([
#         [-64, -48, -48, -48, -48, -48, -48, -64],
#         [-48, -32, -32, -32, -32, -32, -32, -48],
#         [-48, -32, -32, -32, -32, -32, -32, -48],
#         [-48, -32, -32, -32, -32, -32, -32, -48],
#         [-48, -32, -32, -32, -32, -32, -32, -48],
#         [-48, -32, -32, -32, -32, -32, -32, -48],
#         [-48, -32, -32, -32, -32, -32, -32, -48],
#         [-64, -48, -48, -48, -48, -48, -48, -64],
#     ], dtype=int),
#     4: np.array([
#         [64, 48, 48, 48, 48, 48, 48, 64],
#         [48, 32, 32, 32, 32, 32, 32, 48],
#         [48, 32, 32, 32, 32, 32, 32, 48],
#         [48, 32, 32, 32, 32, 32, 32, 48],
#         [48, 32, 32, 32, 32, 32, 32, 48],
#         [48, 32, 32, 32, 32, 32, 32, 48],
#         [48, 32, 32, 32, 32, 32, 32, 48],
#         [64, 48, 48, 48, 48, 48, 48, 64],
#     ], dtype=int),
#     5: np.array([
#         [0, 0, 0, 0, 0, 0, 0, 0],
#         [30, 20, 20, 20, 20, 20, 20, 30],
#         [27, 18, 18, 18, 18, 18, 18, 27],
#         [24, 16, 16, 16, 16, 16, 16, 24],
#         [21, 14, 14, 14, 14, 14, 14, 21],
#         [18, 12, 12, 12, 12, 12, 12, 18],
#         [15, 10, 10, 10, 10, 10, 10, 15],
#         [0, 0, 0, 0, 0, 0, 0, 0],
#     ], dtype=int),
# }
#
# """ 1. yöntem iç içe np.where """
# # 1 kat
# arr = np.array([
#                 [2, 3, 3, 3, 3, 3, 3, 3],
#                 [1, 1, 1, 1, 1, 1, 1, 1],
#                 [1, 1, 1, 1, 1, 1, 1, 1],
#                 [3, 3, 3, 3, 3, 3, 3, 3],
#                 [3, 3, 3, 3, 3, 3, 3, 3],
#                 [5, 5, 5, 5, 5, 5, 5, 5],
#                 [5, 5, 5, 5, 5, 5, 5, 5],
#                 [3, 3, 3, 3, 3, 3, 3, 4],
#             ], dtype=int)
# current_time = time.time()
# for i in range(1000):
#     score_arr = np.where( arr == 1, SCORE_DICT[1], np.where(
#         arr == 5, SCORE_DICT[5], np.where(
#             arr == 2, SCORE_DICT[2], np.where(
#                 arr == 4, SCORE_DICT[4], 0
#             )
#         )
#     ))
# print(f"1. işlem süresi: {time.time() - current_time}")
# print(f"score table:\n{score_arr}\ntotal score: {score_arr.sum()}")
#
#
# """ 2. Yöntem gpt """
# # 2 kat
# current_time = time.time()
# for i in range(1000):
#     score_arr = np.zeros_like(arr, dtype=int)
#     for key, score_matrix in SCORE_DICT.items():
#         score_arr += np.where(arr == key, score_matrix, 0)
#
# print(f"2. işlem süresi: {time.time() - current_time}")
# print(f"score table:\n{score_arr}\ntotal score: {score_arr.sum()}")
#
# """ 3. yöntem iç içe döngü + sözlük """
# # 5.5 kat
# current_time = time.time()
# for i in range(1000):
#     score_arr = np.zeros_like(arr, dtype=int)
#     for y in range(8):
#         for x in range(8):
#             score_arr[y][x] = SCORE_DICT[arr[y][x]][y][x]
# print(f"3. işlem süresi: {time.time() - current_time}")
# print(f"score table:\n{score_arr}\ntotal score: {score_arr.sum()}")