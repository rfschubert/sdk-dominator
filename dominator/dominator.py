from pycpfcnpj import cpf, cnpj, cpfcnpj
from .exceptions import InvalidCPFException, InvalidCNPJException


class Dominator:

    def validate_tax_id(self, tax_id):
        if len(cpfcnpj.clear_punctuation(tax_id)) == 11:
            if not cpf.validate(tax_id):
                raise InvalidCPFException

        if len(cpfcnpj.clear_punctuation(tax_id)) == 14:
            if not cnpj.validate(tax_id):
                raise InvalidCNPJException
