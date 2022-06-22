with open('wordsss.txt', encoding='utf-8') as file:
    words_list = [line for line in file.readlines()]

w_new = []
for w in words_list:
    ww = str(w).split('-')[0].replace('[\' ', '').strip()
    w_new.append(ww)

str_num = 0
print(w_new)

# запись слов из СПИСКА в файл
with open('words.txt', 'a', encoding='utf-8') as file:
    for word_ in w_new:
        file.write(f'{word_}\n')

