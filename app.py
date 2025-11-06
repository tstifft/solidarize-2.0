import streamlit as st # type: ignore
import pandas as pd
import altair as alt
import streamlit_antd_components as sac




def exibir_card_progresso(cidade,total_arrecadado,meta):
    porcentagem = (total_arrecadado / meta) * 100
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin-bottom: 0px;">{cidade}</h3>
                    <p style="font-size: 1.2em; margin-top: 0px;">{total_arrecadado:,} kg arrecadados</p>
                </div>
                <span style='
                    text-align: right; 
                    color: rgb(0, 153, 255) !important; 
                    font-size: 2.5em; 
                    font-weight: bold;
                '>
                    {porcentagem:.0f}%
                </span>
            </div>
            """.replace(",", "."), 
            unsafe_allow_html=True
        )
            
        # Barra de progresso. O valor deve ser um float entre 0.0 e 1.0
        st.progress(total_arrecadado/meta)




st.set_page_config(
    page_title="Solidarize",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)




st.markdown("""
        <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
    
        header {visibility: hidden;}
        [data-testid="stHeader"] {display: none;}
        [data-testid="stToolbar"] {display: none;}
        [data-testid="stDecoration"] {display: none;}
        [data-testid="stStatusWidget"] {display: none;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
            
        /* Remove padding padrão do Streamlit */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 8rem;
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: 100%;
        }
        
        /* Remove header padrão do Streamlit */
        header {
            visibility: hidden;
            height: 0;
        }
        
        /* Remove footer padrão do Streamlit */
        footer {
            visibility: hidden;
            height: 0;
        }
        
        /* Esconde o menu hamburguer */
        #MainMenu {
            visibility: hidden;
        }
        
        /* Remove margin do stApp */
        .stApp {
            margin: 0;
            padding: 0;
        }
        
        /* Esconde qualquer container extra no topo */
        section[data-testid="stVerticalBlock"] > div:has(div[data-testid="stVerticalBlock"]) {
            gap: 0;
        }


        .st-ar{
             height: 3vh;
            border-radius: 15px; 
        }

        </style>
        """, unsafe_allow_html=True)






st.markdown(f"<h1 style='text-align: left; color: #028BF9; font-size: 6vmax'>Solidarize 2025</h1>", unsafe_allow_html=True)





btn = sac.buttons([
    sac.ButtonsItem(label='Home'),
    sac.ButtonsItem(label='Acompanhe'),
    sac.ButtonsItem(label='Participe'),
    sac.ButtonsItem(label='Prioridades'),
    # sac.ButtonsItem(icon='apple'),
    # sac.ButtonsItem(label='google', icon='google', color='#25C3B0'),
    # sac.ButtonsItem(label='wechat', icon='wechat'),
    # sac.ButtonsItem(label='disabled', disabled=True),
    # sac.ButtonsItem(label='link', icon='share-fill', href='https://ant.design/components/button'),
], label='', align='center', color='blue', use_container_width=True ,variant='text', size='sm') #radius='lg'

# st.write(f'The selected button label is: {btn}')

match btn:
    case 'Home':
        entradas = pd.read_csv(st.secrets.gsheet.entradas).sort_values(by=['Quantidade'],ascending=False)

        # Resumo da campanha
        # st.header('Saiba mais')
        st.write("""
        A **Solidarize** é uma campanha anual de arrecadação de alimentos, dedicada a ajudar pessoas em situação de dificuldade na comunidade.
        """)

        st.subheader("Juntos já arrecadamos  ...")

        col1,col2 = st.columns(2)
        
        total_kgs = '{0:,}'.format(entradas["Quantidade"].sum()).replace(',','.')   

        tile1 = col1.container(height=200)
        tile1.markdown(f"<h1 style='text-align: center; color: #028BF9; font-size:65px'>{total_kgs}</h1>", unsafe_allow_html=True)
        ""
        tile1.markdown("<h4 style='text-align: right; color: #028BF9;'>Quantidade (Kgs)</h4>", unsafe_allow_html=True)
    

        total_cestas = '{0:,}'.format(entradas["Cestas"].sum()).replace(',','.')


        tile2 = col2.container(height=200)
        tile2.markdown(f"<h1 style='text-align: center; color: #028BF9; font-size:65px'>{total_cestas}</h1>", unsafe_allow_html=True)
        tile2.markdown("<h4 style='text-align: right; color: #028BF9;'>Cestas Básicas Montadas</h4>", unsafe_allow_html=True)



    case 'Acompanhe':
        """
        ### Nossa meta é ultrapassar os valores arrecadados em 2024
        """
        entradas = pd.read_csv(st.secrets.gsheet.entradas).sort_values(by=['Quantidade'],ascending=False)
        print(entradas)

        for index, row in entradas.iterrows():
            # Você acessa os dados usando o nome da coluna na 'row'
            localidade = row['Localidade']
            quantidade = row['Quantidade']
            cestas = row['Cestas']
            meta = row['Meta']
            exibir_card_progresso(localidade,quantidade,meta)

    case 'Participe':
        """        
        
        Sua participação fará toda a diferença na vida de muitas famílias.

        **Como você pode ajudar:**

        📦 **Doações:** Alimentos não perecíveis.  
        🗓️ **Período:** 08/11/2025  
        📍 **Locais de arrecadação:** 
                
        - Principais Mercados da Cidade  
        - Drive Thru
            - **Camaquã**: Av. Jose Loureiro da Silva, 787 - Carvalho Bastos, Camaquã - RS, 96784-058
            - **Cristal**: Rua Pedro Osório, 109 - Centro, Cristal - RS, 96195-000
            - **Tapes**: Av. Borges de Medeiros, 156, Tapes - RS, 96760-000
            
                

        Juntos podemos :blue[mais !] 
        
        
        """
    case 'Prioridades':
        ############## ITENS PRIORITARIOS
        st.header("Itens Prioritários")
        necessidades = pd.read_csv(st.secrets.gsheet.necessidades, index_col='Localidade')

        # "Esses são os itens prioritários em cada localidade"
        ":red[*Isso nos ajuda a termos uma distribuição adqueada para montagem das cestas básicas*]"
        
        locais = necessidades.index.unique()
        
        for localidade in locais:
            # Imprime o nome da localidade (o cabeçalho)
        
            st.subheader(f"\n{localidade}")

            # Filtra o DataFrame original para obter apenas as linhas dessa localidade
            # .loc[] é usado para acessar por índice
            produtos_da_localidade = necessidades.loc[localidade, 'Produto']

            # Se houver apenas 1 produto, ele não vem como uma Series.
            # Transformamos em lista para garantir que sempre podemos iterar.
            if isinstance(produtos_da_localidade, pd.Series):
                lista_produtos = produtos_da_localidade.tolist()
            else:
                # Caso seja um único valor (string)
                lista_produtos = [produtos_da_localidade]

            # st.write(lista_produtos)
            for prod in lista_produtos:
                st.markdown(f"""\t- {prod}""")
            






