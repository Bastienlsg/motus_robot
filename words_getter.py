import os

char_map = {
    ('à', 'á', 'â', 'ã', 'ä', 'å'): 'a',
    ('À', 'Á', 'Â', 'Ã', 'Ä', 'Å'): 'A',
    'æ': 'ae',
    'Æ': 'AE',
    'ç': 'c',
    'Ç': 'C',
    ('è', 'é', 'ê', 'ẽ', 'ë', 'e̊'): 'e',
    ('È', 'É', 'Ê', 'Ẽ', 'Ë', 'E̊'): 'E',
    'œ': 'oe',
    'Œ': 'OE',
    ('ì', 'í', 'î', 'ĩ', 'ï', 'i̊'): 'i',
    ('Ì', 'Í', 'Î', 'Ĩ', 'Ï', 'I̊'): 'I',
    ('ò', 'о́', 'ô', 'õ', 'ö', 'o̊'): 'o',
    ('Ò', 'О́', 'Ô', 'Õ', 'Ö', 'O̊'): 'O',
    ('ù', 'ú', 'û', 'ũ', 'ü', 'ů'): 'u',
    ('Ù', 'Ú', 'Û', 'Ũ', 'Ü', 'Ů'): 'U',
}


def process_file(input_file):
    for i in range(4, 11):
        with open(input_file, 'r', encoding="utf-8") as f_in:
            lines = [line.strip().upper() for line in f_in if ' ' not in line and '-' not in line]
            for k, v in char_map.items():
                lines = [line.replace(char, v) for line in lines for char in k]
            lines = list(set(line for line in lines if i == len(line)))

        dir_name = f'words/{input_file[6]}'
        os.makedirs(dir_name, exist_ok=True)

        with open(f'{dir_name}/{input_file[6]}-{i}.txt', 'w', encoding="utf-8") as f_out:
            f_out.write('\n'.join(lines))


def get_words_by_letter_in_file(filenames):
    for filename in filenames:
        with open(filename, "r", encoding='UTF-8') as file:
            words = [word.strip() for word in file if word.lower().startswith("z")]
            autres_words = [word for word in file if not word.lower().startswith("z")]

        with open(filename, "w", encoding='UTF-8') as file:
            file.write(''.join(autres_words))

        with open("targeted_words.txt", "a", encoding='UTF-8') as new_file:
            new_file.write('\n'.join(words))


'''get_words_by_letter_in_file(['words/gutenberg.txt', 
                             'words/liste_francais.txt', 
                             'words/ods4.txt', 
                             'words/ods5.txt', 
                             'words/ods6.txt',
                             'words/pli07.txt'])
process_file('words/Z.txt')'''
