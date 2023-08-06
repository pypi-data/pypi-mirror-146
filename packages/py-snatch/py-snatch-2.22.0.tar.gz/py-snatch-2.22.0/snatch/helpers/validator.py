from loguru import logger


class Validator:
    def __init__(self, data):
        self.instance = data["class"]
        self.data = data["data"]
        if "dataset" in data:
            self.dataset = data["dataset"]

    def receita_federal_validator(self):
        logger.info("Running Receita Federal validator")
        if "emails_extended" in self.dataset:
            if not self.data["mail"]:
                return False
        if "phones_extended" in self.dataset:
            if not self.data["phone"]:
                return False
        if "addresses_extended" in self.dataset:
            if not self.data["address"]:
                return False
        return True

    def start(self):
        if self.instance == "receita_federal_pj":
            return self.receita_federal_validator()
        else:
            return True
