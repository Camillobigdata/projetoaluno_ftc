import streamlit as st

st.set_page_config(
    page_title = "Home",
    page_icon = "📈")



#st.sidebar.image('pages/Zomato_logo.png', width = 120)

st.sidebar.image('pages/Zomato_logo.png', width=100, )
st.sidebar.markdown('# Fartura Restaurantes')
st.sidebar.markdown('## Trazendo a melhor experiência culinária!')
st.sidebar.markdown("""---""")

st.write('# Fartura Restaurantes Dashboard')

st.markdown("""
            Growth Dashboard foi construído para acompanhar as métricas de crescimento por países, cidades e tipo de culinária.
            ### Como utilizar o Dashboard?
            - Visão Geral:
                - Acompanhar a visão geral do Top Restaurantes
                - Localização do Restaurantes no Mapa
            - Visão Países: 
                - Acompanhamento da quantidade de restaurantes por país.
                - Quantidade de Cidades por País
                - Acompanhar as avaliações dos restaurantes por país
            - Visão Cidades:
                - Top 1o Cidades com mais restaurantes registrados
                - acompanhamento de restaurantes por nota
                - Top 10 culinárias distintas
            - Visão Culinárias:
                - Culinárias mais bem avaliadas
                - Top 20 restaurantes mais bem avaliados
                - 10 tipos de culinária com maior número de restaurantes
                - Top 20 melhores e piores restaurantes
            ### Ask for help
                - Time de Data Science no Instagram
                    - @Camillo Lepore
            """)