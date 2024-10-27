# 1. Write a function that receives as parameters two lists a and b and returns a list of sets containing: 
# (a intersected with b, a reunited with b, a - b, b - a)

def problem_1(a, b):
    a = set(a)
    b = set(b)
    return [a & b, a | b, a - b, b - a]

# 2. Write a function that receives a string as a parameter and returns a dictionary in which 
# the keys are the characters in the character string and the values
#  are the number of occurrences of that character in the given text.

def problem_2(my_string):
    my_dictionary = dict()

    for ch in my_string:
        if my_dictionary.get(ch) == None:
            my_dictionary[ch] = my_string.count(ch)
    
    return my_dictionary

# 4. The build_xml_element function receives the following parameters:
# tag, content, and key-value elements given as name-parameters. 
# Build and return a string that represents the corresponding XML element. 
# Example: build_xml_element ("a", "Hello there", href =" http://python.org ", 
# _class =" my-link ", id= " someid ") 
# returns  the string = "<a href=\"http://python.org \ "_class = \" my-link \ "id = \" someid \ ">
#  Hello there </a>"

def problem_4(tag, content, **elements):
    to_return = "<" + tag
    for k, v in elements.items(): # (str, str)
        to_return += " " + k + " = \\\"" + v + '\\"'

    to_return += "> " + content + " </" + tag + ">"
    return to_return

# 6. Write a function that receives as a parameter a list and returns a tuple (a, b),
#  representing the number of unique elements in the list, 
# and b representing the number of duplicate elements in the list (use sets to achieve this objective).

def problem_6(num_list):
    unique_apps_list = set(num_list)
    count = 0
    for num in unique_apps_list:
        if num_list.count(num) > 1:
            count += 1

    return(len(unique_apps_list), count)

# 7. Write a function that receives a variable number of sets and returns 
# a dictionary with the following operations from all sets two by two:
#  reunion, intersection, a-b, b-a. 
# The key will have the following form: "a op b", where a and b are two sets,
#  and op is the applied operator: |, &, -. 
# Ex: {1,2}, {2, 3} =>
# {
#     "{1, 2} | {2, 3}":  {1, 2, 3},
#     "{1, 2} & {2, 3}":  { 2 },
#     "{1, 2} - {2, 3}":  { 1 },
#     ...
# }

def problem_7(*sets):
    my_dict = dict()

    for i in range(0, len(sets)):
        for j in range(i + 1, len(sets)):
            my_dict[str(sets[i]) + " | " + str(sets[j])] = sets[i] | sets[j]
            my_dict[str(sets[i]) + " & " + str(sets[j])] = sets[i] & sets[j]
            my_dict[str(sets[i]) + " - " + str(sets[j])] = sets[i] - sets[j]
            my_dict[str(sets[j]) + " - " + str(sets[i])] = sets[j] - sets[i]

    return my_dict

# 8. Write a function that receives a single dict parameter named mapping. 
# This dictionary always contains a string key "start". 
# Starting with the value of this key you must obtain a list of objects by 
# iterating over mapping in the following way: 
# the value of the current key is the key for the next value, until you find a loop 
# (a key that was visited before). 
# The function must return the list of objects obtained as previously described.
# Ex: loop({'start': 'a', 'b': 'a', 'a': '6', '6': 'z', 'x': '2', 'z': '2', '2': '2', 'y': 'start'})
#  will return ['a', '6', 'z', '2']

def problem_8(mapping):
    return_list = list()
    current_key = mapping["start"]
    
    while current_key != "start":
        return_list.append(current_key)
        current_key = mapping[current_key]
        if current_key in return_list:
            break
    
    return return_list

# 9. Write a function that receives a variable number of positional arguments and a variable number
#  of keyword arguments adn will return the number of positional arguments whose values can be 
# found among keyword arguments values.
# Ex: my_function(1, 2, 3, 4, x=1, y=2, z=3, w=5) will return 3

def problem_9(*positional_args, **keyword_args):
    keyword_values = [v for (k, v) in keyword_args.items()]
    return len([i for i in positional_args if i in keyword_values])

# 3 si 5 not done
if __name__ == "__main__":
    print("1. ", problem_1([1, 2, 3, 4, 5], [3, 4, 5, 6, 7, 8]))
    print("2. ", problem_2("Ana has apples."))
    print("4. ", problem_4("a", "Hello there", href="http://python.org ", _class=" my-link ",
                        id=" someid "))
    print("6. ", problem_6([1, 2, 2, 5, 43, 12]))
    print("7. ", problem_7({1, 2}, {2, 3}))
    print("8. ", problem_8({
            "start": "a",
            "b": "a",
            "a": "6",
            "6": "z",
            "x": "2",
            "z": "2",
            "2": "2",
            "y": "start",
        }))
    print("9. ", problem_9(1, 2, 3, 4, x = 1, y = 2, z = 3, w = 5)) 



