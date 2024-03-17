from selenium.webdriver.common.by import By

from src.motus_solver import MotusSolver


class MotusGame:
    def __init__(self, driver):
        self.driver = driver
        self.solver = MotusSolver(driver)

    def fully_loaded(self):
        while True:
            try:
                row = self.driver.find_element(By.CSS_SELECTOR, '#grille table tr:nth-child(1)').text

                if row[-1] == ".":
                    return row
            except Exception:
                continue

    def close_popup(self):
        self.driver.find_element(By.ID, 'panel-fenetre-bouton-fermeture').click()

    def play(self):
        self.fully_loaded()
        self.close_popup()
        self.solver.find_word()
