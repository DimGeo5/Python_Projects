from morse_code import morse_dictionary as morse                # Using a support file that contains 2 dictionaries
from morse_code import reverse_morse_dictionary as reverse      # Characters to morse and morse to characters


def coding(text):           # A function that takes the input text as an argument
    coded_text = []
    try:                    # using try in case of no valid characters (keys to dictionaries)
        for letter in text:
            coded_letter = morse[letter]
            coded_text.append(coded_letter)
        print(' '.join(coded_text))
        print("")
    except KeyError:
        print("Invalid letter. Please use only letters from the English Alphabet\n")
        text = input("Type your message:\n").lower()
        coding(text)


def decoding(text):      # A function that takes the coded message and transform into English
    try:                 # # using try in case of no valid characters (keys to dictionaries)
        coded_words = text.split("   ")
        coded_letters_per_word = [coded_word.split() for coded_word in coded_words]
        decoded_words = [''.join(reverse[letter] for letter in coded_word) for coded_word in coded_letters_per_word]
        print(' '.join(decoded_words))
        print("")
    except KeyError:
        print("The code you input is invalid. Check your code and try again!\n")
        text = input("Type your coded message:\n")
        decoding(text)


while True:     # using a while true in order to give the user the chance to use the program again or if invalid key is pressed
    choice = input("Press 'c' for coding a message, 'd' for decoding a message, or 'e' to exit:\n").lower()
    if choice == "c":
        message = input("Type your message:\n").lower()
        coding(message)

    elif choice == "d":
        message = input("Type your coded message:\n")
        decoding(message)

    elif choice == "e":
        print("Thank you for using the program, goodbye!")
        break

    else:
        print("Wrong Choice!\nTry Again!\n")
