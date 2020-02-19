"""Connectwise Automate Database functions"""
import mysql.connector


class connector:
    """Create connection to the Automate database"""

    def __init__(self, DBAddress, Username, Password):
        self.mydb = mysql.connector.connect(
            host=DBAddress,
            user=Username,
            passwd=Password,
            database="labtech"
        )

    def __parse_dictionary_to_pipe__(self, values: dict):
        return_string = ""
        keys = list(values.keys())
        for key in keys:
            return_string += f"{key}={values[key]}&"
        return return_string[:-1]

    def RaisePluginAlert(self, AlertTemplateId: int, DeviceType: int, DeviceId: int, Subject: str, Message: str, ReplacementVariables={}, ClientId=1, LocationId=1, ContactId=1):
        """Raise a plugin alert (this does not allow Success alerts)"""
        sql = "INSERT INTO pluginalerts(TemplateId, DeviceType, DeviceId, Message, Replacements, ClientId, ContactId, LocationId) VALUES(%s,%s, %s, %s, %s, %s, %s, %s)"
        val = (AlertTemplateId, DeviceType, DeviceId, f"{Subject}~~~{Message}",
               self.__parse_dictionary_to_pipe__(ReplacementVariables), ClientId, ContactId, LocationId)
        self.__insert_command__(sql, val)

    def RestartDBAgent(self):
        """Restart the database agent."""
        self.__dbagent_command__(1)

    def RestartIIS(self):
        """Restart the IIS."""
        self.__dbagent_command__(2)

    def __dbagent_command__(self, commandId):
        sql = "INSERT INTO dbaseagentcontrol(Command, Parameters) VALUES(%s, %s)"
        val = (commandId, "")
        self.__insert_command__(sql, val)

    def __insert_command__(self, sql, vals):
        mycursor = self.mydb.cursor()
        mycursor.execute(sql, vals)
        self.mydb.commit()

    def Close(self):
        """Close the database connection."""
        self.mydb.close()
