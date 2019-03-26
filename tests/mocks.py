import datetime


class MockSERPRO:

    @staticmethod
    def get_cpf_0770374910():
        return {
            "ni":"07770374910",
            "nome":"RAPHAEL FILIPE SCHUBERT",
            "nascimento":"10021992",
            "situacao":{
                "codigo":"0",
                "descricao":"Regular"
            }
        }

    @staticmethod
    def get_invalid():
        return False


class MockDjangoUserModel:

    @staticmethod
    def dominator_lock_account():
        print("\nCalled MockDjangoUserModel.dominator_lock_account()")


class MockDjangoCPFModel:

    def get(self, tax_id):
        if tax_id == "077.703.749-10":
            self.cpf = "077.703.749-10"
            self.nome = "RAPHAEL FILIPE SCHUBERT"
            self.situacao = "{'codigo': '0', 'descricao': 'Regular'}"
            self.data_nascimento = datetime.date(1999, 12, 20)
            self.raw_data = {
                "ni": "07770374910",
                "nome": "RAPHAEL FILIPE SCHUBERT",
                "nascimento": "10021992",
                "situacao": {
                    "codigo": "0", "descricao": "Regular"
                }
            }
            return self

        if tax_id == None:
            return

        if tax_id == 'raw_data':
            self.cpf = "077.703.749-10"
            self.nome = "RAPHAEL FILIPE SCHUBERT"
            self.situacao = "{'codigo': '0', 'descricao': 'Regular'}"
            self.data_nascimento = datetime.date(1999, 12, 20)
            self.raw_data = {}
            return self
