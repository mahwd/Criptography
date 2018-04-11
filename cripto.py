from itertools import *
import random
import math, os

ALPHABET = "ABC"

iterable_symbols=tuple(ALPHABET)

letters = list()

number_of_repeats = math.factorial(len(iterable_symbols))

number_of_iterables = len(iterable_symbols)

number_of_conditions = number_of_repeats/number_of_iterables


def shuffleAlphabet(_list):
    swap_list = list()
    for i in range(int(number_of_conditions)):
        for j, y in enumerate(_list):
            if (i+j) % number_of_conditions == 0 or j % number_of_conditions == number_of_conditions:
                line = (j, y)
                with open('alphabet.txt', 'a') as f:
                    if j == 0 and i == 0:
                        f.writelines(ALPHABET+'\n')
                    f.writelines(str(line) + "\n")
                    f.close()

def createAlphabet():
    print("alphabet recreating")
    for m in permutations(iterable_symbols):
        letters.append(m)
    shuffleAlphabet(letters)

def printAlphabet(alpha):
    for index, alpha in enumerate(alpha):
        print(index, alpha)
        if index % number_of_conditions == 0:
            print("=================")


class encoder():

    def __init__(self):
        self.alphabet = list()
        self.alpabet_interruption = False
        try:
            with open("alphabet.txt", 'r') as f:
                content = f.readlines()
                if content[0].strip() != ALPHABET:
                    os.remove("alphabet.txt")
                    createAlphabet()
                    self.__init__()
                else:
                    if not content[1]:
                        print("not content")
                        createAlphabet()
                        self.__init__()
                    else:
                        content = [x.strip() for x in content]                #  her setrin sonundan '\n'- i silir
            for index, el in enumerate(content):
                if index != 0:
                    self.alphabet.append(eval(el))
        except:
            print("no file")
            createAlphabet()
            self.__init__()

    def decode(self, encoded_text, token):
        _lst_encoded = encoded_text.split("&")
        text = _lst_encoded[0]
        random_lines = _lst_encoded[1:]
        print("DECODE")
        for i, x in enumerate(text):
            selected_row = self.alphabet[int(random_lines[i])]
            print(selected_row)




    def encode(self, text):
        encode_token = list()
        encoded_text = list()
        token_length = len(self.token)
        selected_lines = list()

        print("------------------------------------" + "LENGTH OF ALPHABET" + "---------------------------------------")
        print("--------------------------------------------", len(self.alphabet), "-------------------------------------------")

        for i, x in enumerate(text):
            if not x in iterable_symbols:
                print("Elifbadan kenara cixmayin!")
                self.alpabet_interruption = True
                return
            index = iterable_symbols.index(x)                                   #  sifrelenecek simvolun indexi
            if i <= token_length:                                               #
                token_index = i%token_length                                    #  acar sozun cari indexi
            else:                                                               #
                token_index = (i-1)%token_length                                #  acar sozun cari indexi
            encode_symbol = self.token[token_index]                             #  acar sozun cari simvolu
            cycle = number_of_conditions - 1                                    #  her herf ucun mumkun tekrarlanmalarin sayi
            if encode_symbol in ALPHABET:
                k = ALPHABET.index(encode_symbol)                               #
            else:
                print("Elifbadan kenara cixmayin!")
                return
            x = int(k + cycle * k)                                              #  acar sozun hansi indexler araliginda sifrelenecek
            y = int(k + cycle + cycle*k)                                        #  acar sozun hansi indexler araliginda sifrelenecek
            # print(x, y)
            for line_index in range(x, y+1):
                selected_lines.append(self.alphabet[line_index])
                # print(self.alphabet[line_index])
            selected_line_index = random.choice(range(x, y))                    #  hemin araligda random bir setrin index
            selected_line = self.alphabet[selected_line_index]                  #  hemin araligda random bir setr
            encode_token.append(selected_line_index)                            #  acar soze uygun random secilmis setrin indexi liste elave olunur
            encoded_text.append(selected_line[1][index])                        #  acar soze uygun random secilmis setrde sifrelenecek soze uygun simvol liste elave olunur
            print("Index", selected_lines.index(selected_line))
            # print("selected", selected_line_index)
            # print("selected line: ", selected_line)
            # print("encoded symbol: ", selected_line[1][index])
            # print("==============================")
        return "".join(encoded_text) + "&" + '&'.join(str(x) for x in encode_token)


    def print_encoding(self):
        word_to_encode = input("word: ")
        token = input("token: ")
        self.token = token
        encoded_text = self.encode(word_to_encode)
        self.decode(encoded_text, self.token)
        if not self.alpabet_interruption:
            print("================================================")
            print("ENCODED ->", encoded_text)
            print("================================================")


_encoder = encoder()
_encoder.print_encoding()


