import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


def setup_driver():
    brave_path = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
    options = webdriver.ChromeOptions()
    options.binary_location = brave_path
    options.add_experimental_option("detach", True)
    return webdriver.Chrome(options=options)


def find_cells_by_row(row):
    return row.find_elements(By.TAG_NAME, 'td')


def find_cell_content_by_row(row, index: int):
    return find_cells_by_row(row)[index].text


def site_fully_loaded(driver):
    while True:
        try:
            row = driver.find_element(By.CSS_SELECTOR, '#grille table tr:nth-child(1)').text

            if row[-1] == ".":
                return row
        except Exception:
            continue


def find_word(driver):
    letters_in_row = driver.find_element(By.CSS_SELECTOR, '#grille table tr:nth-child(1)').find_elements(By.TAG_NAME,
                                                                                                         'td')

    first_letter = letters_in_row[0].text
    number_of_letters = len(letters_in_row)

    good_letters = set()
    bad_place_letters = set()
    bad_letters = set()

    with open(f'words/{first_letter}/{first_letter}-{number_of_letters}.txt', 'r', encoding='utf-8') as file:
        words = [word.strip() for word in file.readlines()]

        for i in range(0, 6):
            if i >= 1:
                passed_letters_in_row = driver.find_element(By.CSS_SELECTOR,
                                                            f'#grille table tr:nth-child({i})').find_elements(
                    By.TAG_NAME, 'td')
                for index, letter in enumerate(passed_letters_in_row):
                    if "bien-place" in letter.get_attribute("class"):
                        good_letters.add((letter.text, index))
                    elif "mal-place" in letter.get_attribute("class") and not (letter.text in good_letters):
                        bad_place_letters.add((letter.text, index))
                    else:
                        bad_letters.add(letter.text)

                for letter in good_letters.copy():
                    letter_key = letter[0]
                    for bad_place_letter in bad_place_letters.copy():
                        if letter_key in bad_place_letter[0]:
                            bad_place_letters.remove(bad_place_letter)

                    if letter_key in bad_letters:
                        bad_letters.remove(letter_key)

                for letter in bad_place_letters.copy():
                    letter_key = letter[0]
                    if letter_key in bad_letters:
                        bad_letters.remove(letter_key)

            best_word = ""
            for word in words:
                if all(word[index] == letter for letter, index in good_letters) and \
                        all(letter in word and word.index(letter) not in [index for _, index in bad_place_letters] for
                            letter, _ in bad_place_letters) and \
                        all(letter not in word for letter in bad_letters):
                    best_word = word
                    break

            driver.find_element(By.TAG_NAME, 'body').send_keys(best_word + Keys.ENTER)
            time.sleep(2.5)


def main():
    driver = setup_driver()
    driver.get('https://sutom.nocle.fr/')

    site_fully_loaded(driver)

    driver.find_element(By.ID, 'panel-fenetre-bouton-fermeture').click()

    find_word(driver)


if __name__ == "__main__":
    main()
