class IDbMutable:

	def __init__(self, method, DbName):
		self.method = method
		self.__DbName = DbName

	def execute_query(self, query):
		return self.method(query, self.__DbName)

class IDbUnMutable:

	def __init__(self, method, DbName):
		self.__method = method
		self.__DbName = Dbname

	def execute_query(self, query):
		return self.__method(query, self.__DbName)
