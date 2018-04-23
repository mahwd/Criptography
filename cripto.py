from pathlib import Path
from builtins import print
from itertools import *
import random
import math, os
from time import sleep
from tkinter import *
from tkinter import messagebox
import traceback

import time

ALPHABET = "ABCDEF"  # elifbanin teyini


def check_alphabet():
    alphabet_list_in_file = ""
    try:
        with open("alphabet.txt", 'r') as f:
            lines = f.readlines()
            if lines[0].strip():
                alphabet_list_in_file = lines[0].strip()
                print(alphabet_list_in_file)
    except:
        print(traceback.print_exc())
        alphabet_list_in_file = ALPHABET
        createAlphabet(ALPHABET)
    return alphabet_list_in_file


iterable_symbols = tuple(ALPHABET)  # elifba tuple - a convert edir "ABCDE" => ("A", "B", "C", "D", "E" )

letters = list()  # boş list teyin edirəm

number_of_repeats = math.factorial(
    len(iterable_symbols))  # Əlifbanin sayına uyğun olaraq bütün mümkün variantların sayını tapıram

number_of_iterables = len(iterable_symbols)  # Əlifabanın hərflərinin sayını tapıram

number_of_conditions = number_of_repeats / number_of_iterables  # Bir hərflə başlayan sətrlərin sayı


def shuffleAlphabet(_list, **kwargs):  # Əlifbani sətrlərini qarışdıraraq fayla yazmaq üçün funksiya
    os.remove('alphabet.txt') if Path('alphabet.txt').exists() else os.system('touch alphabet.txt')
    for i in range(int(number_of_conditions)):  # Hər hərflə başlayan sətrləri iterasiya edirəm | range(6) => 0..5
        for j, y in enumerate(
                _list):  # Hər iterasiyada ötürülmüş listi enumerate vasitəsilə indexləyərək iterasiya edirəm   exmple: j=0, y=("A", "B", "C", "D", "E" )
            if (i + j) % number_of_conditions == 0 or j % number_of_conditions == number_of_conditions:
                line = (j, y)
                with open('alphabet.txt',
                          'a') as f:  # alphabet.txt adlı fayl yaradır və qarışdırılmış sətrləri fayla yazıram
                    if j == 0 and i == 0:  # ilk sətrə Əlifbanın sətrləri yazıram
                        f.writelines(kwargs["alpha_symbols"] + '\n' if kwargs["alpha_symbols"] else ALPHABET + '\n')
                    f.writelines(str(line) + "\n")
                    f.close()  # fayli bağlıyıram


def createAlphabet(_list):  # Əlifbanın sətrlərini yaradan funksiya
    print("alphabet recreating")
    letters = list()
    if _list:
        for m in permutations(tuple(_list)):  # Əlifbanın hərflərinə uyğun bütün mümkün variantları iterasiya edərək
            letters.append(m)  # letters listinə yazır
        shuffleAlphabet(letters,
                        alpha_symbols=_list)  # sonra həmin lisi qarışdırmaq üçün shuffleAlphabet(letters) funksiyasına ötürürəm
    else:
        for m in permutations(iterable_symbols):  # Əlifbanın hərflərinə uyğun bütün mümkün variantları iterasiya edərək
            letters.append(m)  # letters listinə yazır
        shuffleAlphabet(letters)  # sonra həmin lisi qarışdırmaq üçün shuffleAlphabet(letters) funksiyasına ötürürəm


check_alphabet()


