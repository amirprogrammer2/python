from words import Words

all_words = []

while True:
    print("1:add word :")
    print("2:find meaning :")
    print("3:see all word : ")
    choice = input("1 , 2 , 3 , or exit : ")
    if choice == "exit":
        break
    if choice == "1":
        word_endlish = input("enter english word : ")
        if word_endlish == "exit":
            break
        word_pershin = input("enter pershin word : ")
        word = Words(word_endlish,word_pershin)
        all_words.append(word)

    elif choice == "2":
        user_input = input("enter english word or pershin word : ")
        found = False
        for word in all_words:
            if word.word_english or word.word_pershin == user_input:
                print(word.meaning())
                found = True
                break
            if not found:
                print("word nit found ")
    elif choice =="3":
        for woord in all_words:
            print(woord.show())