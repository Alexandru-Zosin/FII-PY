# 1. Write a function to return a list of the first n numbers in the Fibonacci string.
def problem_1(num):
    if num == 1:
        return [0]
    if num == 2:
        return [0, 1]

    fibo_list = [0, 1]
    prev = 0
    curr = 1
    for i in range(2, num):
        new_value = prev + curr
        fibo_list.append(new_value)
        prev = curr
        curr = new_value
    
    return fibo_list

# 2. Write a function that receives a list of numbers and returns a list of the prime numbers found in it.
def is_prime(n):
    if n == 0 or n == 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, n // 2, 2):
        if n % i == 0:
            return False

    return True

def problem_2(num_list):
    return list(filter(lambda e: is_prime(e), num_list))

# 3. Write a function that receives as parameters two lists a and b and returns:
#  (a intersected with b, a reunited with b, a - b, b - a)
def problem_3(list_a, list_b):
    list_a = set(list_a)
    list_b = set(list_b)
    return (list_a & list_b, list_a | list_b, list_a - list_b, list_b - list_a)

# 4. Write a function that receives as a parameters a list of musical notes (strings), 
# a list of moves (integers) and a start position (integer).
#  The function will return the song composed by going though the musical notes beginning with the start 
# position and following the moves given as parameter.
# Example : compose(["do", "re", "mi", "fa", "sol"], [1, -3, 4, 2], 2) 
# will return ["mi", "fa", "do", "sol", "re"] 
def problem_4(musical_notes, moves, start_pos):
    song = [musical_notes[start_pos]]
    pos = start_pos
    for move in moves:
        pos = (pos + move) % len(musical_notes)
        song.append(musical_notes[pos])
    
    return song

