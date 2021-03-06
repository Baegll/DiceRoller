import random

# global variables for function calculations
from math import ceil

finished_rolls = []
rolls = []
index_list = [0]  # index list, for operation order
d_index = []  # separate dice rolls         'd'
s_index = []  # whitespace                  ' ,|'
o_index = []  # basic math operations       '+,-,/,*'
b_index = []  # lose lowest/keep highest    'l,k'
rb_index = []  # keep lowest/lose highest   'o,i'
e_index = []  # explode/re-roll             'e,r'


def dice_parser(in_string):
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

    # test for simple invalid input
    if in_string[0] in ('d', '|', ' ', '+', '-', '/', '*', 'l', 'k', 'o', 'i', 'e', 'r'):
        print("invalid input")
        exit(1)

    # parse the string
    current_index = 0
    for i in range(0, len(in_string)):
        # each time we come across a key, mark its location in the proper index[]
        if in_string[i] == 'd':  # separate dice rolls
            index_list.append(current_index)
            d_index.append(current_index)
            if _state == 1:
                _state = 2
            else:
                print("Error_State: " + str(_state))
                print("Index: " + in_string[i])
                exit(3)

        elif in_string[i] in (' ', '|'):  # whitespace
            index_list.append(current_index)
            s_index.append(current_index)
            if _state in (3, 10, 9):
                _state = 4
            else:
                print("Error_State: " + str(_state))
                print("Index: " + in_string[i])
                exit(3)

        elif in_string[i] in ('+', '-', '/', '*'):  # basic math operations
            index_list.append(current_index)
            o_index.append(current_index)
            if _state in (3, 9):
                _state = 5
            else:
                print("Error_State: " + str(_state))
                print("Index: " + in_string[i])
                exit(3)

        elif in_string[i] in ('l', 'k'):  # lose lowest/keep highest
            index_list.append(current_index)
            b_index.append(current_index)
            if _state == 3:
                _state = 7
            else:
                print("Error_State: " + str(_state))
                print("Index: " + in_string[i])
                exit(3)

        elif in_string[i] in ('o', 'i'):  # keep lowest/lose highest
            index_list.append(current_index)
            rb_index.append(current_index)
            if _state == 3:
                _state = 8
            else:
                print("Error_State: " + str(_state))
                print("Index: " + in_string[i])
                exit(3)

        elif in_string[i] in ('e', 'r'):  # explode/re-roll
            index_list.append(current_index)
            e_index.append(current_index)
            if _state == 3:
                _state = 6
            else:
                print("Error_State: " + str(_state))
                print("Index: " + in_string[i])
                exit(3)

        elif in_string[i].isdigit():
            if _state in (0, 4):  # start of a die
                _state = 1  # requires [d] tag next
            elif _state == 2:  # finish of die
                _state = 3  # Die is "finished" Requires whitespace or END
            elif _state in (6, 7, 8):  # Explode/Re-roll, Lose/Keep, RLose/RKeep
                _state = 9  # Number for operation
            elif _state == 5:  # Math operation
                _state = 10  # Finish of math operation
            elif _state in (1, 3, 9, 10):  # continue to count the number
                _state = _state
            else:
                print("Error_State: ISDIGIT, " + str(_state))
                exit(3)

        else:
            print("invalid symbol: " + in_string[i])
            exit(2)

        current_index += 1




