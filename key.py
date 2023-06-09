class Key:

    @staticmethod
    def get_public_key(login):
        pass

    @staticmethod
    def get_private_key(login, password):
        pass

    @staticmethod
    def get_keys(login, password):
        return Key.get_public_key(login), Key.get_private_key(login, password)

    @staticmethod
    def set_public_key(login):
        pass

    @staticmethod
    def set_private_key(login, password):
        pass

    @staticmethod
    def set_keys(login, password):
        Key.set_public_key(login)
        Key.set_private_key(login, password)