class encoder():  # şifrələmək prosesini yerine yetirən class

    def __init__(self, token):  # classın constructoruna açar söz ötürürəm
        self.alphabet = list()  # class dəyişənlərini təyin edirəm
        self.token = token
        self.alpabet_interruption = False
        try:
            with open("alphabet.txt", 'r') as f:  # əgər alphabet.txt adlı fayl mövcuddursa onu açıram
                content = f.readlines()  # faylın içindəki sətrləri oxuyuram
                if content[0].strip() != ALPHABET:  # faylın birinci sətrinin Əlifbaya uyğunluöunu yoxlayıram
                    os.remove("alphabet.txt")  # əgər bərabər deyillərsə faylı silirəm
                    createAlphabet()  # yenidən createAlphabet() funksiyasını çağıraraq yeni əlifbaya uyğun fayl yaradıram
                    self.__init__(token)  # və yeni faylın oxunması üçün constructoru yenidən çağırıram
                else:  # əgər faylda olan əlifba bizim əlifbaya uyğundursa
                    if not content[1]:  # contentin varlığını yoxlayıram
                        print("not content")  # əgər yoxdursa
                        createAlphabet()  # createAlphabet() funksiyasını çağıraraq faylı yenidən yaradıram
                        self.__init__(token)  # və yeni faylın oxunması üçün constructoru yenidən çağırıram
                    else:  # content mövcuddursa
                        content = [x.strip() for x in content]  # her setrin sonundan '\n'- i silir
            for index, el in enumerate(content):  # sonra contenti ENUMERATE edərək iterasiya edib
                if index != 0:  # birinci sətrdən başqa
                    self.alphabet.append(eval(
                        el))  # bütün sətrləri eval() funksiyası vasitəsilə çevrilir. exp: ex="("A", "B")" eval(ex) => ("A", "B") <class "tuple">
        except:  # əgər fayl mövcud deyilsə və ya başqa bir səbəbdən xəta baş verərsə
            print("no file")
            createAlphabet()  # əlifba yenidən yaradılır
            self.__init__(token)  # və yeni faylın oxunması üçün constructoru yenidən çağırılır

    def decode(self, encoded_text):  # şifrəni deşifrələmək üçün funksiya
        decoded_text = list()  # deşifrələnmiş simvollarin yığmaq üçün boş list yaradıram
        token_length = len(self.token)  # tokenin simvol sayı
        _lst_encoded = encoded_text.split("&")  # sifrənin içindəki
        text = _lst_encoded[0]  # şifrələnmiş sözü
        random_lines = _lst_encoded[1:]  # və random sətrləri ayırıram
        devided_alphabet = self.devide_alphabet()  # devide_alphabet() funksiyası vasitəsilə əlifbanı hər hərflə başlaya sətrlərin sayı qədər hissəyə bölürəm
        for i, x in enumerate(text):  # şifrələnmiş sözü iterasiya edib
            if i <= token_length:  # açar sözün simvol sayı şifrənin simvol sayını aşmırsa
                token_index = i % token_length  # açar sözün cari indexi sifrənin cari indexinin açarsözün simvol sayına bölünməsindən alınan qalığa bərabər olur
            else:  # açar sözün simvol sayı şifrənin simvol sayını aşırsa
                token_index = (i - 1) % token_length  # çar sözün cari indexi (i-1)%token_length düsturu ilə hesablanır
            if self.token[token_index] in ALPHABET:  # əgər açar sözün cari indexindəki simvol əlifbada varsa
                token_alphabet_index = ALPHABET.index(self.token[
                                                          token_index])  # əgər açar sözün cari indexindəki simvol əlifbada varsa onun indexini tapiram
                selected_lines = devided_alphabet[
                    token_alphabet_index]  # hissələrə bölünmüş əlifbadan yuxarıdakı indexdəki listi selected_lines dəyişəninə təyin edirəm
                selected_line = selected_lines[int(random_lines[
                                                       i])]  # açar sözə uyğun seçilmiş sətrlərdən(selected_lines) şifrənin içindəki random str indexlərindən uyğun olanı seçib selected_line dəyişninə mənimsədirəm
                index = selected_line[1].index(x)  # həmin sətrdə şifrələnmiş sözün uyğun simvolunun indexini tapıram
                decoded_text.append(ALPHABET[
                                        index])  # sonda həmin indexdəki əlifba simvolu deşifrələnmiş simvol olur və onu deşifrələnmiş simvollarin yığmaq üçün boş listə əlavə edirəm
            else:  # əgər açar sözün cari indexindəki simvol əlifbada yoxdursa yəni əlifbadan kənara çıxılarsa
                return "Elifbadan kenara cixmayin"
        return "".join(
            decoded_text)  # hər şey qaydasında bitərsə şifrələnmiş simvolların yığıldığı list stringify edərək return edirəm

    def devide_alphabet(self):
        devided_list = list()
        temp_lst = list()
        for i, k in enumerate(self.alphabet):
            if i % number_of_conditions == 0 and i != 0:
                devided_list.append(temp_lst)
                temp_lst = []
                temp_lst.append(k)
            elif i == len(self.alphabet) - 1:
                temp_lst.append(k)
                devided_list.append(temp_lst)
            else:
                temp_lst.append(k)
        return devided_list

    def encode(self, text):
        encode_token = list()
        encoded_text = list()
        token_length = len(self.token)
        selected_lines = list()

        for i, x in enumerate(text):
            index = iterable_symbols.index(x)  # sifrelenecek simvolun indexi
            if i <= token_length:  #
                token_index = i % token_length  # acar sozun cari indexi
            else:  #
                token_index = (i - 1) % token_length  # acar sozun cari indexi
            encode_symbol = self.token[token_index]  # acar sozun cari simvolu
            cycle = number_of_conditions - 1  # her herf ucun mumkun tekrarlanmalarin sayi

            if not x in iterable_symbols or not encode_symbol in iterable_symbols:
                print("Elifbadan kenara cixmayin!")
                self.alpabet_interruption = True
                return
            if encode_symbol in ALPHABET:
                k = ALPHABET.index(encode_symbol)  #
            x = int(k + cycle * k)  # acar sozun hansi indexler araliginda sifrelenecek
            y = int(k + cycle + cycle * k)  # acar sozun hansi indexler araliginda sifrelenecek
            for line_index in range(x, y + 1):
                selected_lines.append(self.alphabet[line_index])
                # print(self.alphabet[line_index])
            selected_line_index = random.choice(range(x, y + 1))  # hemin araligda random bir setrin index
            selected_line = self.alphabet[selected_line_index]  # hemin araligda random bir setr
            random_index = range(x, y + 1).index(selected_line_index)
            encode_token.append(random_index)  # acar soze uygun random secilmis setrin indexi liste elave olunur
            encoded_text.append(selected_line[1][
                                    index])  # acar soze uygun random secilmis setrde sifrelenecek soze uygun simvol liste elave olunur
        return "".join(encoded_text) + "&" + '&'.join(str(x) for x in encode_token)


