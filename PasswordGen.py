import random as rd
import string

if __name__ == '__main__':
    print("\nPassword Requirements:")
    # Get data from user
    p_length = int(input("\nPassword Length: #? "))
    b_upper = input("\nInclude Uppercase: Y/N ")
    b_lower = input("\nInclude Lowercase: Y/N ")
    b_numb = input("\nInclude Numbers: Y/N ")
    b_spec = input("\nInclude Special Characters: Y/N ")

    if b_upper != 'Y' and b_lower != 'Y' and b_numb != 'Y' and b_spec != 'Y':
        print("\nPassword cannot be configured with no values.")
        exit(10)

    # Define fields for password
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    special = string.punctuation

    p_fields = ""

    # Select allowed data fields
    if b_upper == 'Y':
        p_fields += upper
    if b_lower == 'Y':
        p_fields += lower
    if b_numb == 'Y':
        p_fields += num
    if b_spec == 'Y':
        p_fields += special

    password = "".join([rd.choice(p_fields) for n in range(p_length)])
    print("\nHere is your specified password: \n")
    print(password)
