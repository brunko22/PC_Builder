class User:
    def __init__(self):
        self.email = None
        self.admin = None

    def __int__(self, email, admin):
        self.email = email
        self.admin = admin

    def __str__(self):
        return f"{self.email}\n{self.admin}\n"

    def get_email(self):
        return self.email

    def get_admin(self):
        return self.admin

    def set_email(self, email):
        self.email = email

    def set_admin(self, admin):
        self.admin = admin
