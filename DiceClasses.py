# Dice Class
import requests
import json
import os

math_op_list = ['+', '-', '*', '/']
lose_op_list = ['l', 'k']
keep_op_list = ['o', 'i']


class DiceGroup:
    def __init__(self, dice, command_list):
        self.dice = dice
        self.command_list = command_list

        num = int(self.dice[0])      # First value of dice list will always be the number
        size = int(self.dice[1])     # Second value of dice list will always be size

        low = [1 * num]
        avg = dice_avg(num, size, command_list) # TODO: Fix to have list of average
        rand = dice_rand(num, size)
        print("avg: " + str(avg))
        high = [size * num]

        index = 1
        for command in self.command_list:
            if command in math_op_list:
                index = index + 1
                # math_op()
            elif command in lose_op_list:
                index = index + 1
                lose_lowest(low, index)
                lose_lowest(avg, index)
                lose_lowest(rand, index)
                lose_lowest(high, index)
            elif command in keep_op_list:
                index = index + 1
                lose_highest(low, index)
                lose_highest(avg, index)
                lose_highest(rand, index)
                lose_highest(high, index)
            elif command == 'e':
                index = index + 1
                explode_dice(low, size, index)
                explode_dice(low, size, index)
                explode_dice(low, size, index)
                explode_dice(low, size, index)
            elif command == 'r':
                index = index + 1
                re_roll_dice(low, size, index)
                re_roll_dice(avg, size, index)
                re_roll_dice(rand, size, index)
                re_roll_dice(high, size, index)


def dice_rand(d_num, d_size):
    rand_org_data = json.dumps({
        "jsonrpc": "2.0",
        "method": "generateIntegers",
        "params": {
            "apiKey": os.environ['RAND_ORG_API_KEY'],
            "n": d_num,
            "min": 1,
            "max": d_size,
            "replacement": True
        },
        'id': 1
    })

    headers = {'Content-type': 'application/json', 'Content-Length': '200', 'Accept': 'application/json'}

    response = requests.post(url='https://api.random.org/json-rpc/2/invoke',
                             data=rand_org_data,
                             headers=headers
                             )
    data = response.json()
    # print(data)
    values = data['result']['random']['data']
    return values


def dice_avg(d_num, d_size, op_list):
    d_list = []
    for die in range(0, d_num):
        if 'e' in op_list:
            d_list.append(int((d_size/2+1)))
        else:
            d_list.append(int((d_size/2+.5)))
    return d_list


def lose_lowest(d_list, op_num):
    for x in range(0, op_num):
        d_list.remove(min(d_list))
    return d_list


def lose_highest(d_list, op_num):
    for x in range(0, op_num):
        d_list.remove(max(d_list))
    return d_list


def explode_dice(d_list, d_size, op_num):
    n_dice = 0
    if op_num == 1:
        print("1 would explode indefinitely, using max die size..")
        op_num = d_size
    for die in d_list:
        if die >= op_num:
            n_dice = n_dice + 1
    if n_dice > 0:
        return d_list + explode_dice(dice_rand(n_dice, d_size), d_size, op_num)
    return d_list


def re_roll_dice(d_list, d_size, op_num):
    n_dice = 0
    for die in d_list:
        if die <= op_num:
            n_dice = n_dice + 1
            d_list.remove(die)
            return d_list + dice_rand(n_dice, d_size)


def math_op(value, op_num, op_type):
    if op_type == '+':
        return op_num
    elif op_type == '-':
        return 0 - op_num
    elif op_type == '*':    # TODO: Fix Multiply
        return 3 * op_num
    elif op_type == '/':    # TODO: Fix Division
        return int(3 / op_num)
    else:
        print("Error with math_op")

