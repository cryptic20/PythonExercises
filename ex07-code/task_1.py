class Password:
    def __init__(self, name, username, password):
        #  private instance variables
        self.__name = name
        self.__username = username
        self.__password = password

    def __str__(self):
        return '%s: %s / %s' % (self.__name, self.__username, '*' * len(self.__password))

    def pretty_str_password(self):
        return '%s: %s / %s' % (self.__name, self.__username, self.__password)


class PasswordManager:
    def __init__(self, master_password):
        self.__master_password = master_password
        self.__passwords = {}
        self.unlocked = False

    def lock(self):
        self.unlocked = False

    def unlock(self, master_password):
        if master_password == self.__master_password:
            self.unlocked = True
            return True
        else:
            return False

    def create_new_password(self, name, username, password):
        if self.__passwords.get(name) or not self.unlocked:
            # already exist and class is locked
            return None
        else:
            # add new key
            pass_obj = Password(name, username, password)
            self.__passwords[name] = pass_obj
            return pass_obj

    def update_password(self, name, username, password):
        if self.__passwords.get(name) and self.unlocked:
            # it exist
            pass_obj = Password(name, username, password)
            self.__passwords[name] = pass_obj
            return pass_obj
        else:
            # name does not exist
            return None

    def get_password(self, name):
        if self.__passwords.get(name) and self.unlocked:
            return self.__passwords.get(name)
        else:
            return None

    def list_passwords(self):
        if self.unlocked:
            return [value.pretty_str_password() for key, value in self.__passwords.items()]
        else:
            return [str(value) for key, value in self.__passwords.items()]


if __name__ == '__main__':
    test = Password('facebook', 'admin', 'helloworld123')
    print(test)
    new_test = PasswordManager('helloworld')
    print(new_test.unlock('helloworld'))
    print(new_test.create_new_password('facebook', 'admin', 'helloworld'))
    print(new_test.create_new_password('google', 'gmailadmin', 'helloworld'))
    print(new_test.update_password('facebook', 'notadmin', 'nothelloworld'))
    print(new_test.list_passwords())
    new_test.lock()
    print(new_test.list_passwords())





