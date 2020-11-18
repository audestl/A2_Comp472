import random

with open("input3puzzles.txt", mode='w+', newline='') as output_file:
    for i in range(0, 3):
        # Generate 'n' unique random numbers within a range
        randomList = random.sample(range(0, 10), 10)
        str1 = ""
        for number in randomList:
            str1 += str(number) + " "
        output_file.write(str1 + "\n")