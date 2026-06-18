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

# Layout em colunas simula a barra lateral e o conteúdo principal
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
            
            # Card de visualização estruturado sem usar f-string tripla combinada com chaves CSS
            card_html = f"""
                <div class="spotify-card">
                    <p style="color: #B3B3B3; text-transform: uppercase; font-size: 11px; font-weight: bold; letter-spacing: 1px; margin-bottom: 5px;">Faixa Selecionada</p>
                    <h3 style="color: #FFFFFF; margin: 0; font-size: 20px;">{selected_title}</h3>
                    <p style="color: #1DB954; font-size: 14px; margin-top: 5px;">Disponível para conversão imediata</p>
                </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Escolha do formato (Opções horizontais simulam botões de filtro)
            format_choice = st.radio("Escolha o formato de saída:", ("MP3 (Apenas Áudio)", "MP4 (Vídeo com Som)"), horizontal=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Botão para iniciar o download (Estilo botão de Play do Spotify)
            if st.button("Iniciar Conversão"):
                with st.spinner("A processar streams de áudio e vídeo..."):
                    
                    for f in glob.glob("downloaded_file.*"):
                        try:
                            os.remove(f)
                        except:
                            pass
                    
                    if format_choice == "MP3 (Apenas Áudio)":
                        ydl_opts = {
                            'format': 'bestaudio/best',
                            'outtmpl': 'downloaded_file.%(ext)s',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                            'noplaylist': True,
                        }
                        file_ext = "mp3"
                        mime_type = "audio/mpeg"
                    else:
                        ydl_opts = {
                            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                            'outtmpl': 'downloaded_file.%(ext)s',
                            'merge_output_format': 'mp4',
                            'noplaylist': True,
                        }
                        file_ext = "mp4"
                        mime_type = "video/mp4"
                    
                    try:
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([selected_url])
                        
                        actual_file = glob.glob(f"downloaded_file.{file_ext}")
                        if not actual_file and file_ext == "mp4":
                            actual_file = glob.glob("downloaded_file.mkv")
                        
                        if actual_file:
                            target_file = actual_file[0]
                            final_ext = target_file.split(".")[-1]
                            
                            with open(target_file, "rb") as file:
                                st.markdown("<br>", unsafe_allow_html=True)
                                st.download_button(
                                    label=f"📥 Baixar .{final_ext.upper()}",
                                    data=file,
                                    file_name=f"{selected_title}.{final_ext}",
                                    mime=mime_type
                                )
                        else:
                            st.error("Não foi possível localizar o ficheiro convertido.")
                    except Exception as e:
                        st.error(f"Erro no processamento: {e}")
        else:
            st.warning("Nenhum conteúdo foi localizado nesta URL. Verifique se o canal é público.")