class CriptoGUI():

    def __init__(self):
        self.main_window = Tk()
        # change window title
        self.main_window.title("Choose user type")
        self.user_login_window = dict()
        self.admin_login_window = dict()
        self.admin_panel = dict()
        self.encode_window = dict()
        self.user = dict()
        self.main_window.attributes('-zoomed', True)
        self.main_window.config(bg="white")
        buttons_container = Frame(self.main_window, bg="white")
        buttons_container.place(relx=0.5, rely=0.5, anchor=CENTER, width=300, height=100, bordermode="outside")
        user_btn = Button(buttons_container, text="User Login", command=self.user_click)
        admin_btn = Button(buttons_container, text="Admin Login", command=self.admin_click)
        close_btn = Button(self.main_window, text="Close", command=lambda: self.quit(self.main_window))
        user_btn.pack(side=LEFT, padx=20, pady=20)
        admin_btn.pack(side=LEFT, padx=20, pady=20)
        close_btn.grid(column=1, row=1)
        close_btn.place(relx=1.0, rely=1.0, width=80, height=40, anchor=SE, bordermode="outside")

        self.main_window.mainloop()

    # ===============
    # user part ====
    # ===============

    def user_click(self):
        # create user login window
        self.user_login_window = Tk()
        # change window title
        self.user_login_window.title("Login to encode and decode")
        # maximize window
        self.user_login_window.attributes('-zoomed', True)
        # changing main window background color
        self.user_login_window.config(bg="white")
        # creating container for entries
        entries_container = Frame(self.user_login_window, bg="white")
        # placing ui container in main window
        entries_container.place(relx=0.5, rely=0.5, anchor=CENTER, width=300, height=150, bordermode="outside")
        # creating ui widgets
        email_entry = Entry(entries_container)
        email_label = Label(entries_container, text="email")
        passwrod_entry = Entry(entries_container, show="*", width=15)
        passwrod_label = Label(entries_container, text="password")
        login_btn = Button(entries_container, text="LOGIN",
                           command=lambda: self.login_user(email_entry.get(), passwrod_entry.get()))
        close_btn = Button(self.user_login_window, text="BACK", command=lambda: self.quit(self.user_login_window))
        # placing ui widgets in container
        email_label.pack(side=TOP, pady=(0, 10))
        email_entry.pack(side=TOP, padx=20, pady=0)
        passwrod_label.pack(side=TOP, pady=10)
        passwrod_entry.pack(side=TOP, padx=20, pady=0)
        login_btn.pack(side=TOP, padx=20, pady=(10, 0))
        close_btn.place(relx=1.0, rely=1.0, width=80, height=40, anchor=SE, bordermode="outside")
        # load user login window
        self.user_login_window.mainloop()

    def login_user(self, email, password):
        try:
            with open("user", "r") as f:
                _users = f.readline().strip()
                if _users:
                    user = eval(_users)
                    logged_in = False
                    if email == user["email"] and password == user["password"]:
                        logged_in = True
                if logged_in:
                    self.quit(self.main_window)
                    self.quit(self.user_login_window)
                    self.user = user
                    self.trigger_encode_window()
                else:
                    messagebox.showinfo("OPS", "incorrect email or password")
        except:
            messagebox.showinfo("ERROR", traceback.print_exc())

    def trigger_encoder(self, code, token, label):
        _encoder = encoder(token)
        encoded_text = _encoder.encode(text=code)
        label.config(text=encoded_text)

    def trigger_encode_window(self):
        # creating trigger_encode_window
        self.encode_window = Tk()
        # maximize window
        self.encode_window.attributes('-zoomed', True)
        # changing main window background color
        self.encode_window.config(bg="white")
        # creating container for entries
        entries_container = Frame(self.encode_window, bg="white")
        # placing ui container in main window
        entries_container.place(relx=0.5, rely=0.5, anchor=CENTER, width=300, height=150, bordermode="outside")
        # creating ui widgets
        code_entry = Entry(entries_container)
        code_label = Label(entries_container, text="Şifrələcək söz")
        token_entry = Entry(entries_container, )
        token_label = Label(entries_container, text="Açar söz")
        label_encode = Label(self.encode_window, text="", bg="white")
        label_encode.pack(side=TOP, padx=20, pady=10)
        token = token_entry.get().upper()
        code = code_entry.get().upper()
        login_btn = Button(entries_container, text="Şifrələ",
                           command=lambda: self.trigger_encoder(code, token, label_encode))
        back_btn = Button(self.encode_window, text="Bağla", command=lambda: self.quit(self.encode_window))
        # placing ui widgets in container
        code_label.pack(side=TOP, pady=(0, 10))
        code_entry.pack(side=TOP, padx=20, pady=0)
        token_label.pack(side=TOP, pady=10)
        token_entry.pack(side=TOP, padx=20, pady=0)
        login_btn.pack(side=TOP, padx=20, pady=10)
        back_btn.place(relx=1.0, rely=1.0, width=80, height=40, anchor=SE, bordermode="outside")
        # load user login window
        self.encode_window.mainloop()

    # ===============
    # admin part ====
    # ===============

    def admin_click(self):
        # create admin login window
        self.admin_login_window = Tk()
        # maximize window
        self.admin_login_window.attributes('-zoomed', True)
        # changing main window background color
        self.admin_login_window.config(bg="white")
        # creating container for entries
        entries_container = Frame(self.admin_login_window, bg="white")
        # placing ui container in main window
        entries_container.place(relx=0.5, rely=0.5, anchor=CENTER, width=300, height=150, bordermode="outside")
        # creating ui widgets
        email_entry = Entry(entries_container)
        email_label = Label(entries_container, text="email")
        passwrod_entry = Entry(entries_container, show="*", width=15)
        passwrod_label = Label(entries_container, text="password")
        login_btn = Button(entries_container, text="LOGIN",
                           command=lambda: self.login_admin(email_entry.get(), passwrod_entry.get()))
        close_btn = Button(self.admin_login_window, text="Geri", command=lambda: self.quit(self.admin_login_window))
        # placing ui widgets in container
        email_label.pack(side=TOP, pady=(0, 10))
        email_entry.pack(side=TOP, padx=20, pady=0)
        passwrod_label.pack(side=TOP, pady=10)
        passwrod_entry.pack(side=TOP, padx=20, pady=0)
        login_btn.pack(side=TOP, padx=20, pady=(10, 0))
        close_btn.place(relx=1.0, rely=1.0, width=80, height=40, anchor=SE, bordermode="outside")
        # load user login window
        self.admin_login_window.mainloop()

    def login_admin(self, email, password):
        try:
            with open("admin", "r") as f:
                _admin = f.readline().strip()
                if _admin:
                    admin = eval(_admin)
                    logged_in = False
                    if email == admin["email"] and password == admin["password"]:
                        logged_in = True
                if logged_in:
                    self.quit(self.main_window)
                    self.quit(self.admin_login_window)
                    # self.admin = admin
                    self.trigger_admin_window()
                else:
                    messagebox.showinfo("OPS", "incorrect email or password")
        except:
            messagebox.showinfo("ERROR", traceback.print_exc())

    def trigger_admin_window(self):
        # creating trigger_encode_window
        self.admin_panel = Tk()
        # change window title
        self.admin_panel.title("Change Alphabet [Admin]")
        # maximize window
        self.admin_panel.attributes('-zoomed', True)
        # changing main window background color
        self.admin_panel.config(bg="white")
        # creating container for entries
        entries_container = Frame(self.admin_panel, bg="white")
        # placing ui container in main window
        entries_container.place(relx=0.5, rely=0.5, anchor=CENTER, width=300, height=150, bordermode="outside")
        # creating ui widgets
        alphabet_letters_entry = Entry(entries_container)
        alphabet_letters_label = Label(entries_container, text="Yeni əlifbanın simvolları")
        alphabet_letters_label = Label(entries_container, text="Əlifbanın simvolları: %s" % check_alphabet())
        loader = Label(entries_container, text="")
        change_btn = Button(entries_container, text="Dəyiş",
                            command=lambda: self.change_alphabet(alphabet_letters_entry.get(), loader, alphabet_letters_label))
        back_btn = Button(self.admin_panel, text="Geri", command=lambda: self.launch_admin_login(self.admin_panel))
        # placing ui widgets in container
        loader.pack(side=TOP, padx=20, pady=10)
        alphabet_letters_label.pack(side=TOP, padx=20, pady=0)
        alphabet_letters_entry.pack(side=TOP, pady=(0, 10))
        change_btn.pack(side=TOP, padx=20, pady=10)
        back_btn.place(relx=1.0, rely=1.0, width=80, height=40, anchor=SE, bordermode="outside")
        # load user login window
        self.admin_panel.mainloop()

    def change_alphabet(self, alpha_list, loader, alpha_label):
        loader.config(bg="white", text='alphabet recreating...')
        createAlphabet(alpha_list)
        loader.config(text="")
        alpha_label.config(text="Əlifbanın simvolları: %s" % check_alphabet())

    @staticmethod
    def quit(_window):
        _window.destroy()

    def launch_user_login(self, _window):
        self.quit(_window)
        self.user_click()

    def launch_admin_login(self, _window):
        self.quit(_window)
        self.admin_click()


