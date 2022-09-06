# Dice Class
import requests
import json
import os

math_op_list = ['+', '-', '*', '/']
lose_op_list = ['l', 'k']
keep_op_list = ['o', 'i']


class DiceGroup:
    def __init__(self, dice, command_list, default):
        self.dice = dice
        self.command_list = command_list
        self.low = default
        self.avg = default
        self.rand = default
        self.high = default
        num = int(self.dice[0])      # First value of dice list will always be the number
        size = int(self.dice[1])     # Second value of dice list will always be size

        self.low = dice_low(num)
        self.avg = dice_avg(num, size, command_list)
        self.rand = dice_rand(num, size)
        self.high = dice_high(size, num)

        index = 1
        for command in self.command_list:
            if command in math_op_list:
                index = index + 1
                self.low.append(math_op(self.low, self.dice[index], command))
                self.avg.append(math_op(self.avg, self.dice[index], command))
                self.rand.append(math_op(self.rand, self.dice[index], command))
                self.high.append(math_op(self.high, self.dice[index], command))
            elif command in lose_op_list:
                index = index + 1
                self.low = lose_lowest(self.low, self.dice[index])
                self.avg = lose_lowest(self.avg, self.dice[index])
                self.rand = lose_lowest(self.rand, self.dice[index])
                self.high = lose_lowest(self.high, self.dice[index])
            elif command in keep_op_list:
                index = index + 1
                self.low = lose_highest(self.low, self.dice[index])
                self.avg = lose_highest(self.avg, self.dice[index])
                self.rand = lose_highest(self.rand, self.dice[index])
                self.high = lose_highest(self.high, self.dice[index])
            elif command == 'e':
                index = index + 1
                self.low = explode_dice(self.low, size, self.dice[index])
                self.avg = explode_dice(self.avg, size, self.dice[index])
                self.rand = explode_dice(self.rand, size, self.dice[index])
                self.high = explode_dice(self.high, size, self.dice[index])
            elif command == 'r':
                index = index + 1
                self.low = re_roll_dice(self.low, size, self.dice[index])
                self.avg = re_roll_dice(self.avg, size, self.dice[index])
                self.rand = re_roll_dice(self.rand, size, self.dice[index])
                self.high = re_roll_dice(self.high, size, self.dice[index])
        # Completed list of low, avg, random, and high values.

    def get_low(self):
        return self.low

    def get_avg(self):
        return self.avg

    def get_rand(self):
        return self.rand

    def get_high(self):
        return self.high


def dice_low(d_num):
    d_list = []
    for die in range(0, d_num):
        d_list.append(1)
    return d_list


def dice_avg(d_num, d_size, op_list):
    d_list = []
    for die in range(0, d_num):
        if 'e' in op_list:
            d_list.append(int((d_size/2+1)))
        else:
            d_list.append(int((d_size/2+.5)))
    return d_list


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
    # If response not good, use randint()

    data = response.json()
    # print(data)
    values = data['result']['random']['data']
    d_list = []
    for value in values:
        d_list.append(value)
    return d_list


def dice_high(d_size, d_num):
    d_list = []
    for die in range(0, d_num):
        d_list.append(d_size)
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


def math_op(d_list, op_num, op_type):
    if op_type == '+':
        return int(op_num)
    elif op_type == '-':
        return 0 - int(op_num)
    elif op_type == '*':
        tot = 0
        # Add all values in list
        for v in d_list:
            tot += v
        # get end total after multiplication
        mult = tot * op_num
        # get value that it end total-starting total
        mult = mult - tot
        return int(mult)
    elif op_type == '/':
        tot = 0
        # Add all values in list
        for v in d_list:
            tot += v
        # get total after divisor
        divisor = tot / op_num
        # return value that will make current list into the correct quotient
        '''
        tot-9
        divisor-3
        divisor = tot-divisor
        new_divisor = 6
        now make new_divisor negative
        '''
        divisor = 0 - (tot - divisor)
        return int(divisor)
    else:
        print("Error with math_op")

