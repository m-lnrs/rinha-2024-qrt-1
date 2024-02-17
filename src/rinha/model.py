class Client():
	def __init__(self, **entries):
		self.__dict__.update(entries)

	def __init__(self, number=None, name=None, limit_amount=None):
		self.number = number
		self.name = name
		self.limit_amount = limit_amount

class Balance():
	def __init__(self, **entries):
		self.__dict__.update(entries)

	def __init__(self, number=None, client_number=None, amount=None):
		self.number = number
		self.amount = amount
		self.client_number = client_number

class Response():
	def __init__(self, **entries):
		self.__dict__.update(entries)

	def __init__(self, balance=None, success=None, message=None):
		self.balance = balance
		self.success = success
		self.message = message

class Transaction():
	def __init__(self, **entries):
		self.__dict__.update(entries)

	def __init__(self, number=None, client_number=None, amount=None, transaction_type=None, description=None, done=None):
		self.number = number
		self.client_number = client_number
		self.amount = amount
		self.transaction_type = transaction_type
		self.description = description
		self.done = done

class Statement():
	def __init__(self, **entries):
		self.__dict__.update(entries)

	def __init__(self, balance=None, done=None, limit_amount=None):
		self.balance = balance
		self.done = done
		self.limit_amount = limit_amount
