# -*- coding: utf-8 -*-
from diplomas.geocaching.utils import get_caches_by_type, get_cache_to_number_table, get_numbers_to_cache_mapping, \
    remove_number


def get_geoloto_cards():
    cards = [['6', '11', '20', '28', '32', '34', '45', '47', '51', '53', '63', '70', '77', '86', '89'],
             ['2', '9', '12', '17', '21', '24', '38', '43', '46', '59', '60', '65', '73', '81', '87'],
             ['3', '14', '16', '25', '37', '39', '41', '50', '57', '61', '62', '74', '78', '85', '90'],
             ['1', '5', '19', '23', '33', '36', '48', '52', '54', '66', '67', '71', '72', '80', '88'],
             ['8', '15', '18', '22', '26', '35', '40', '49', '55', '58', '64', '69', '76', '82', '89'],
             ['4', '7', '10', '13', '27', '29', '30', '31', '42', '44', '56', '68', '75', '79', '83'],
             ['7', '9', '15', '18', '21', '26', '33', '45', '47', '59', '62', '64', '78', '84', '89'],
             ['5', '19', '22', '28', '30', '37', '44', '46', '54', '58', '69', '71', '75', '82', '90'],
             ['6', '8', '10', '17', '24', '32', '35', '43', '52', '55', '61', '68', '70', '83', '86'],
             ['4', '11', '16', '29', '38', '40', '42', '53', '57', '65', '67', '73', '74', '80', '87'],
             ['2', '13', '14', '20', '27', '31', '39', '48', '51', '56', '60', '77', '79', '85', '88'],
             ['1', '3', '12', '23', '25', '34', '36', '41', '49', '50', '63', '66', '72', '76', '81'],
             ['7', '15', '19', '20', '22', '36', '38', '47', '50', '54', '69', '76', '78', '84', '90'],
             ['2', '13', '16', '29', '32', '35', '43', '49', '51', '57', '60', '66', '79', '83', '86'],
             ['1', '9', '14', '25', '27', '33', '44', '46', '59', '62', '67', '71', '77', '80', '87'],
             ['4', '8', '10', '12', '21', '26', '39', '41', '45', '53', '61', '73', '75', '81', '88'],
             ['5', '17', '24', '31', '37', '40', '42', '55', '58', '63', '68', '70', '74', '82', '89'],
             ['3', '6', '11', '18', '23', '28', '30', '34', '48', '52', '56', '64', '65', '72', '85'],
             ['4', '10', '18', '21', '26', '32', '34', '40', '45', '51', '57', '69', '72', '80', '89'],
             ['6', '8', '14', '28', '20', '39', '41', '46', '55', '62', '65', '70', '79', '82', '90'],
             ['1', '16', '19', '24', '33', '38', '48', '50', '54', '61', '66', '73', '75', '81', '84'],
             ['7', '9', '11', '23', '31', '36', '44', '47', '59', '60', '63', '71', '74', '83', '85'],
             ['2', '5', '13', '17', '25', '29', '35', '37', '43', '52', '56', '64', '68', '78', '86'],
             ['3', '12', '15', '22', '27', '30', '42', '49', '53', '58', '67', '76', '77', '87', '88']]
    return cards


def check_geoloto_dp(caches_list, numbers_card):
    dic = {}
    cache_to_number_table = {}
    for cache_type in ['TR', 'VI', 'MS', 'MV']:
        caches_to_process = get_caches_by_type(caches_list, cache_type)
        cache_to_number_table = get_cache_to_number_table(numbers_card, caches_to_process)
        get_cache_to_number_table_with_simple_ones_heuristic(cache_type, cache_to_number_table, dic)
        get_cache_to_number_table_with_simple_singleton_two(cache_type, cache_to_number_table, dic)
        get_cache_to_number_table_with_two_equal_pairs(cache_type, cache_to_number_table, dic)
    return dic, cache_to_number_table


def get_cache_to_number_table_with_simple_singleton_two(cache_type, cache_to_number_table, resulted_dict):
    # Check if there is only one cache in table an it could be paired
    # with two numbers -> then select first number and pair
    # Works with {'11538': ['11', '53']} as well as  with
    # {'6576': ['57', '65'], '11538': ['11', '53']}

    restart_needed = True
    while restart_needed and cache_to_number_table:
        map_numbers_to_cache = get_numbers_to_cache_mapping(cache_to_number_table)
        restart_needed = False
        for number in sorted(map_numbers_to_cache):
            if len(map_numbers_to_cache[number]) == 1:
                cache = map_numbers_to_cache[number][0]
                if number not in resulted_dict:
                    resulted_dict[number] = {}
                resulted_dict[number][cache_type] = cache

                del cache_to_number_table[cache]
                restart_needed = True
                break
    return resulted_dict


def get_cache_to_number_table_with_two_equal_pairs(cache_type, cache_to_number_table, resulted_dict):
    # {'1212': ['1', '2'], '2121': ['1', '2']}

    restart_needed = True
    while restart_needed and cache_to_number_table:
        map_numbers_to_cache = get_numbers_to_cache_mapping(cache_to_number_table)
        restart_needed = False
        for number in sorted(map_numbers_to_cache):
            if len(map_numbers_to_cache[number]) == 2:
                map_numbers_to_cache[number] = sorted(map_numbers_to_cache[number])
                cache_a = map_numbers_to_cache[number][0]
                cache_b = map_numbers_to_cache[number][1]
                caches_numbers = set(cache_to_number_table[cache_a] + cache_to_number_table[cache_b])
                if len(caches_numbers) == 2:
                    caches_numbers.remove(number)
                    number_b = list(caches_numbers)[0]

                    if number not in resulted_dict:
                        resulted_dict[number] = {}
                    if number_b not in resulted_dict:
                        resulted_dict[number_b] = {}
                    resulted_dict[number][cache_type] = cache_a
                    resulted_dict[number_b][cache_type] = cache_b

                    del cache_to_number_table[cache_a]
                    del cache_to_number_table[cache_b]
                    restart_needed = True
                    break
    return resulted_dict


def get_cache_to_number_table_with_simple_ones_heuristic(cache_type, cache_to_number_table, resulted_dict):
    restart_needed = True
    while restart_needed:
        restart_needed = False
        for cache in cache_to_number_table:
            if len(cache_to_number_table[cache]) == 1:
                number = cache_to_number_table[cache][0]
                if number not in resulted_dict:
                    resulted_dict[number] = {}
                resulted_dict[number][cache_type] = cache

                cache_to_number_table = remove_number(cache_to_number_table, number)
                restart_needed = True
                break
    return resulted_dict