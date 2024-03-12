class IDbMutable


	def __init__(self, object):
		self.object = object

	def execute_query(self, query):
		return self.object.execute_query(query)

class IDbUnMutable:

	def __init__(self, object):
		self.__object = object

	def execute_query(self, query):
		return self.__object.execute_query(query)

class ILoggerMutable:

        def __init__(self, object):
                self.object = object

        def execute_query(self, mesaage):
                return self.object.log(query)

class  ILoggerUnMutable:

        def __init__(self, object):
                self.__object = object

        def log(self, message):
                return self.__object.log(message)
