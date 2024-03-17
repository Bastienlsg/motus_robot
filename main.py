from src.motus_game import MotusGame
from src.web_driver_setup import WebDriverSetup


def main():
    driver = WebDriverSetup.setup_driver()
    driver.get('https://sutom.nocle.fr/')

    MotusGame(driver).play()


if __name__ == "__main__":
    main()
