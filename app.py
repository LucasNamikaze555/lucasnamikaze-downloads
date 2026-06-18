import streamlit as st
import yt_dlp
import os
import glob

# Configuração da página com tema escuro e título personalizado
st.set_page_config(
    page_title="LucasNamikaze Downloads", 
    page_icon="🎵",
    layout="wide"
)

# Estilização CSS para transformar o Streamlit no tema escuro do Spotify
st.markdown("""
    <style>
    /* Fundo geral da aplicação */
    .stApp {
        background-color: #121212;
        color: #FFFFFF;
    }
    
    /* Customização dos inputs de texto */
    div[data-baseweb="input"] {
        background-color: #242424 !important;
        border-radius: 50px !important;
        border: 1px solid transparent !important;
        padding: 4px 12px !important;
    }
    div[data-baseweb="input"] input {
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif;
    }
    div[data-baseweb="input"]:focus-within {
        border: 1px solid #1DB954 !important;
    }
    
    /* Títulos e textos */
    h1 {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-family: 'Montserrat', sans-serif;
        letter-spacing: -1px;
    }
    
    /* Botões do Streamlit no estilo Spotify */
    div.stButton > button {
        background-color: #1DB954 !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 12px 34px !important;
        transition: transform 0.2s, background-color 0.2s;
        text-transform: uppercase;
        font-size: 13px;
        letter-spacing: 1px;
    }
    div.stButton > button:hover {
        background-color: #1ED760 !important;
        transform: scale(1.04);
        color: #FFFFFF !important;
    }
    div.stButton > button:active {
        transform: scale(0.98);
    }
    
    /* Customização do Selectbox e Radio buttons */
    div[data-baseweb="select"] {
        background-color: #242424 !important;
        border-radius: 8px !important;
    }
    div[class*="stRadio"] label {
        color: #B3B3B3 !important;
    }
    div[class*="stRadio"] label:hover {
        color: #FFFFFF !important;
    }
    
    /* Esconder o menu padrão do Streamlit para parecer um app nativo */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background-color: transparent !important;}
    
    /* Card de exibição */
    .spotify-card {
        background: linear-gradient(transparent, rgba(0, 0, 0, 0.71));
        background-color: #181818;
        padding: 24px;
        border-radius: 8px;
        margin-bottom: 20px;
        border: 1px solid #282828;
    }
    </style>
""", unsafe_allow_html=True)

# Layout em colunas simula a barra lateral esquerda e o conteúdo principal
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown('<div style="text-align: center; padding: 20px 0;"><h1 style="color: #1DB954 !important; font-size: 28px;">🟢 LucasNamikaze</h1><p style="color: #B3B3B3; font-size: 14px;">Music & Video Downloader</p></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p style='color: #B3B3B3; font-weight: bold; font-size: 12px; letter-spacing: 1px; text-transform: uppercase;'>Navegação</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FFFFFF; font-weight: bold; font-size: 16px; margin-bottom: 5px;'>🏠 Início</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #B3B3B3; font-size: 16px; margin-bottom: 5px;'>🔍 Biblioteca</p>", unsafe_allow_html=True)

with col2:
    st.title("LucasNamikaze Downloads")
    st.markdown("<p style='color: #B3B3B3; margin-top: -15px;'>Transforme canais e playlists em seus formatos favoritos de áudio e vídeo.</p>", unsafe_allow_html=True)
    
    # Área principal de Input (Barra de Pesquisa do Spotify)
    channel_url = st.text_input("", placeholder="Cole a URL do Canal ou Playlist do YouTube aqui...")

    # Função para listar os vídeos do canal (sem baixar os vídeos em si)
    @st.cache_data(show_spinner="A aceder ao catálogo do canal... Por favor, aguarde.")
    def get_channel_videos(url):
        ydl_opts = {
            'extract_flat': 'in_playlist',
            'skip_download': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info:
                    return [(entry.get('title'), f"https://www.youtube.com/watch?v={entry.get('url')}") 
                            for entry in info['entries'] if entry]
                return []
            except Exception as e:
                st.error(f"Erro ao ler o canal: {e}")
                return []

    if channel_url:
        videos = get_channel_videos(channel_url)
        
        if videos:
            st.markdown(f"<p style='color: #1DB954; font-weight: bold;'>✓ Encontradas {len(videos)} faixas disponíveis para download.</p>", unsafe_allow_html=True)
            
            video_dict = {title: url for title, url in videos if title}
            
            # Caixa de seleção estilizada
            selected_title = st.selectbox("Selecione a faixa que deseja processar:", list(video_dict.keys()))
            selected_url = video_dict[selected_title]
            
            # Card de visualização do item selecionado
            st.markdown(f"""
                <div class="spotify-card">
                    <p style="color: #B3B3B3; text-transform: uppercase; font-size: 11px; font-weight: bold; letter-spacing: 1px; margin-bottom: 5px;">Faixa Selecionada</p>
