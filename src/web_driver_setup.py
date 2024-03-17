from selenium import webdriver


class WebDriverSetup:
    @staticmethod
    def setup_driver():
        brave_path = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
        options = webdriver.ChromeOptions()
        options.binary_location = brave_path
        options.add_experimental_option("detach", True)
        return webdriver.Chrome(options=options)