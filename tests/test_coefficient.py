from unittest import TestCase

from dominator import Coefficient


class CoefficientTestCase(TestCase):

    def test_check_rules_values(self):
        self.assertEqual(Coefficient().check_rule_value('INVALID_TAX_ID'), 100)
        self.assertEqual(Coefficient().check_rule_value('INVALID_ADDRESS'), 50)
        self.assertEqual(Coefficient().check_rule_value('EMAIL_CONTAINS_CLIENT_NAME'), -30)
        self.assertEqual(Coefficient().check_rule_value('EMAIL_CONFIRMED'), -25)
        self.assertEqual(Coefficient().check_rule_value('PHONE_INFORMED'), -25)
        self.assertEqual(Coefficient().check_rule_value('PHONE_CONFIRMED'), -25)
        self.assertEqual(Coefficient().check_rule_value('DRIVER_LICENSE_UPLOADED'), -10)
        self.assertEqual(Coefficient().check_rule_value('DRIVER_LICENSE_VALIDATED'), -30)
        self.assertEqual(Coefficient().check_rule_value('PROOF_OF_ADDRESS_UPLOADED'), -10)
        self.assertEqual(Coefficient().check_rule_value('PROOF_OF_ADDRESS_VALIDATED'), -30)
        self.assertEqual(Coefficient().check_rule_value('FAKE_DOCUMENT_IDENTIFIED'), 250)
        self.assertEqual(Coefficient().check_rule_value('FAKE_PROOF_OF_ADDRESS_IDENTIFIED'), 250)
        self.assertEqual(Coefficient().check_rule_value('CRIME_HISTORY_FEDERAL_DATABASES'), 65)
        self.assertEqual(Coefficient().check_rule_value('FINANCIAL_CRIME_HISTORY_IDENTIFIED'), 85)
        self.assertEqual(Coefficient().check_rule_value('BILLET_FRAUD_IDENTIFIED'), 35)
        self.assertEqual(Coefficient().check_rule_value('FRAUD_CLAIMED_BY_THIRD_PART'), 10)
        self.assertEqual(Coefficient().check_rule_value('A_MONTH_WITHOUT_NEGATIVE_CLAIMS'), -3)
        self.assertEqual(Coefficient().check_rule_value('REQUEST_FOR_BREACH_OF_BANK_SECRECY_BY_THIRD_PART'), 75)
        self.assertEqual(Coefficient().check_rule_value('REQUEST_FOR_BREACH_OF_BANK_SECRECY_BY_FINANCIAL_FRAUD'), 310)
        self.assertEqual(Coefficient().check_rule_value('SELFIE_WITH_DOCUMENTS_VALIDATED'), -20)
        self.assertEqual(Coefficient().check_rule_value('SAME_IP_ACESSING_MORE_THAN_ONE_ACCOUNT_ON_SAME_DAY'), 20)
        self.assertEqual(Coefficient().check_rule_value('SAME_EMAIL_CONFIGURED_FOR_MANY_ACCOUNTS'), 55)
        self.assertEqual(Coefficient().check_rule_value('SAME_PHONE_CONFIGURED_FOR_MANY_ACCOUNTS'), 55)
        self.assertEqual(Coefficient().check_rule_value('TWO_AUTH_FACTOR_NOT_CONFIGURED'), 20)

    def test_apply_rule(self):
        coefficient = Coefficient()
        coefficient.apply('INVALID_TAX_ID')
        coefficient.apply('INVALID_TAX_ID')
        self.assertEqual(coefficient.COEFFICIENT, 100)
        coefficient\
            .apply('EMAIL_CONTAINS_CLIENT_NAME')\
            .apply('PHONE_INFORMED')\
            .apply('CRIME_HISTORY_FEDERAL_DATABASES')
        self.assertEqual(coefficient.COEFFICIENT, 110)
        del coefficient

