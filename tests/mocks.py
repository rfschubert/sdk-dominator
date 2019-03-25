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
    def lock_account():
        print("\nCalled MockDjangoUserModel.lock_account()")
