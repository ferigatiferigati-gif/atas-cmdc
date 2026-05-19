import streamlit as st
import os
from google import genai

# =====================================================================
# CONFIGURAÇÃO DE SEGURANÇA: Coloque sua chave do Gemini aqui dentro.
CHAVE_API_AUTOMACAO = "AIzaSyCjFZON18OH5dnjcPz6gTuBL9199OJxnGY"
# =====================================================================

# Configuração visual e título da aba
st.set_page_config(
    page_title="Sistema de Atas CMDCA - Ouro Preto",
    page_icon="🏢",
    layout="centered"
)

# --- MENU LATERAL DE SUPORTE E COLARES (Para a Heloísa) ---
with st.sidebar:
    st.markdown("### 🌟 Central de Ajuda da Heloísa")
    st.write("Olá, Heloísa! Se tiver qualquer dúvida, veja as respostas rápidas abaixo:")
    
    with st.expander("❓ Como o sistema funciona?"):
        st.write("Você envia o áudio da reunião, a nossa Inteligência Artificial 'escuta' tudo o que foi falado e redige a ata diretamente no modelo oficial de Ouro Preto, convertendo tudo para um arquivo do Word.")
        
    with st.expander("❓ Qual o tamanho máximo do áudio?"):
        st.write("O sistema aguenta áudios bem longos, de até 5 horas de duração de uma só vez.")
        
    with st.expander("❓ O botão de gerar sumiu ou deu erro?"):
        st.write("Isso geralmente acontece se a internet oscilar durante o envio do áudio. Sugerimos recarregar a página (apertando F5) e tentar enviar o áudio novamente.")
        
    with st.expander("⚠️ Mensagem de erro vermelha?"):
        st.write("Se aparecer algum aviso em vermelho na tela, tire um print ou copie o texto e envie para o responsável técnico ajustar a Chave de Acesso.")

    st.markdown("---")
    st.caption("Sistema desenvolvido com carinho para o CMDCA de Ouro Preto/MG.")

# --- CORPO PRINCIPAL DO SISTEMA ---
st.title("🏢 Sistema de Atas - CMDCA Ouro Preto")
st.subheader("Olá, Heloísa! Seja bem-vinda ao seu assistente digital.")
st.write("Este espaço foi feito para facilitar o seu trabalho. Aqui você transforma as gravações do Conselho em Atas Oficiais para o Word com apenas alguns cliques.")
st.markdown("---")

# Passo 1: Envio do arquivo
st.markdown("#### **Passo 1:** Escolha o arquivo de áudio da reunião")
arquivo_audio = st.file_uploader(
    label="Clique no botão abaixo ou arraste a gravação para cá:", 
    type=["mp3", "wav", "m4a", "aac"]
)

# Só avança se a Heloísa colocar o áudio
if arquivo_audio:
    st.markdown("---")
    st.markdown("#### **Passo 2:** Iniciar a criação do documento")
    st.write("Excelente, Heloísa! O áudio já foi carregado no sistema. Agora é só clicar no botão azul abaixo.")
    
    # Botão de ação
    if st.button("🪄 HELOÍSA, CLIQUE AQUI PARA GERAR A ATA", type="primary", use_container_width=True):
        try:
            client = genai.Client(api_key=CHAVE_API_AUTOMACAO)
            
            # Mensagens carinhosas durante o carregamento longo
            with st.spinner("⏳ Heloísa, estou lendo o arquivo de áudio... Por favor, aguarde um momento."):
                temp_filename = f"temp_{arquivo_audio.name}"
                with open(temp_filename, "wb") as f:
                    f.write(arquivo_audio.getbuffer())
                
                audio_file = client.files.upload(file=temp_filename)
            
            with st.spinner("🤖 Estou escutando a reunião e redigindo a ata no padrão de Ouro Preto... Como o áudio é longo, isso pode demorar de 2 a 5 minutos. Pode tomar um café, só não feche esta página! 😉"):
                
                prompt_ouro_preto = """
                Você é o Secretário Executivo do Conselho Municipal dos Direitos da Criança e do Adolescente (CMDCA) de Ouro Preto - MG. 
                Sua tarefa é ouvir o áudio fornecido e redigir a ATA OFICIAL DE REUNIÃO ORDINÁRIA OU EXTRAORDINÁRIA, adotando estritamente o formato padrão exigido para publicação no Diário Oficial do Município de Ouro Preto.
                
                REGRAS RÍGIDAS DE FORMATAÇÃO E ESTILO (PADRÃO OURO PRETO):
                1. Não quero transcrição integral de bate-papo. O texto deve ser sintético, formal, corrido e impessoal (terceira pessoa).
                2. O documento deve ter um tamanho equilibrado (equivalente a 2 a 4 páginas no Word). Elimine informalidades.
                3. Abertura por extenso: Comece rigorosamente no padrão formal: "Ao(s) [número por extenso] dias do mês de [mês] de [ano], às [horas] horas, reuniu-se..."
                4. Identifique o local ou a plataforma (ex: "de forma virtual pelo Google Meet" ou "na Casa dos Conselhos Municipais de Ouro Preto").
                5. Registro de Presença: Liste de forma organizada quem estava presente (identificando se representam o Poder Público ou Sociedade Civil).
                6. Corpo do Texto (Pauta e Discussão): Descreva os pontos debatidos em parágrafos justificados contínuos. Use frases formais como: "Passando para o primeiro ponto da pauta...", "Colocado em discussão...", "A conselheira [Nome] pediu a palavra...".
                7. Votações e Deliberações: Registre com precisão o que foi deliberado e o resultado da votação (Aprovado por unanimidade, aprovado por maioria, ou rejeitado). Se houver resoluções aprovadas, cite explicitamente.
                8. Fechamento Oficial: Termine obrigatoriamente com a fórmula: "Não havendo nada mais a tratar, eu, [Nome], lavrei a presente Ata que, após lida e aprovada, será assinada por mim e pela Presidência. Ouro Preto, [Data por extenso]."
                
                Gere o texto pronto, limpo, sem marcas de markdown (sem asteriscos de negrito, pois o programa cuidará disso).
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[audio_file, prompt_ouro_preto]
                )
                
                texto_ata = response.text
            
            # Aqui, para simplificar o deploy na nuvem e evitar erros de permissão de pasta, 
            # vamos disponibilizar o arquivo de texto formatado estruturado, que abre direto no Word perfeitamente.
            st.success("🎉 Parabéns, Heloísa! Sua ata oficial foi gerada com sucesso.")
            st.markdown("---")
            
            st.markdown("#### **Passo 3:** Baixar o documento")
            st.write("Clique no botão verde abaixo para salvar o arquivo no seu computador. Depois, é só abri-lo com o Word para revisar e imprimir.")
            
            st.download_button(
                label="📥 CLIQUE AQUI PARA SALVAR A ATA NO COMPUTADOR",
                data=texto_ata,
                file_name="Ata_Oficial_CMDCA_Ouro_Preto.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            with st.expander("Clique aqui se quiser dar uma olhada no texto antes de baixar"):
                st.text(texto_ata)
                
            # Limpeza automática
            client.files.delete(name=audio_file.name)
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
                
        except Exception as e:
            st.error(f"Oi, Heloísa. Ocorreu um probleminha no processamento. Por favor, tente enviar o áudio de novo. Se persistir, avise o suporte. Detalhe técnico: {e}")
            if 'temp_filename' in locals() and os.path.exists(temp_filename):
                os.remove(temp_filename)
else:
    st.info("Heloísa, estou aguardando você escolher o arquivo de áudio no Passo 1 para começarmos! 😊")