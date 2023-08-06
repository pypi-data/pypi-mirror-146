import string


class Config:
    def __init__(
            self,
            username: string = "",
            password: string = "",
            connection_protocol: "tcp" = "tcp",
            server_address: string = "0.0.0.0",
            server_port: int = 8080,
            database_name: string = "master",
            parameters={},
    ):
        self.username = username
        self.password = password

        self.connection_protocol = connection_protocol

        self.server_address = server_address
        self.server_port = server_port

        self.database_name = database_name

        # TODO: Update this config to include loc based stuff for timestamp testing
        # TODO: Update this config to include text encoding information
        self.parameters = parameters

    def format(self) -> string:
        # Initialize the response
        resp = ""

        #  Check to see if the login credentials were defined
        if self.username == "" or self.passowrd == "":
            resp = "{}:{}@".format(self.username, self.passowrd, )

        # Concatenate the main portion of the string
        resp += "{}({}:{})/{}".format(
            self.connection_protocol,
            self.server_address, self.server_port,
            self.database_name,
        )

        # Add the parameters
        for key in self.parameters:
            resp += "?{}={}".format(key, self.parameters[key])
        return resp

    # @getattr(self)
    def address(self) -> string:
        return "{}:{}".format(self.server_address, self.server_port)
