import re
import DiceClasses


def dice_get_rand(dice_string):

    op_string = list(filter(None, re.split(r'[d0-9]', dice_string)))
#    print(op_string)
    num_list = re.split(r'[a-z+*/\-]', dice_string)
#    print(num_list)
    dice_class = DiceClasses.DiceGroup(num_list, op_string, [])
#    print(dice_class.get_low())
#    print(dice_class.get_avg())
#    print(dice_class.get_rand())
#    print(dice_class.get_high())
    return dice_class.get_rand()


def dice_roller(in_str):
    if in_str is None:
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
            return dice_get_rand(dice)
    else:
        return "Invalid Syntax"


def stat_definer(stat):
    if stat < 10:
        distance = stat - 11
        stat_bonus = int(distance / 2)
        return f"{stat_bonus}"
    if stat >= 10:
        distance = stat - 10
        stat_bonus = int(distance / 2)
        return f"+{stat_bonus}"
