def getRandomQuestion():
    import string
    import random
    number_of_strings = 1
    length_of_string = random.randrange(4,6)
    for x in range(number_of_strings):
        str = (''.join(random.choice(string.ascii_letters) for _ in range(length_of_string)))
        str = str.lower()
        print(str)
    return str

if __name__ == "__main__":
    print(getRandomQuestion())