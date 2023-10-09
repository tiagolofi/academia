
from database import DataBase
from pandas import DataFrame, to_datetime

class Academia(object):
	"""docstring for Academia"""
	def __init__(self, username, password):
		super(Academia, self).__init__()
		self.username = username
		self.password = password
		self.db = DataBase()

	def auth(self):

		data = self.db.ler(path='/users/users.json')

		try:

			data = [i for i in data if i['User'] == self.username][0]

		except:

			print('Usuário Inválido')

			return False

		if self.password == data['Password']:
	
			return True, data['Department'], data['Name']
		
		else:

			print('Senha Incorreta')

			return False

	def create_service_train(self):

		data = [{'name': 'Treino 0', 'type': 'Nenhum'}]

		self.db.salvar(data, path = '/treinos/treinos.json')
	
	def create_service_evolution(self):

		data = [{'weight': 0, 'date': '01/01/2022', 'ativities': ['1', '2', '3'], 'diary': 'e disse Deus: haja luz e houve luz.'}]

		self.db.salvar(data, path = '/acompanhamentos/evolution.json')

	def train(self, train: dict):

		data = self.db.ler(path = '/treinos/treinos.json')

		data.append(train)

		self.db.salvar(data, path = '/treinos/treinos.json')

	def train_list(self):

		data = self.db.ler(path = '/treinos/treinos.json')

		return [i['name'] for i in data if i['name'] != 'Treino 0']

	def program(self, data: dict):

		self.db.salvar(data, path = f"""/programas/{data['name']}.json""")

	def evolution(self, evo: dict):
		
		data = self.db.ler(path = '/acompanhamentos/evolution.json')

		data.append(evo)

		self.db.salvar(data, path = '/acompanhamentos/evolution.json')

	def evo(self):

		data = self.db.ler(path = '/acompanhamentos/evolution.json')

		data = [i for i in data if i['weight'] != 0]

		data = DataFrame(data)

		data['ativities'] = [', '.join(i) for i in data['ativities']]

		data['date'] = to_datetime(data['date'])

		return data

	def see_program(self):

		return self.db.listar('/programas/')

	def data_program(self, program):

		data = self.db.ler(path = f"""/programas/{program}""")

		return data

if __name__ == '__main__':

	academia = Academia(username = 'tiagolofi', password = 'jt310799')

	academia.create_service_train()

	academia.create_service_evolution()