def roller(in_string):
    z = -1  # set index counter to "0" since i increase z at beginning of loop
    for x in index_list:
        z += 1  # increase index counter
        if x in d_index:
            prev_element = int(index_list[z - 1])
            dice_num = int(in_string[index_list[z - 1]:x])
            dice_size = int(in_string[x + 1:(index_list[z + 1])])

            for y in range(0, dice_num):
                roll = random.randint(1, dice_size)
                rolls.append(roll)

        if x in s_index:
            # add individual rolls, store as number in finished_rolls
            finished_rolls.append(add_rolls())
            # clear rolls[]
            rolls.clear()
            # let program continue

        if x in o_index:
            if in_string[x] == '+':
                rolls.append(int(in_string[x + 1:(index_list[z + 1])]))  # append positive number according to proper index to rolls list for final sum
            if in_string[x] == '-':
                neg = 0 - int(in_string[x + 1:(index_list[z + 1])])
                rolls.append(neg)  # append negative number according to proper index to rolls list for final sum
            if in_string[x] == '*':  # add previous roll(s), multiply by next index
                prev_roll = add_rolls()
                multiplicative = int(in_string[x + 1:(index_list[z + 1])])  # Create multiplier from proper index
                # TODO: remove previous roll from rolls[], replace with new_num, the prev roll multiplied
                new_num = (prev_roll * multiplicative)
                rolls.append(new_num)  # Multiply previous rolls and add back to roll list
            if in_string[x] == '/':
                prev_roll = add_rolls()
                divisor = int(in_string[x + 1:(index_list[z + 1])])  # Create divisor from proper index
                # TODO: remove previous roll from rolls[], replace with new_num, the prev roll divided
                new_num = ceil(prev_roll / divisor)
                rolls.append(new_num)  # Divide previous rolls and add back to roll list

        if x in b_index:
            if in_string[x] == 'l':
                lose_these_dice = int(in_string[x + 1:(index_list[z + 1])])   # This is the number of dice to lose
                # Sort rolls[] highest->lowest: pop values until rolls[]size == original_size - lose_these_dice
                rolls.sort(reverse=True)
                # print(rolls)        # DEBUG STATEMENT
                for y in range(0, lose_these_dice):
                    rolls.pop()
                # print(rolls)        # DEBUG STATEMENT
            if in_string[x] == 'k':
                keep_these_dice = int(in_string[x + 1:(index_list[z + 1])])     # This is the number of dice to keep
                # Sort rolls[] highest->lowest: pop values until rolls[]size == keep_these_dice
                rolls.sort(reverse=True)
                # print(rolls)        # DEBUG STATEMENT
                while len(rolls) != keep_these_dice:
                    rolls.pop()
                # print(rolls)        # DEBUG STATEMENT

        if x in rb_index:
            if in_string[x] == 'o':
                keep_these_dice = int(in_string[x + 1:(index_list[z + 1])])  # This is the number of dice to keep
                # Sort rolls[] highest->lowest: pop values until rolls[]size == original_size - lose_these_dice
                rolls.sort()
                # print(rolls)  # DEBUG STATEMENT
                for y in range(0, keep_these_dice):
                    rolls.pop()
                # print(rolls)  # DEBUG STATEMENT
            if in_string[x] == 'i':
                lose_these_dice = int(in_string[x + 1:(index_list[z + 1])])  # This is the number of dice to lose
                # Sort rolls[] highest->lowest: pop values until rolls[]size == keep_these_dice
                rolls.sort()
                # print(rolls)  # DEBUG STATEMENT
                while len(rolls) != lose_these_dice:
                    rolls.pop()
                # print(rolls)  # DEBUG STATEMENT

        if x in e_index:
            if x == 'r':
                re_roll_on = int(in_string[x + 1:(index_list[z + 1])])
                dice_size = int(in_string[x + 1:(index_list[z+1])])

                i = 0
                for roll_value in rolls:
                    if re_roll_on == roll_value:
                        re_roll_value = random.randint(1, dice_size)    # TODO: Modular Rerroll, based on user input
                        rolls[i] = re_roll_value
                    i += 1

            # if re-roll, do above, else its exploding dice, so do below
            explode_rolls = []
            explode_on = int(in_string[x + 1:(index_list[z + 1])])      # I.E. Dice Size

            # Test rolls[] for every value that == explode_on, make a new roll in explode_rolls
            for roll_value in rolls:
                if explode_on == roll_value:
                    roll = random.randint(1, explode_on)        # TODO: Modular explode_on, based on user input
                    explode_rolls.append(roll)
                    # roll and append to explode_rolls

            # If no exploding dice, the below While loop does not execute
            # pop values from explode_rolls and test if they explode, append each popped value to rolls[]
            while len(explode_rolls) > 0:
                roll_value = explode_rolls.pop()
                if explode_on == roll_value:
                    roll = random.randint(1, explode_on)
                    explode_rolls.append(roll)
                rolls.append(roll_value)

    # once done with operations, add it to finished roll list
    finished_rolls.append(add_rolls())


def add_rolls():
    total = 0
    for x in rolls:
        total += x
    return total


def print_dice():
    print_string = ""
    for x in finished_rolls:
        print_string += str(x) + "\t"
    print(print_string)


if __name__ == '__main__':
    in_str = input()
    dice_parser(in_str)
    index_list.append(len(in_str))
    roller(in_str)

    # print index lists
    print_dice()
    """print(index_list)
    print(d_index)
    print(s_index)
    print(o_index)
    print(b_index)
    print(rb_index)
    print(e_index)"""
