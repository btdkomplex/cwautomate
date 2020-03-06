"""Connectwise Automate Database functions"""
import mysql.connector
from cwautomate.objects.computer import Computer


class connector:
    """Create connection to the Automate database"""

    def __init__(self, DBAddress, Username, Password):
        self.mydb = mysql.connector.connect(
            host=DBAddress,
            user=Username,
            passwd=Password,
            database="labtech",
            autocommit=True
        )

    def __parse_dictionary_to_pipe__(self, values: dict):
        return_string = ""
        keys = list(values.keys())
        for key in keys:
            return_string += f"{key}={values[key]}&"
        return return_string[:-1]

    def RaisePluginAlert(self, AlertTemplateId: int, DeviceType: int, DeviceId: int, Subject: str, Message: str, ReplacementVariables={}, ClientId=None, LocationId=None, ContactId=1):
        """Raise a plugin alert (this does not allow Success alerts)"""
        if ClientId == None:
            mycursor = self.mydb.cursor()
            mycursor.execute(
                f"SELECT ClientId FROM computers WHERE computerId={DeviceId}")
            myresult = mycursor.fetchall()
            ClientId = myresult[0][0]

        if LocationId == None:
            mycursor = self.mydb.cursor()
            mycursor.execute(
                f"SELECT LocationId FROM computers WHERE computerId={DeviceId}")
            myresult = mycursor.fetchall()
            LocationId = myresult[0][0]

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

    def getComputer(self, computerId):
        return Computer(self, computerId)

    def getComputers(self, ClientID=None, LocationID=None, Name=None, OS=None):
        filterValues = []
        returnComputers = []
        filter = ""
        if ClientID:
            filterValues.append(f"ClientID={ClientID}")
        if LocationID:
            filterValues.append(f"LocationID={LocationID}")
        if Name:
            filterValues.append(
                f"Name NOT LIKE '{Name[1:]}'" if Name[0] == "!" else f"Name LIKE '{Name}'")
        if OS:
            filterValues.append(
                f"OS NOT LIKE '{OS[1:]}'" if OS[0] == "!" else f"OS LIKE '{OS}'")

        if len(filterValues) > 0:
            filter = "WHERE "
            for val in filterValues:
                filter += f"{val} AND "
            filter = filter[0:-5]

        cursor = self.mydb.cursor()
        cursor.execute(f"SELECT computerId FROM computers {filter}")
        result = cursor.fetchall()
        for computerId in result:
            returnComputers.append(self.getComputer(computerId[0]))
        return returnComputers

    def getColumns(self, table):
        cursor = self.mydb.cursor()
        cursor.execute(
            f"SELECT * FROM {table} LIMIT 1")
        field_names = [i[0] for i in cursor.description]
        return field_names
