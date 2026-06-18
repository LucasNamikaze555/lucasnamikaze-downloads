import streamlit as st
import yt_dlp
import os
import glob
import zipfile
import shutil

# Configuração da página com tema escuro e título personalizado
st.set_page_config(
    page_title="LucasNamikaze Downloads", 
    page_icon="🎵",
    layout="wide"
)

# Estilização CSS para transformar o Streamlit no tema escuro do Spotify
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #FFFFFF; }
    div[data-baseweb="input"] { background-color: #242424 !important; border-radius: 50px !important; border: 1px solid transparent !important; padding: 4px 12px !important; }
    div[data-baseweb="input"] input { color: #FFFFFF !important; font-family: 'Montserrat', sans-serif; }
    div[data-baseweb="input"]:focus-within { border: 1px solid #1DB954 !important; }
    h1 { color: #FFFFFF !important; font-weight: 800 !important; font-family: 'Montserrat', sans-serif; letter-spacing: -1px; }
    div.stButton > button { background-color: #1DB954 !important; color: #FFFFFF !important; font-weight: bold !important; border-radius: 50px !important; border: none !important; padding: 12px 34px !important; transition: transform 0.2s, background-color 0.2s; text-transform: uppercase; font-size: 13px; letter-spacing: 1px; }
    div.stButton > button:hover { background-color: #1ED760 !important; transform: scale(1.04); color: #FFFFFF !important; }
    div[class*="stRadio"] label { color: #B3B3B3 !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {background-color: transparent !important;}
    .spotify-card { background-color: #181818; padding: 24px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #282828; }
    </style>
""", unsafe_allow_html=True)

# Definição de cabeçalhos padrão para camuflar o robô
HEADERS_PADRAO = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Sec-Fetch-Mode': 'navigate',
}

col1, col2 = st.columns([1, 3])

with col1:
    st.markdown('<div style="text-align: center; padding: 20px 0;"><h1 style="color: #1DB954 !important; font-size: 28px;">🟢 LucasNamikaze</h1><p style="color: #B3B3B3; font-size: 14px;">Music & Video Downloader</p></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p style='color: #B3B3B3; font-weight: bold; font-size: 12px; letter-spacing: 1px; text-transform: uppercase;'>Navegação</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FFFFFF; font-weight: bold; font-size: 16px; margin-bottom: 5px;'>🏠 Início</p>", unsafe_allow_html=True)

with col2:
    st.title("LucasNamikaze Downloads")
    st.markdown("<p style='color: #B3B3B3; margin-top: -15px;'>Fila Automática: Baixe canais inteiros e receba tudo compactado em um único arquivo ZIP.</p>", unsafe_allow_html=True)
    
    channel_url = st.text_input("", placeholder="Cole a URL do Canal ou Playlist do YouTube aqui...")

    @st.cache_data(show_spinner="Mapeando faixas do canal... Por favor, aguarde.")
    def get_channel_videos(url):
        ydl_opts = {
            'extract_flat': 'in_playlist',
            'skip_download': True,
            'http_headers': HEADERS_PADRAO,
            'no_check_certificate': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info:
                    lista_videos = []
                    for entry in info['entries']:
                        if entry:
                            title = entry.get('title')
                            video_url = entry.get('url')
                            
                            if video_url:
                                if "youtube.com" not in video_url and "youtu.be" not in video_url:
                                    video_url = f"https://www.youtube.com/watch?v={video_url}"
                                
                                lista_videos.append((title, video_url))
                    return lista_videos
                return []
            except Exception as e:
                st.error(f"Erro ao acessar o canal: {e}")
                return []

    if channel_url:
        videos = get_channel_videos(channel_url)
        
        if videos:
            st.markdown(f"<p style='color: #1DB954; font-weight: bold;'>✓ Mapeamento concluído: {len(videos)} faixas prontas para a fila.</p>", unsafe_allow_html=True)
            
            format_choice = st.radio("Selecione o formato de saída:", ("MP3 (Apenas Áudio)", "MP4 (Vídeo com Som)"), horizontal=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Botão único para disparar a automação
            if st.button("🚀 INICIAR FILA AUTOMÁTICA"):
                
                # Cria ou limpa diretórios de trabalho temporários
                pasta_download = "lucasnamikaze_queue"
                if os.path.exists(pasta_download):
                    shutil.rmtree(pasta_download)
                os.makedirs(pasta_download)
                
                arquivo_zip_final = "lucasnamikaze_pack.zip"
                if os.path.exists(arquivo_zip_final):
                    os.remove(arquivo_zip_final)
                
                total_itens = len(videos)
                progresso_barra = st.progress(0)
                status_texto = st.empty()
                
                # Executa a fila de forma totalmente automatizada em loop sequencial
                for index, (title, url) in enumerate(videos):
                    status_texto.markdown(f"**Processando ({index + 1}/{total_itens}):** *{title}*")
                    progresso_barra.progress((index + 1) / total_itens)
                    
                    # Normaliza o nome do arquivo para evitar caracteres ilegais
                    clean_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
                    out_tmpl = f"{pasta_download}/{clean_title}.%(ext)s"
                    
                    # Configuração base contra bloqueios 403
                    ydl_base_opts = {
                        'outtmpl': out_tmpl,
                        'noplaylist': True,
                        'quiet': True,
                        'http_headers': HEADERS_PADRAO,
                        'no_check_certificate': True,
                        'rm_cached_metadata': True, # Limpa o cache interno do yt-dlp por vídeo
                    }
                    
                    if format_choice == "MP3 (Apenas Áudio)":
                        ydl_base_opts.update({
                            'format': 'bestaudio/best',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                        })
                    else:
                        ydl_base_opts.update({
                            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                            'merge_output_format': 'mp4',
                        })
                    
                    try:
                        with yt_dlp.YoutubeDL(ydl_base_opts) as ydl:
                            ydl.download([url])
                    except Exception as e:
                        st.warning(f"Aviso: Falha ao converter a faixa '{title}'. Pulando para a próxima... Erro: {e}")
                
                status_texto.markdown("**📦 Empacotando arquivos no ZIP...**")
                
                # Compacta todos os arquivos processados sequencialmente na pasta
                arquivos_baixados = glob.glob(f"{pasta_download}/*")
                if arquivos_baixados:
                    with zipfile.ZipFile(arquivo_zip_final, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for arquivo in arquivos_baixados:
                            zipf.write(arquivo, os.path.basename(arquivo))
                    
                    status_texto.markdown("<p style='color: #1DB954; font-weight: bold;'>✓ Fila concluída com sucesso! Seu pacote está pronto para download.</p>", unsafe_allow_html=True)
                    
                    # Disponibiliza o botão único para baixar o ZIP gerado
                    with open(arquivo_zip_final, "rb") as f:
                        st.download_button(
                            label="📥 BAIXAR PACOTE COMPLETO (.ZIP)",
                            data=f,
                            file_name="lucasnamikaze_pack.zip",
                            mime="application/zip"
                        )
                    
                    # Limpeza pós-processamento da pasta para liberar espaço no servidor
                    shutil.rmtree(pasta_download)
                else:
                    st.error("Erro: Nenhum arquivo pôde ser convertido com sucesso para gerar o pacote.")
        else:
            st.warning("Nenhum conteúdo localizado. Certifique-se de usar a URL correta do canal ou playlist.")
