import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from urllib.parse import quote
import random
import re
import threading
import os
import sys
import logging

def resource_path(relative_path):
    """Obtém o caminho absoluto para recursos empacotados ou não"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

class WhatsAppSender:
    def __init__(self, master):
        self.master = master
        master.title("WhatsApp Sender by Alexandre Bialowas")
        master.geometry("800x600")
        
        # Configuração de log usando resource_path
        log_file = resource_path('whatsapp_sender.log')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.setup_ui()
        self.initialize_variables()
        
        self.log_text.tag_configure('error', foreground='red')
        self.log_text.tag_configure('success', foreground='green')

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.master, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # File selection
        self.file_frame = ttk.LabelFrame(self.main_frame, text="Arquivo", padding="10")
        self.file_frame.pack(fill=tk.X, pady=(0, 10))

        self.btn_selecionar = ttk.Button(
            self.file_frame,
            text="Selecionar Planilha",
            command=self.selecionar_planilha
        )
        self.btn_selecionar.pack(side=tk.LEFT, padx=5)

        self.lbl_planilha = ttk.Label(self.file_frame, text="Nenhuma planilha selecionada")
        self.lbl_planilha.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Controls frame
        self.controls_frame = ttk.Frame(self.main_frame)
        self.controls_frame.pack(fill=tk.X, pady=10)

        self.btn_enviar = ttk.Button(
            self.controls_frame,
            text="Iniciar Envio",
            command=self.iniciar_envio_thread,
            state=tk.DISABLED
        )
        self.btn_enviar.pack(side=tk.LEFT, padx=5)

        self.btn_parar = ttk.Button(
            self.controls_frame,
            text="Parar Envio",
            command=self.parar_envio,
            state=tk.DISABLED
        )
        self.btn_parar.pack(side=tk.LEFT, padx=5)

        # Progress frame
        self.progress_frame = ttk.LabelFrame(self.main_frame, text="Progresso", padding="10")
        self.progress_frame.pack(fill=tk.X, pady=10)

        self.progress = ttk.Progressbar(
            self.progress_frame,
            orient="horizontal",
            length=100,
            mode="determinate"
        )
        self.progress.pack(fill=tk.X)

        self.lbl_status = ttk.Label(self.progress_frame, text="")
        self.lbl_status.pack(fill=tk.X, pady=(5, 0))

        # Log frame
        self.log_frame = ttk.LabelFrame(self.main_frame, text="Log de Envio", padding="10")
        self.log_frame.pack(fill=tk.BOTH, expand=True)

        self.log_text = tk.Text(
            self.log_frame,
            height=15,
            wrap=tk.WORD,
            state=tk.DISABLED
        )

        scrollbar = ttk.Scrollbar(self.log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.log_text.configure(yscrollcommand=scrollbar.set)

    def initialize_variables(self):
        self.caminho_planilha = None
        self.driver = None
        self.processing = False
        self.stop_requested = False
        self.total_mensagens = 0
        self.mensagens_enviadas = 0

    def log(self, mensagem, level='info'):
        """Helper method to output to text box and also to logging."""
        self.log_text.config(state=tk.NORMAL)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        formatted_message = f"[{timestamp}] {mensagem}\n"
        
        tag = None
        if level == 'error':
            tag = 'error'
            logging.error(mensagem)
        elif level == 'success':
            tag = 'success'
            logging.info(mensagem)
        else:
            logging.info(mensagem)
            
        if tag:
            self.log_text.insert(tk.END, formatted_message, tag)
        else:
            self.log_text.insert(tk.END, formatted_message)
            
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.master.update_idletasks()

    def selecionar_planilha(self):
        """
        Opens file dialog to select an Excel file. 
        Uses safer file type specification on macOS (space-separated or tuple).
        """
        try:
            filetypes = [
                ("Planilhas Excel", "*.xlsx *.xls"),
                ("All Files", "*.*")
            ]
            filename = filedialog.askopenfilename(
                title="Selecionar planilha",
                filetypes=filetypes
            )
            
            if filename:
                self.caminho_planilha = filename
                self.lbl_planilha.config(text=os.path.basename(filename))
                self.btn_enviar.config(state=tk.NORMAL)
                self.log(f"Planilha selecionada: {filename}", 'success')
        except Exception as e:
            self.log(f"Erro ao selecionar planilha: {str(e)}", 'error')
            messagebox.showerror("Erro", f"Erro ao selecionar planilha: {str(e)}")

    def formatar_telefone(self, telefone):
        """
        Formata o telefone no padrão adequado (por exemplo, para números brasileiros).
        """
        try:
            if pd.isna(telefone):
                return None
                
            telefone = re.sub(r'\D', '', str(telefone))
            
            if not telefone:
                return None
                
            if len(telefone) == 11:  # Número brasileiro com DDD e 9
                return f"+55{telefone}"
            elif len(telefone) == 10:  # Número brasileiro com DDD sem 9
                return f"+55{telefone[:2]}9{telefone[2:]}"
            elif telefone.startswith('55') and len(telefone) >= 12:
                return f"+{telefone}"
            else:
                return f"+{telefone}"
                
        except Exception as e:
            self.log(f"Erro ao formatar telefone {telefone}: {str(e)}", 'error')
            return None

    def enviar_mensagem(self, driver, telefone, mensagem):
        """
        Envia a mensagem para o telefone indicado usando WhatsApp Web.
        """
        try:
            telefone_formatado = self.formatar_telefone(telefone)
            if not telefone_formatado:
                self.log(f"Número inválido: {telefone}", 'error')
                return False

            url = f"https://web.whatsapp.com/send?phone={telefone_formatado}&text={quote(mensagem)}"
            driver.get(url)
            
            try:
                # Aguarda até o box de mensagem ficar clicável (20 seg)
                input_box = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-tab='10']"))
                )
                time.sleep(2)
                
                input_box.send_keys(Keys.ENTER)
                time.sleep(3)
                
                try:
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((
                            By.CSS_SELECTOR,
                            "span[data-icon='msg-check'], span[data-icon='msg-dblcheck'], "
                            "span[data-testid='msg-check'], span[data-testid='msg-dblcheck']"
                        ))
                    )
                    self.log(f"Mensagem enviada com sucesso para {telefone_formatado}", 'success')
                    return True
                except TimeoutException:
                    self.log(f"Não foi possível confirmar o envio para {telefone_formatado}", 'error')
                    return False
                
            except TimeoutException:
                if "Phone number shared via url is invalid" in driver.page_source:
                    self.log(f"Número inválido: {telefone_formatado}", 'error')
                else:
                    self.log(f"Timeout ao aguardar campo de mensagem para {telefone_formatado}", 'error')
                return False
                
        except Exception as e:
            self.log(f"Erro ao enviar mensagem para {telefone_formatado}: {str(e)}", 'error')
            return False

    def iniciar_envio_thread(self):
        """
        Inicia o envio em uma nova thread para não travar a interface.
        """
        if not self.processing:
            self.processing = True
            self.stop_requested = False
            self.btn_enviar.config(state=tk.DISABLED)
            self.btn_parar.config(state=tk.NORMAL)
            self.btn_selecionar.config(state=tk.DISABLED)
            
            thread = threading.Thread(target=self.processar_envio)
            thread.daemon = True
            thread.start()

    def parar_envio(self):
        """
        Sinaliza para interromper o loop de envio no meio.
        """
        if self.processing:
            self.stop_requested = True
            self.log("Solicitação de parada recebida. Aguardando conclusão do envio atual...")
            self.btn_parar.config(state=tk.DISABLED)

    def atualizar_progresso(self, current, total):
        """
        Atualiza a barra de progresso e o label de status.
        """
        progress = (current / total) * 100
        self.progress['value'] = progress
        self.lbl_status.config(text=f"Progresso: {current}/{total} ({progress:.1f}%)")
        self.master.update_idletasks()

    def processar_envio(self):
        """
        Lê a planilha e processa o envio das mensagens.
        """
        try:
            df = pd.read_excel(self.caminho_planilha, dtype=str)
            self.log(f"Planilha carregada. Total de linhas: {len(df)}", 'success')

            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            # Usando resource_path para o perfil Chrome
            chrome_profile = resource_path('chrome_profile')
            if not os.path.exists(chrome_profile):
                os.makedirs(chrome_profile)
            options.add_argument(f"--user-data-dir={chrome_profile}")
            
            try:
                service = Service(ChromeDriverManager().install())
            except Exception as e:
                # Fallback para chromedriver local
                chromedriver_path = resource_path(os.path.join('selenium', 'chromedriver'))
                if sys.platform == 'win32':
                    chromedriver_path += '.exe'
                service = Service(chromedriver_path)
            
            self.driver = webdriver.Chrome(service=service, options=options)

            self.driver.get("https://web.whatsapp.com")
            self.log("Aguardando confirmação de login no WhatsApp Web...")
            
            if not messagebox.askokcancel(
                "Confirmar Login",
                "Por favor, faça o login no WhatsApp Web escaneando o QR Code.\n\n"
                "Clique em OK apenas depois de ter feito o login com sucesso.",
                icon='info'
            ):
                self.log("Processo cancelado pelo usuário")
                self.finalizar_processo()
                return

            self.log("Login confirmado. Iniciando envio das mensagens...", 'success')
            
            self.mensagens_enviadas = 0
            self.total_mensagens = len(df) - 1
            
            for index, row in df.iloc[1:].iterrows():
                if self.stop_requested:
                    self.log("Processo interrompido pelo usuário")
                    break
                    
                try:
                    mensagens_a_enviar = []
                    for col in df.columns[2:]:  # Começa da terceira coluna (após Telefone e Mensagem)
                        if not pd.isna(df.iloc[0][col]) and not pd.isna(row[col]):
                            condicao_geral = str(df.iloc[0][col]).strip().upper()
                            condicao_individual = str(row[col]).strip().upper()
                            
                            if condicao_geral == 'SIM' and condicao_individual == 'SIM':
                                telefone = str(row['Telefone']).strip()
                                mensagem = str(row['Mensagem']).strip()
                                mensagens_a_enviar.append((telefone, mensagem))
                    
                    # Se houver mensagens para enviar
                    if mensagens_a_enviar:
                        for telefone, mensagem in mensagens_a_enviar:
                            if self.stop_requested:
                                break
                                
                            if self.enviar_mensagem(self.driver, telefone, mensagem):
                                self.mensagens_enviadas += 1
                            
                            # Adiciona um tempo de espera aleatório entre os envios
                            tempo_espera = random.uniform(10, 20)
                            time.sleep(tempo_espera)
                    
                    # Atualiza a barra de progresso
                    self.atualizar_progresso(index, self.total_mensagens)
                    
                except Exception as e:
                    self.log(f"Erro na linha {index + 2}: {str(e)}", 'error')
                    continue

        except Exception as e:
            self.log(f"Erro crítico: {str(e)}", 'error')
            messagebox.showerror("Erro Crítico", str(e))
        finally:
            self.finalizar_processo()

    def finalizar_processo(self):
        """
        Encerra o processo, fecha o WebDriver, 
        reseta os botões e mostra um resumo no log.
        """
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
            
        self.log(f"\nProcesso finalizado\nMensagens enviadas: {self.mensagens_enviadas}\nTotal de tentativas: {self.total_mensagens}")
        
        self.processing = False
        self.stop_requested = False
        self.btn_enviar.config(state=tk.NORMAL)
        self.btn_parar.config(state=tk.DISABLED)
        self.btn_selecionar.config(state=tk.NORMAL)
        self.progress['value'] = 0
        self.lbl_status.config(text="")

def main():
    root = tk.Tk()
    app = WhatsAppSender(root)
    root.mainloop()

if __name__ == "__main__":
    main()