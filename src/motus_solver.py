import time
import re

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class MotusSolver:
    def __init__(self, driver):
        self.driver = driver
        self.letters_to_find = set()
        self.letters_to_forbid = ''

    @staticmethod
    def str_replace(string, index, letter):
        string_list = list(string)
        string_list[index] = letter
        return "".join(string_list)

    def set_context(self):
        letters_in_row = self.driver.find_element(By.CSS_SELECTOR, '#grille table tr:nth-child(1)').find_elements(
            By.TAG_NAME,
            'td')

        first_letter = letters_in_row[0].text
        number_of_letters = len(letters_in_row)

        return first_letter, number_of_letters

    def find_word(self):
        first_letter, number_of_letters = self.set_context()

        re_pattern_to_force = '.' * number_of_letters

        with open(f'words/{first_letter}/{first_letter}-{number_of_letters}.txt', 'r', encoding='utf-8') as file:
            letter_positions_to_ignore = [set() for _ in range(number_of_letters)]

            words = [word.strip() for word in file.readlines()]
            best_word = words[0]
            for i in range(0, 6):
                if i >= 1:
                    passed_letters_in_row = self.driver.find_element(By.CSS_SELECTOR,
                                                                     f'#grille table tr:nth-child({i})').find_elements(
                        By.TAG_NAME, 'td')
                    for index, letter in enumerate(passed_letters_in_row):
                        if "bien-place" in letter.get_attribute("class"):
                            re_pattern_to_force = MotusSolver.str_replace(re_pattern_to_force, index, letter.text)
                        elif "mal-place" in letter.get_attribute("class"):
                            self.letters_to_find.add(letter.text)
                            letter_positions_to_ignore[index].add(letter.text)
                        else:
                            self.letters_to_forbid += letter.text

                    re_pattern_wrong_position = "".join(
                        ['.' if len(a) == 0 else '[^' + "".join(a) + "]" for a in letter_positions_to_ignore])
                    letters_known_as_wrongly_positionned = "".join(self.letters_to_find)

                    filtered_values = list(filter(lambda v: re.match(re_pattern_to_force, v), words))

                    filtered_values = list(filter(lambda v: re.match(re_pattern_wrong_position, v), filtered_values))
                    for letter in letters_known_as_wrongly_positionned:
                        filtered_values = list(filter(lambda v: re.match(f'.*{letter}.*', v), filtered_values))

                    if len(self.letters_to_forbid) > 0:
                        filtered_values = list(
                            filter(lambda v: re.match(f'^((?![[^{self.letters_to_forbid}]).)*$', v), filtered_values))

                    best_word = filtered_values[0] if len(filtered_values) > 0 else ""

                self.driver.find_element(By.TAG_NAME, 'body').send_keys(best_word + Keys.ENTER)
                time.sleep(2.5)
                while self.driver.find_element(By.CSS_SELECTOR,
                                               '#grille table tr:nth-child(1)'
                                               ).find_elements(By.TAG_NAME,
                                                               'td')[-1].get_attribute("class") == "resultats":
                    continue
