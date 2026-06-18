import streamlit as st
import yt_dlp
import os
import glob

# Configuração da página com o seu novo nome
st.set_page_config(page_title="LucasNamikaze Downloads", page_icon="🎵")

# Título principal personalizado
st.title("🎵 LucasNamikaze Downloads")
st.write("Cole o link de um canal ou playlist para listar os vídeos e baixar em MP3 ou MP4 manualmente.")

# Input da URL do Canal ou Playlist
channel_url = st.text_input("Cole a URL do Canal ou Playlist aqui:", placeholder="https://www.youtube.com/@NomeDoCanal")

# Função para listar os vídeos do canal (sem baixar os vídeos em si)
@st.cache_data(show_spinner="Carregando lista de vídeos do canal... (Isso pode demorar um pouco)")
def get_channel_videos(url):
    ydl_opts = {
        'extract_flat': 'in_playlist',  # Extrai apenas os metadados rápidos, não o vídeo
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                # Retorna uma lista de dicionários com título e url de cada vídeo
                return [(entry.get('title'), f"https://www.youtube.com/watch?v={entry.get('url')}") 
                        for entry in info['entries'] if entry]
            return []
        except Exception as e:
            st.error(f"Erro ao ler o canal: {e}")
            return []

if channel_url:
    videos = get_channel_videos(channel_url)
    
    if videos:
        st.success(f"Encontrados {len(videos)} vídeos neste canal/playlist!")
        
        # Cria um dicionário para o selectbox exibir o título mas sabermos a URL
        video_dict = {title: url for title, url in videos if title}
        
        # Menu de seleção para o usuário escolher a música manualmente
        selected_title = st.selectbox("Escolha o vídeo/música que deseja baixar:", list(video_dict.keys()))
        selected_url = video_dict[selected_title]
        
        st.write(f"**Selecionado:** [{selected_title}]({selected_url})")
        
        # Opção de formato: MP3 ou MP4
        format_choice = st.radio("Selecione o formato de saída:", ("MP3 (Apenas Áudio)", "MP4 (Vídeo com Som)"))
        
        # Botão para iniciar o download
        if st.button("Processar e Gerar Arquivo"):
            with st.spinner("Baixando e convertendo... Por favor, aguarde."):
                
                # Limpa arquivos antigos para evitar conflito de espaço ou download errado
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
                    # Para MP4 garantindo vídeo + áudio juntos e convertendo para mp4 se necessário
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
                    
                    # O yt-dlp pode mudar a extensão real dependendo do merge
                    actual_file = glob.glob(f"downloaded_file.{file_ext}")
                    if not actual_file and file_ext == "mp4":
                        actual_file = glob.glob("downloaded_file.mkv") # Fallback caso o ffmpeg junte em mkv
                    
                    if actual_file:
                        target_file = actual_file[0]
                        final_ext = target_file.split(".")[-1]
                        
                        with open(target_file, "rb") as file:
                            st.success(f"Pronto! Download concluído: **{selected_title}**")
                            st.download_button(
                                label=f"📥 Salvar arquivo .{final_ext.upper()}",
                                data=file,
                                file_name=f"{selected_title}.{final_ext}",
                                mime=mime_type
                            )
                    else:
                        st.error("Erro ao localizar o arquivo baixado no servidor.")
                except Exception as e:
                    st.error(f"Erro no processamento: {e}")
    else:
        st.warning("Nenhum vídeo encontrado ou a URL é inválida. Certifique-se de usar o link público correto.")