# 5. Write a function that receives as parameter a matrix and will return the matrix obtained 
# by replacing all the elements under the main diagonal with 0 (zero).
def problem_5(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i > j:
                matrix[i][j] = 0
                
    return matrix

# 6. Write a function that receives as a parameter a variable number of lists and a whole number x.
# Return a list containing the items that appear exactly x times in the incoming lists.

def problem_6(x, *lists):
    appearances = dict()

    for my_list in lists:
        for i in my_list:
            if appearances.get(i) == None:
                appearances[i] = 1
            else:
                appearances[i] += 1
    
    returned_list = list()
    for k, v in appearances.items():
        if v == x:
            returned_list.append(k)

    return returned_list

# 7. Write a function that receives as parameter a list of numbers (integers)
#   and will return a tuple with 2 elements.
#   The first element of the tuple will be the number of palindrome numbers found in the list 
#   and the second element will be the greatest palindrome number.
def is_palindrome(num): #Lab-1
    str_num = str(num)

    for i in range(0, len(str_num) // 2):
        if str_num[i] != str_num[-i - 1]:
            return False
    
    return True

def problem_7(num_list):
    max_palindrome = 0
    count = 0
    for i in num_list:
        if is_palindrome(i):
            count += 1
            if i > max_palindrome:
                max_palindrome = i
    
    return(count, max_palindrome)

# 8. Write a function that receives a number x, default value equal to 1, a list of strings, 
# and a boolean flag set to True. For each string, generate a list containing the characters 
# that have the ASCII code divisible by x if the flag is set to True,
#  otherwise it should contain characters that have the ASCII code not divisible by x.
def problem_8(x = 1, strings_list = [], flag = True):
    result = []
    
    for s in strings_list:
        if flag:
            chars = [c for c in s if ord(c) % x == 0]
        else:
            chars = [c for c in s if ord(c) % x != 0]
        
        result.append(chars)
    
    return result

# 9. Write a function that receives as parameter a matrix which represents the heights of the spectators 
# in a stadium and will return a list of tuples (line, column) each one representing a seat of a
#  spectator which can't see the game.
#  A spectator can't see the game if there is at least one taller spectator standing in front of him. 
# All the seats are occupied. All the seats are at the same level. 
# Row and column indexing starts from 0, beginning with the closest row from the field.
# Example:
# FIELD
# [[1, 2, 3, 2, 1, 1],
#  [2, 4, 4, 3, 7, 2],
#  [5, 5, 2, 5, 6, 4],
#  [6, 6, 7, 6, 7, 5]] 
# Will return : [(2, 2), (3, 4), (2, 4)] 

def problem_9(matrix):
    return_list = list()
    n = len(matrix)
    m = len(matrix[0])

    for j in range(0, m):
        maxHeight = matrix[0][j]
        
        for i in range(1, n):
            if matrix[i][j] <= maxHeight:
                return_list.append((i, j))
            else:
                maxHeight = matrix[i][j]

    return return_list

# 10. Write a function that receives a variable number of lists and returns a list of tuples as follows: 
# the first tuple contains the first items in the lists, the second element contains the items
# on the position 2 in the lists, etc. 
# Example: for lists [1,2,3], [5,6,7], ["a", "b", "c"] return: [(1, 5, "a ") ,(2, 6, "b"), (3,7, "c")]. 
# Note: If input lists do not have the same number of items, 
# missing items will be replaced with None to be able to generate max ([len(x) for x in input_lists])
# tuples.

def problem_10(*lists):
    result = []
    max_length = max([len(l) for l in lists])

    for i in range(max_length):
        current_tuple = []

        for l in lists:
            if i < len(l):
                current_tuple.append(l[i])
            else:
                current_tuple.append(None)
        
        result.append(tuple(current_tuple))

    return result

# 11. Write a function that will order a list of string tuples based on the 3rd character
# of the 2nd element in the tuple. 
# Example: ('abc', 'bcd'), ('abc', 'zza')] ==> [('abc', 'zza'), ('abc', 'bcd')]

def problem_11(tuples):
    return sorted(tuples, key = lambda element: element[1][2])

# 12. Write a function that will receive a list of words as parameter and will return 
# a list of lists of words, grouped by rhyme. 
# Two words rhyme if both of them end with the same 2 letters.
# Example:
# group_by_rhyme(['ana', 'banana', 'carte', 'arme', 'parte']) will return
#  [['ana', 'banana'], ['carte', 'parte'], ['arme']] 

def problem_12(words_list):
    rhymes = dict()

    for word in words_list:
        last_2_letters = word[-2:]

        if rhymes.get(last_2_letters) == None:
            rhymes[last_2_letters] = [word]
        else:
            rhymes[last_2_letters].append(word)

    return [w for (k, w) in rhymes.items()]

if __name__ == "__main__":
    print("1.", problem_1(10))
    print("2.", problem_2([1, 2, 7, 43, 9, 13, 43, 0, 1, 4, 6, 21, 45]))
    print("3.", problem_3([2, 4, 43, 1, 123, 11], [2, 4, 43, 55, 10]))
    print("4.", problem_4(["do", "re", "mi", "fa", "sol"], [1, -3, 4, 2], 2))
    sm = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    print("5.", problem_5(sm))
    print("6.", problem_6(2, [1, 2, 3], [2, 3, 4], [4, 5, 6], [4, 1, "test"]))
    print("7.", problem_7([123, 123, 1221, 22, 332121233]))
    m = [[1, 2, 3, 2, 1, 1],
     [2, 4, 4, 3, 7, 2],
     [5, 5, 2, 5, 6, 4],
     [6, 6, 7, 6, 7, 5]]
    print("8.", problem_8(2, ["test", "hello", "lab002"], False))
    print("9.", problem_9(m))
    print("10.", problem_10([1,2,3], [5,6,7], ["a", "b", None]))
    print("11.", problem_11([("abc", "bcd"), ("abc", "zza")]))
    print("12.", problem_12(["ana", "banana", "carte", "arme", "parte"]))