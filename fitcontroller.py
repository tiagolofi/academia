
import streamlit as st
from academia import Academia
import altair as alt

st.set_page_config(page_title='FitController', page_icon='💪')

css = """

	<style>
		@import url('https://fonts.googleapis.com/css2?family=MontSerrat&display=swap');
		@font-face{
			font-family: 'MontSerrat', sans-serif;
		}
		html, body, [class*="css"] {
		font-family: 'MontSerrat', sans-serif;
		}
	</style>

"""

st.markdown(css, unsafe_allow_html=True)
	
st.write('# **FitController**')	
	
block0 = st.empty()
block1 = st.empty()
block2 = st.empty()

user = block0.text_input('Nome de Usuário:')
senha = block1.text_input('Senha:', type='password')
login = block2.button('Entrar')

st.session_state['user'] = user

st.session_state['pwd'] = senha

academia = Academia(username=st.session_state['user'], password=st.session_state['pwd'])

try:

	if login:
	
		st.session_state['auth'], st.session_state['dep'], st.session_state['name'] = academia.auth()
	
		block0.empty()
		block1.empty()
		block2.empty()
	
except: 

	st.warning('Insira as credenciais corretamente.')

if 'auth' not in st.session_state:

	st.empty()

elif st.session_state['auth']:

	block0.empty()
	block1.empty()
	block2.empty()
	
	sair = st.button(label = 'Sair')

	if sair:

		st.session_state['auth'] = None

	st.header('Evolução de Peso')

	dados = academia.evo()

	graph = alt.Chart(dados).mark_area(
		line={'color': 'blue'},
		color=alt.Gradient(
			gradient='linear',
			stops=[
				alt.GradientStop(color='white', offset=0),
				alt.GradientStop(color='blue', offset=1)
				],
			x1=1,
			x2=1,
			y1=1,
			y2=0
		)).encode(
		alt.X('date:T'),
		alt.Y('weight:Q')
	)	

	st.altair_chart(graph, use_container_width=True)

	st.header('Cadastrar Novo Treino')

	new_train = {
		'name': st.text_input('Nome do Treino'),
		'type': st.selectbox('Tipo de Treino', options=['Superior', 'Inferior', 'Neutro'])
	}

	register_train = st.button(label = 'Cadastrar Treino')

	if register_train:

		try:

			academia.train(train = new_train)

			st.success('Treino cadastrado com sucesso!')

		except:

			st.error('Erro ao tentar cadastrar treino!')

	st.header('Cadastrar Programa de Treino')	

	data = {
		'name': st.text_input('Nome do programa'),
		'date': st.date_input('Início do Programa').strftime('%d/%m/%Y'),
		'type': st.selectbox('Tipo da Ficha (Treino)', options=['A', 'B']),
		'ativities': st.multiselect('Atividades do Programa', options = academia.train_list())
	}

	register_program = st.button('Cadastrar Programa')

	if register_program:

		try:

			academia.program(data = data)

			st.success('Programa cadastrado com sucesso!')

		except:

			st.error('Erro ao tentar cadastrar programa!')

	st.header('Ver Detalhes do Programa')

	prog = st.selectbox('Lista de Programas', options = academia.see_program())

	ver = st.button('Ver Programa')

	if ver:

		st.table(academia.data_program(program = prog))

	st.header('Acompanhamento')

	evo = {
		'weight': st.number_input('Peso', min_value=0.0),
		'date': st.date_input('Data').strftime('%d/%m/%Y'),
		'ativities': st.multiselect('Atividades', options = academia.train_list()),
		'diary': st.text_area('Diário')
	}

	register_day = st.button('Cadastrar Diário')

	if register_day:

		try:

			academia.evolution(evo = evo)

			st.success('Diário cadastrado com sucesso!')

		except:

			st.error('Erro ao tentar cadastrar diário!')

	st.write('#### Meu Diário de Treinos')

	dados['date'] = [i.strftime('%d/%m/%Y') for i in dados['date']]

	st.table(dados)

elif st.session_state['auth'] == False:

	st.error('Credenciais incorretas.')