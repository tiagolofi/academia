
from dropbox import Dropbox, files
from json import dump, load
from io import StringIO, BytesIO
from credentials import TOKEN_DROPBOX

class DataBase(object):
	"""docstring for DataBase"""
	def __init__(self):
		super(DataBase, self).__init__()
		self.db = Dropbox(TOKEN_DROPBOX)

	def listar(self, path: str):
		folders = self.db.files_list_folder(path=path)
		files = [i.name for i in folders.entries]
		return files

	def salvar(self, data: dict, path: str):
		with StringIO() as stream:
			dump(data, stream, indent=2)
			stream.seek(0)
			self.db.files_upload(
				stream.read().encode(), 
				path,
				mode=files.WriteMode.overwrite
			)

	def ler(self, path: str):
		metadata, data = self.db.files_download(path)
		with BytesIO(data.content) as stream:
			content_data = load(stream)
		return content_data

	def tamanho(self, path: str):
		metadata, data = self.db.files_download(path)
		return int(metadata.size)
