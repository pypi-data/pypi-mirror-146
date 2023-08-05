class SsoValidToken:
    def __init__(self, decoded_token):
        self.sso_uuid = decoded_token["sub"]
        self.first_name = decoded_token["given_name"]
        self.last_name = decoded_token["family_name"]
        self.username = decoded_token["username"]
        self.email = decoded_token["email"]
        self.list_apps = list(decoded_token["resource_access"].keys())

    def to_dict(self):
        return {
            "sso_uuid": self.sso_uuid,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "list_apps": self.list_apps,
        }
