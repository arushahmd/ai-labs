import re

match = "[wW]eek" # it can be a w or W here then the eek, means either week or Week both will be matched.

string = ("This is the day of week, I have been waiting for a Week. "
          "He is weaker than him. He joined gym a week earlier.")

result = re.search(match, string) # searches for the first occurance

results = re.findall(match, string) # searches all the matches

print("============Disjunction results ===========\n")

print("Result is : ", result.group()) # Result is :  week
print(f"Results are : {results} \n" ) # Results are :  ['week', 'Week']

print("==========Disjunction results End===========\n\n")

#=======================================================#
#                        Range                          #

"""
    Range can be used to specify characters in a range.
    The symbol "-" is used along with brackets []
    For Example,
          - instead of writing /[ABCDEFGHIJKLMNOPQRSTUVWXYZ]/ we 
            can simply use range and specify [A-Z], [a-z]
          - instead of specifying /[1234567890]/, use [0-9]
"""

test_string = "I am 24 years old. I am a software Engineer. There are 26 alphabets in English."

num_match = "[0-9]" # Find all numbers

num_in_string = re.findall(num_match, test_string)

print("============= Range results =============\n")

print(f"Numbers in string are : {num_in_string} \n")

print("=========== Range results End ===========\n\n")

#                      Range End                        #
#=======================================================#

#=======================================================#
#                        Caret                          #

"""
    Caret Symbol (^) is used to neglect some characters.
    For Example,
                - [^A-Z] skips all the upper case letters
                - [^0-9] skip all numbers
                - [a^b]  find pattern where there is no b after a.
"""

test_string = "I am 24 years old. I am a software Engineer. There are 26 alphabets in English."

caret_match = "[^A-Z]"
caret_match_no_num = "[^0-9]"

result = re.findall(caret_match, test_string)
result_no_num = re.findall(caret_match_no_num, test_string)

print("============= Caret results =============\n")

print(f"Caret Result Upper Case : {''.join(result)}")
print(f"Caret Result No Number : {''.join(result_no_num)}")

print("=========== Caret results End ===========\n\n")

#                      Caret End                        #
#=======================================================#
