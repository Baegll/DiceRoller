# Dice Class
import requests
import json
import os

math_op_list = ['+', '-', '*', '/']


class DiceGroup:
    def __init__(self, dice, command_list):
        self.dice = dice
        self.command_list = command_list

        num = int(self.dice[0])      # First value of dice list will always be the number
        size = int(self.dice[1])     # Second value of dice list will always be size

        low = [1 * num]
        rand = dice_rand(num, size)
        avg = dice_avg(num, size, command_list)
        print("avg: " + str(avg))
        high = [size * num]

        index = 1
        for command in self.command_list:
            if command in math_op_list:
                index = index + 1   # We use index, so increase value
                # print(math_op(low, int(self.dice[index]), command))


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
    if 'e' in op_list:
        avg_val = d_num * (d_size/2+1)
    else:
        avg_val = d_num * (d_size/2+.5)
    return [int(avg_val)]


'''
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

'''