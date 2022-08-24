import re


def dice_parser(dice_string):
    _state = 0
    # 0 = empty
    # 1 = number of dice
    # 2 = d
    # 3 = size of die
    # 4 = new die/Whitespace,|
    # 5 = Math operation
    # 6 = Explode/Re-roll
    # 7 = lose/keep
    # 8 = r_lose/r_keep
    # 9 = manipulation number for states 6,7,8
    # 10 = op_number for Math
    # 11 = END

    op_string = ''.join([i for i in dice_string if not i.isdigit()])
    print(op_string)


if __name__ == '__main__':
    in_str = input()

    dice_rolls = re.split(r'[,|]', in_str)
    regex = "(\\d+d{1}\\d+$)|(d{1}\\d+$)|(\\d+d{1}\\d+[kloier+\\-/\\*]\\d+$)|(d{1}\\d+[kloier+\\-/\\*]\\d+$)|(\\d+d{" \
            "1}\\d+(?:[kloier+\\-/\\*]{1}\\d+)+)|(d{1}\\d+(?:[kloier+\\-/\\*]{1}\\d+)+)"
    for dice in dice_rolls:
        if re.match(regex, dice):
            pass
        else:
            print("Invalid Format: " + dice)
            break

