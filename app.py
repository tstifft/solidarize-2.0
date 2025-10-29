import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import altair as alt

#Importando as paginas
import pages.home as home

# ==============================
# ⚙ CONFIGURAÇÕES INICIAIS
# ==============================
st.set_page_config(
    page_title="Solidarize",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Inicializa o estado da sessão
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = 'Home'


# ==============================
# 🎨 CSS PERSONALIZADO
# ==============================

st.markdown("""
    <link href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap' rel='stylesheet'>
    <style>
        * {
	font-family: 'Inter', sans-serif;
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
            
        div[data-testid="stVerticalBlock"]{
            width: 100% !important;
        }
        .st-key-bottom-menu {
            /* height: 10vh !important; */
            position: fixed !important;
            bottom: 0;
            left: 0;
            width: 100%;
            margin: 0 !important;
            padding: 10px 0 !important;
            background-color: white;
            border-top: 1px solid #e0e0e0;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
            z-index:  999;   
            
            height: auto !important;      
            min-height: auto !important;  
            padding: 0 !important;
            margin: 0 !important;
        }
        .st-key-bottom-menu > div {
          width: 100%;
        }

            
        .st-key-content-area {
            
        }
            


        /* Garantir que o option_menu não tenha padding/margens extras */
        nav[data-testid="stHorizontalBlock"], nav.st-bt, .css-1d391kg, .css-ocqkz7 {
            padding: 0 !important;
            margin: 0 !important;
        }

   
</style>
""", unsafe_allow_html=True)




# ==============================
# 📄 CONTEÚDO DAS PÁGINAS
# ==============================
with st.container(key='content-area'):    
    if st.session_state.selected_menu == "Home":
        home.render()

    elif st.session_state.selected_menu == "Doações":
        st.title("📦 Registro de Doações")
        with st.form("form_doacao"):
            nome = st.text_input("Nome do doador")
            valor = st.number_input("Valor da doação (R$)", min_value=0.0, step=10.0)
            enviar = st.form_submit_button("Registrar")
            if enviar:
                st.success(f"✅ {nome} doou R$ {valor:.2f}")

    elif st.session_state.selected_menu == "Relatórios":
        st.title("📈 Relatórios")
        entradas = pd.read_csv(st.secrets.gsheet.entradas).sort_values(by=['Quantidade'],ascending=False)
        st.header("Juntos já arrecadamos  ...")

        ""
        col1,col2 = st.columns(2)
        
        total_kgs = '{0:,}'.format(entradas["Quantidade"].sum()).replace(',','.')
        
        
        tile1 = col1.container(height=200)
        tile1.markdown(f"<h1 style='text-align: center; color: #028BF9; font-size:70px'>{total_kgs}</h1>", unsafe_allow_html=True)
        ""
        tile1.markdown("<h3 style='text-align: right; color: #028BF9;'>Quantidade (Kgs)</h3>", unsafe_allow_html=True)
    

        total_cestas = '{0:,}'.format(entradas["Cestas"].sum()).replace(',','.')


        tile2 = col2.container(height=200)
        tile2.markdown(f"<h1 style='text-align: center; color: #028BF9; font-size:70px'>{total_cestas}</h1>", unsafe_allow_html=True)
        tile2.markdown("<h3 style='text-align: right; color: #028BF9;'>Cestas Básicas Montadas</h3>", unsafe_allow_html=True)

        "veja por localidade aqui 	:point_down:"
        ""
        ""
        ""
    
        # Gráfico de barras com Altair
        # color='blues'
        chart = alt.Chart(entradas).mark_bar().encode(
            x=alt.X('Localidade:N',axis=alt.Axis(title='') ),
            y=alt.Y('Quantidade:Q',axis=alt.Axis(labels=False, title='Qtd em KGs')),
            tooltip=['Localidade', 'Quantidade']
        ).properties(
            title='Quantidade (kgs) por Localidade'
        )
        st.altair_chart(chart, use_container_width=True)

        chart2 = alt.Chart(entradas).mark_bar().encode(
            x=alt.X('Localidade:N',axis=alt.Axis(title='') ),
            y=alt.Y('Cestas:Q',axis=alt.Axis(labels=False, title='Qtd Cestas')),
            tooltip=['Localidade', 'Cestas']
        ).properties(
            title='Quantidade de Cestas por Localidade'
        )
        st.altair_chart(chart2, use_container_width=True)

    elif st.session_state.selected_menu == "Config":
        st.title("⚙ Configurações")
        st.radio("Tema:", ["Claro", "Escuro"])



# ==============================
# 🧭 MENU INFERIOR (FIXO)
# ==============================
with st.container(key='bottom-menu'):
  selected = option_menu(
      menu_title=None,
      options=["Home", "Doações", "Relatórios", "Config"],
      icons=["house", "box", "bar-chart", "gear"],
      orientation="horizontal",
      default_index=0,
      key="bottom_menu",
      styles={ "container": { "width": "100% !important" } 
          # "container": { "padding": "1 !important", "bottom": "0 !important", "margin": "0 !important", "left":"0 !important"}
      }
      #   # "icon": {"color": "orange", "font-size": "25px"}, 
      #   # "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
      #   # "nav-link-selected": {"background-color": "green"},
      # }
  )
  


# Atualiza o estado quando o menu muda
if selected != st.session_state.selected_menu:
  st.session_state.selected_menu = selected
  st.rerun()
