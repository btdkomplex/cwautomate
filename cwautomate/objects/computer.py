class Computer:
    def __init__(self, connection, ComputerID):
        self.connection = connection
        self.ComputerID = ComputerID

    def __get_LastContact(self):
        return self.__basic_query("LastContact")

    def __get_Name(self):
        return self.__basic_query("Name")

    def __get_LoggedInUsers(self):
        return self.__basic_query("Username")

    def __get_OS(self):
        return self.__basic_query("OS")

    def __get_PCDate(self):
        return self.__basic_query("PCDate")

    def __get_Uptime(self):
        return self.__basic_query("Uptime")

    def __get_LocalAddress(self):
        return self.__basic_query("LocalAddress")

    def __get_RouterAddress(self):
        return self.__basic_query("RouterAddress")

    def __get_ClientID(self):
        return self.__basic_query("ClientID")

    def __get_LocationID(self):
        return self.__basic_query("LocationID")

    def __get_ClientName(self):
        return self.__basic_query("Name", "Clients", "ClientID", self.__get_ClientID())

    def __get_LocationName(self):
        return self.__basic_query("Name", "Locations", "LocationID", self.__get_LocationID())

    def __get_MAC(self):
        return self.__basic_query("MAC")

    def __get_Domain(self):
        return self.__basic_query("Domain")

    def __get_TimeZone(self):
        return self.__basic_query("TimeZone")

    def __get_LastInventory(self):
        return self.__basic_query("LastInventory")

    def __basic_query(self, column, table="computers", filter="ComputerID", filterValue=None):
        if self.__exists():
            cursor = self.connection.mydb.cursor()
            cursor.execute(
                f"SELECT {column} FROM {table} WHERE {filter}={filterValue if filterValue != None else self.ComputerID}")
            result = cursor.fetchone()
            cursor.close()
            return result[0]
        return 0

    def __exists(self):
        cursor = self.connection.mydb.cursor()
        cursor.execute(
            f"SELECT COUNT(*) FROM computers WHERE ComputerID={self.ComputerID}")
        result = cursor.fetchone()
        cursor.close()
        return False if result[0] == 0 else True

    Name = property(__get_Name)
    LastContact = property(__get_LastContact)
    LoggedInUsers = property(__get_LoggedInUsers)
    OS = property(__get_OS)
    PCDate = property(__get_PCDate)
    Uptime = property(__get_Uptime)
    LocalAddress = property(__get_LocalAddress)
    RouterAddress = property(__get_RouterAddress)
    ClientID = property(__get_ClientID)
    LocationID = property(__get_LocationID)
    ClientName = property(__get_ClientName)
    LocationName = property(__get_LocationName)
    MAC = property(__get_MAC)
    Domain = property(__get_Domain)
    TimeZone = property(__get_TimeZone)
    LastInventory = property(__get_LastInventory)