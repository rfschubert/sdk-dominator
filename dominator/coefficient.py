class Coefficient:
    APPLIED_RULES = []
    COEFFICIENT = 0

    def apply(self, rule):
        if rule not in self.APPLIED_RULES:
            self.APPLIED_RULES.append(rule)

        self.calculate()
        return self

    def calculate(self):
        self.COEFFICIENT = 0
        for rule in self.APPLIED_RULES:
            self.COEFFICIENT += self.check_rule_value(rule)

        if self.COEFFICIENT < 0:
            self.COEFFICIENT = 0

        return self.COEFFICIENT

    def check_rule_value(self, rule):
        RULES = {
            'INVALID_TAX_ID': 100,
            'INVALID_ADDRESS': 50,
            'EMAIL_CONTAINS_CLIENT_NAME': -30,
            'EMAIL_CONFIRMED': -25,
            'PHONE_INFORMED': -25,
            'PHONE_CONFIRMED': -25,
            'DRIVER_LICENSE_UPLOADED': -10,
            'DRIVER_LICENSE_VALIDATED': -30,
            'PROOF_OF_ADDRESS_UPLOADED': -10,
            'PROOF_OF_ADDRESS_VALIDATED': -30,
            'FAKE_DOCUMENT_IDENTIFIED': 250,
            'FAKE_PROOF_OF_ADDRESS_IDENTIFIED': 250,
            'CRIME_HISTORY_FEDERAL_DATABASES': 65,
            'FINANCIAL_CRIME_HISTORY_IDENTIFIED': 85,
            'BILLET_FRAUD_IDENTIFIED': 35,
            'FRAUD_CLAIMED_BY_THIRD_PART': 10,
            'A_MONTH_WITHOUT_NEGATIVE_CLAIMS': -3,
            'REQUEST_FOR_BREACH_OF_BANK_SECRECY_BY_THIRD_PART': 75,
            'REQUEST_FOR_BREACH_OF_BANK_SECRECY_BY_FINANCIAL_FRAUD': 310,
            'SELFIE_WITH_DOCUMENTS_VALIDATED': -20,
            'SAME_IP_ACESSING_MORE_THAN_ONE_ACCOUNT_ON_SAME_DAY': 20,
            'SAME_EMAIL_CONFIGURED_FOR_MANY_ACCOUNTS': 55,
            'SAME_PHONE_CONFIGURED_FOR_MANY_ACCOUNTS': 55,
            'TWO_AUTH_FACTOR_NOT_CONFIGURED': 20,
        }

        return RULES[rule]

