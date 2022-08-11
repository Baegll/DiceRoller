import random as rd
import string

# Generates random garbage that *TECHNICALLY* will be a proper input to DiceRoller, of varying length

if __name__ == '__main__':
    print("\nGenerating Testers:")
    p_fields = "1234567890d |+-/*lkoier"

    # Generate Testers
    rand_length = 4
    i = 0
    print("\nHere is your random Garbage Testers: \n")
    while i < 50:
        password = "".join([rd.choice(p_fields) for n in range(rand_length)])
        print(password)
        i = i+1
        rand_length = rd.randint(4, 12)