CriptoGUI()


def run_in_console():
    print("salam, ")
    user_input = input("encode elemek isteyirsense 1, decode elemek isteyirsense 2 daxil et: ")
    while 1:
        if user_input == "1":
            word_to_encode = input("Sifrelemek istediyin sozu daxil et: ")
            token = input("Acar sozu daxil et: ")
            is_valid = True
            for x in word_to_encode:
                if not x in ALPHABET:
                    print("sifrelenecek soz elifbaya uygun olaraq yalniz ", ALPHABET, "herflerinden ibaret ola biler")
                    is_valid = False
                    break
            for x in token:
                if not x in ALPHABET:
                    print("Acar soz elifbaya uygun olaraq yalniz ", ALPHABET,
                          "herflerinden ibaret ola biler")
                    is_valid = False
                    break
            if is_valid:
                _encoder = encoder(token)
                decoded_text = _encoder.encode(text=word_to_encode)
                print("=================")
                print("daxil etdiyiniz soz sifrelendi: ", decoded_text)
        elif user_input == "2":
            word_to_decode = input("Sifresini acmaq istediyin setri daxil et: ")
            token = input("Acar sozu daxil et: ")
            is_valid = True
            for x in word_to_decode.split("&")[0]:
                if not x in ALPHABET:
                    print("daxil edilen elifbaya uygun olaraq yalniz ", ALPHABET, "herflerinden ibaret ola biler")
                    is_valid = False
                    break
            for x in token:
                if not x in ALPHABET:
                    print("Acar soz elifbaya uygun olaraq yalniz ", ALPHABET,
                          "herflerinden ibaret ola biler")
                    is_valid = False
                    break
            if is_valid:
                _encoder = encoder(token)
                decoded_text = _encoder.decode(word_to_decode)
                print("=================")
                print("daxil etdiyiniz setr desifrelendi: ", decoded_text)
        else:
            break
        user_input = input(
            "encode elemek isteyirsense 1, decode elemek isteyirsense 2 daxil et, proqramdan cixmaq ucun her hansi simvol daxil et: ")
