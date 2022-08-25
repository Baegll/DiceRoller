import re
import DiceClasses


def dice_parser(dice_string):

    op_string = list(filter(None, re.split(r'[d0-9]', dice_string)))
#    print(op_string)
    num_list = re.split(r'[a-z+*/\-]', dice_string)
#    print(num_list)
    dice_class = DiceClasses.DiceGroup(num_list, op_string)


if __name__ == '__main__':
    in_str = input()

    dice_rolls = re.split(r'[,|]', in_str)
    regex = '(\\d+)?d(\\d+)([kloier]?[\\d+]([+\\-*/]\\d+)?)*'
    valid_format = True
    for dice in dice_rolls:
        if re.match(regex, dice):
            pass
        else:
            print("Invalid Format: " + dice)
            valid_format = False
            break

    if valid_format:
        for dice in dice_rolls:
            dice_parser(dice)
