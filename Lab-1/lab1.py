# 1. Find The greatest common divisor of multiple numbers read from the console.
def find_gcd(a, b): #https://infogenius.ro/algoritmul-lui-euclid/
    while a and b:
        if a > b:
            a %= b
        else:
            b %= a
    return a + b

def problem_1():
    count = int(input("How many numbers do you want to calculate GCD for?: "))
    if (count < 2):
        print("The GCD cannot be computed.")

    gcd = int(input("Enter number: "))
    for i in range (1, count):
        num = int(input("Enter number: "))
        gcd = find_gcd(gcd, num)

    return gcd

# 2. Write a script that calculates how many vowels are in a string.
def problem_2(input_str):
    count = 0
    for c in input_str:
        if c.lower() in ['a', 'e', 'i', 'o', 'u']:
            count += 1

    return count 

# 3. Write a script that receives two strings and prints the number of occurrences
# of the first string in the second.
def problem_3(input_str_1, input_str_2):
#    input_str_1 = input("Enter the first string: ")
    return(input_str_2.count(input_str_1))

# 4. Write a script that converts a string of characters written in
#  UpperCamelCase into lowercase_with_underscores.
def problem_4(input_str):
    output_str = ""
    for c in input_str:
        if c.isupper():
            if len(output_str) != 0:
                output_str += "_"
            output_str += c.lower()
        else:
            output_str += c
    return output_str

# 5. Write a function that validates if a number is a palindrome.
def problem_5(num):
    str_num = str(num)

    for i in range(0, len(str_num) // 2):
        if str_num[i] != str_num[-i - 1]:
            return False
    
    return True

# 6. Write a function that extract a number from a text 
# (for example if the text is "An apple is 123 USD", this function will return 123,
#  or if the text is "abc123abc" the function will extract 123). 
# The function will extract only the first number that is found.
def problem_6(text):
    found_num = ""
    found_digit = False
    for c in text:
        if c.isdigit():
            found_num += c
            found_digit = True
        elif found_digit == True:
            break
        else:
            continue
    return int(found_num)

# 7. Write a function that counts how many bits with value 1 a number has.
# For example for number 24, the binary format is 00011000, meaning 2 bits with value "1"
def problem_7(number):
    return bin(number).count('1')

# 8. Write a function that counts how many words exists in a text.
#  A text is considered to be form out of words that are separated by only ONE space. 
# For example: "I have Python exam" has 4 words.
def problem_8(text):
    split_text = text.split(" ")
    count = 0
    for entry in split_text:
        if entry != "":
            count += 1

    return count

if __name__ == "__main__":
    print("Problem 1 answer: ", problem_1()) # reading from console
    print("Problem 2 answer: ", problem_2("vowels in a string"))
    print("Problem 3 answer: ", problem_3("do", "dogodogodo"))
    print("Problem 4 answer: ", problem_4("UpperCamelCaseCasesDe"))
    print("Problem 5 answer: ", problem_5(12321))
    print("Problem 6 answer: ", problem_6("litere01025sialtecifre982374"))
    print("Problem 7 answer: ", problem_7(21))
    print("Problem 8 answer: ", problem_8("I have    Python  exam"))