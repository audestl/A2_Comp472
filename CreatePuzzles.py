import random

with open("input50puzzles.txt", mode='w+', newline='') as output_file:
    for i in range(0, 50):
        # Generate 'n' unique random numbers within a range
        randomList = random.sample(range(0, 8), 8)
        str1 = ""
        for number in randomList:
            str1 += str(number) + " "
        output_file.write(str1 + "\n")