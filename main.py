import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkbootstrap import Style
from tkinter import font

from PIL import Image, ImageTk

import conexao as bd

class Tela():
    
    def __init__(self, master):
        self.janela = master
        self.janela.title('Plataforma de Atividades Interativas')
        self.janela.minsize(1000, 600)
        try: self.janela.attributes('-zoomed', True)
        except: self.janela.state('zoomed')
        
        self.style = Style()
        self.style.theme_use('sandstone')
        self.bg_light = '#A6A6A6'
        self.bg_dark = '#D9D9D9'
        self.bg_atual = self.bg_light

        self.header = ttk.Frame(self.janela, height=50)
        self.header.pack(side='top', fill='x')

        self.header.grid_rowconfigure(0, weight=1)
        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid_columnconfigure(1, weight=1)
        self.header.grid_columnconfigure(2, weight=1)
        self.header.grid_columnconfigure(3, weight=1)
        self.header.grid_columnconfigure(4, weight=1)
        
        self.imagem = Image.open('logo.png')
        self.logo = ImageTk.PhotoImage(self.imagem)
        self.logo_label = ttk.Label(self.header, image=self.logo)
        self.logo_label.grid(row=0, column=0)
        
        self.inicio = ttk.Label(self.header, text='INÍCIO', font=('Times New Roman', 18), padding=(50, 50), cursor='hand2')
        self.inicio.grid(row=0, column=1)
        self.inicio.bind('<Button-1>', lambda event, label_name=self.inicio: self.atualiza_header(label_name))
        
        self.questoes = ttk.Label(self.header, text='QUESTÕES', font=('Times New Roman', 18), padding=(50, 50), cursor='hand2')
        self.questoes.grid(row=0, column=2)
        self.questoes.bind('<Button-1>', lambda event, label_name=self.questoes: self.atualiza_header(label_name))
        
        self.perfil = ttk.Label(self.header, text='PERFIL', font=('Times New Roman', 18), padding=(50, 50), cursor='hand2')
        self.perfil.grid(row=0, column=3)
        self.perfil.bind('<Button-1>', lambda event, label_name=self.perfil: self.atualiza_header(label_name))
        
        self.tema = ttk.Label(self.header, text='☀', font=('Times New Roman', 18), padding=(50, 50), cursor='hand2')
        self.tema.grid(row=0, column=4)
        self.tema.bind('<Button-1>', self.troca_tema)

        self.actual_header_option = self.inicio
        self.actual_header_option.config(background='')
        self.actual_header_option = self.inicio
        self.inicio.config(background=self.bg_atual)
        
        self.style.configure('Footer.TFrame', background=self.bg_atual)
        self.style.configure('Button.TButton', font=('Times New Roman', 24))
        self.style.configure('Label.TLabel', foreground='white', background='#004AAD')

        self.footer = ttk.Frame(self.janela, style='Footer.TFrame')
        self.footer.pack(side='bottom', fill='x')

        self.footer_label = ttk.Label(self.footer, text='© 2023 Daniel Elias & Erika da Hora', background=self.bg_atual, font=('Times New Roman', 12))
        self.footer_label.pack()
        
        self.main = ttk.Frame(self.janela)
        self.main.pack(expand=True, fill='both')
        
        self.nav = tk.Frame(self.main)
        self.nav.pack(side='top', fill='x')
        self.nav.configure(background='#004AAD')
        
        self.nav_inicio()
        
        self.usuario_logado = ''
        
    def nav_inicio(self):
        lbl1 = ttk.Label(self.nav, text='Reduza suas chaces de reprovação.', font=('Times New Roman', 24), style='Label.TLabel')
        lbl1.pack(pady=10)
        lbl2 = ttk.Label(self.nav, text='ESTUDE COM NOSSO BANCO DE QUESTÕES DAS DISCIPLINAS DO CURSO DE SISTEMAS DE INFORMAÇÃO.', font=('Times New Roman', 14), style='Label.TLabel')
        lbl2.pack(pady=10)
        self.nav_inicio_btn = ttk.Button(self.nav, text='Começar', style='Button.TButton', command=self.cadastro)
        self.nav_inicio_btn.pack(pady=10)
    
    def nav_questoes(self):
        lbl = ttk.Label(self.nav, text='Questões', style='Label.TLabel', font=('Times New Roman', 18))
        lbl.grid(padx=100, pady=20)

    def nav_perfil(self):
        lbl = ttk.Label(self.nav, text='Perfil', style='Label.TLabel', font=('Times New Roman', 18))
        lbl.grid(padx=100, pady=20)
    
    def main_perfil(self):
        lbf = tk.LabelFrame(self.main, text='Informações Cadastrais', font=('Times New Roman', 18))
        lbf.pack(ipadx=75, pady=15)
        
        frm_nome = tk.Frame(lbf)
        frm_nome.pack(padx=15, pady=15)
        lbl_nome = ttk.Label(frm_nome, text='Nome:', font=('Times New Roman', 14), justify='center')
        lbl_nome.pack()
        ent_nome = ttk.Entry(frm_nome, width=25, font=('Times New Roman', 16), justify='center')
        ent_nome.pack(pady=10)
        
        frm_email = tk.Frame(lbf)
        frm_email.pack(padx=15, pady=15)
        lbl_email = ttk.Label(frm_email, text='Email:', font=('Times New Roman', 14))
        lbl_email.pack()
        ent_senha = ttk.Entry(frm_email, width=25, font=('Times New Roman', 16), justify='center')
        ent_senha.pack(pady=10)
        
        btn = ttk.Button(lbf, text='Atualizar', style='Button.TButton')
        btn.pack(pady=15)

    def atualiza_header(self, seleceted_header_option):
        self.actual_header_option.config(background='')
        self.actual_header_option = seleceted_header_option
        seleceted_header_option.config(background=self.bg_atual)
        self.limpa_tela(self.nav)
        self.limpa_tela(self.main)
        if seleceted_header_option == self.inicio:
            self.nav_inicio()
        elif seleceted_header_option == self.questoes:
            self.nav_questoes()
        elif seleceted_header_option == self.perfil:
            if self.usuario_logado == '':
                self.login()
            self.nav_perfil()
            self.main_perfil()
        
    def troca_tema(self, e):
        estilo_atual = self.style.theme_use()
        if estilo_atual == 'sandstone':
            self.tema.config(text='🌙')
            self.bg_atual = self.bg_light
            self.style.theme_use('darkly')
        else:
            self.tema.config(text='☀')
            self.bg_atual = self.bg_dark
            self.style.theme_use('sandstone')
        self.style.configure('Footer.TFrame', background=self.bg_atual)
        self.style.configure('Button.TButton', font=('Times New Roman', 24))
        self.style.configure('Label.TLabel', foreground='white', background='#004AAD')
        self.footer.config(style='Footer.TFrame')
        self.footer_label.config(background=self.bg_atual)
        self.nav.config(bg='#004AAD')
        self.nav_inicio_btn.config(style='Button.TButton')
        
    def limpa_tela(self, tela):
        for item in tela.winfo_children():
            if item == self.nav: pass
            else: item.destroy()

    def cadastro(self):
        
        self.val_nome = False
        def focus_in(entry):
            if entry == self.ent_nome:
                if self.ent_nome.get() == 'nome de usuario':
                    self.ent_nome.delete(0, 'end')
            elif entry == self.ent_senha:
                if self.ent_senha.get() == 'senha':
                    self.ent_senha.delete(0, 'end')
                    self.ent_senha.configure(show='*')

        def focus_out(entry):
            if entry == self.ent_nome:
                if self.ent_nome.get() == '':
                    self.ent_nome.insert('end', 'nome de usuario')
                else:
                    r = bd.listar(f'SELECT * FROM usuario U WHERE U.nome = "{self.ent_nome.get()}";')
                    print(r)
                    if len(r) >= 1:
                        if len(frm3.winfo_children()) == 1:
                            self.lbl4 = ttk.Label(frm3, text='Nome de usuário indisponível', font=('Times New Roman', 12))
                            self.lbl4.pack()
                    else:
                        self.val_nome = True
                        try: self.lbl4.destroy()
                        except: pass
            elif entry == self.ent_senha:
                if self.ent_senha.get() == '':
                    self.ent_senha.insert('end', 'senha')
                    self.ent_senha.configure(show='')
        
        def valida_senha(entry):
            senha = entry.get()
            self.vv1.config(text='✅' if len(senha) >= 8 else '❌')
            self.vv2.config(text='✅' if len([i for i in range(65, 91) if chr(i) in senha]) > 0 else '❌')
            self.vv3.config(text='✅' if len([i for i in senha if not i.isalnum()]) > 0 else '❌')
            self.vv4.config(text='✅' if len([i for i in senha if i.isdigit()]) > 0 else '❌')

        def habilitar_botao(e):
            valida_senha(self.ent_senha)
            val_senha = False
            if self.vv1.cget('text') == self.vv2.cget('text') == self.vv3.cget('text') == self.vv4.cget('text') == '✅':
                val_senha = True
            if self.val_nome and val_senha:
                btn_confirmar.config(state='normal')
            else:
                btn_confirmar.config(state='disabled')

        self.tlv_cadastro = tk.Toplevel(self.janela)
        self.tlv_cadastro.title('Crie sua conta')
        self.tlv_cadastro.geometry('500x400')
        self.tlv_cadastro.grab_set()
                
        self.tlv_cadastro.grid_columnconfigure(0, weight=1)
        self.tlv_cadastro.grid_rowconfigure(0, weight=1)
        self.tlv_cadastro.grid_rowconfigure(1, weight=1)
        self.tlv_cadastro.grid_rowconfigure(2, weight=1)
        self.tlv_cadastro.grid_rowconfigure(3, weight=1)
        self.tlv_cadastro.grid_rowconfigure(4, weight=1)
        self.tlv_cadastro.grid_rowconfigure(5, weight=1)
        
        self.imagem = Image.open('logo.png')
        self.logo = ImageTk.PhotoImage(self.imagem)
        self.logo_label = ttk.Label(self.header, image=self.logo)
        self.logo_label.grid(row=0, column=0)
        
        frm1 = ttk.Frame(self.tlv_cadastro)
        frm1.grid(row=1, column=0)
        
        lbl1 = ttk.Label(frm1, text='Já está cadastrado?', font=('Times New Roman', 16))
        lbl1.pack(side='left')
        lbl2 = ttk.Label(frm1, text='Faça login', foreground='#233dff', cursor='hand2', font=('Times New Roman', 16))
        lbl2.config(underline=6)
        fonte = font.Font(lbl2, lbl2.cget('font'))
        fonte.configure(underline=True)
        lbl2.configure(font=fonte)
        lbl2.bind('<Button-1>', self.cadastro_login)
        lbl2.pack(side='left')
        
        frm3 = ttk.Frame(self.tlv_cadastro)
        frm3.grid(row=2, column=0)
        self.ent_nome = ttk.Entry(frm3, width=25, font=('Times New Roman', 16), justify='center')
        self.ent_nome.insert('end', 'nome de usuario')
        self.ent_nome.pack()
        self.ent_nome.bind('<FocusIn>', lambda event, entry=self.ent_nome: focus_in(self.ent_nome))
        self.ent_nome.bind('<FocusOut>', lambda event, entry=self.ent_nome: focus_out(self.ent_nome))
        
        self.ent_senha = ttk.Entry(self.tlv_cadastro, width=25, font=('Times New Roman', 16), justify='center')
        self.ent_senha.insert('end', 'senha')
        self.ent_senha.grid(row=3, column=0)
        self.ent_senha.bind('<FocusIn>', lambda event, entry=self.ent_senha: focus_in(entry))
        self.ent_senha.bind('<FocusOut>', lambda event, entry=self.ent_senha: focus_out(entry))
        self.ent_senha.bind('<KeyRelease>', lambda event, entry=self.ent_senha: valida_senha(entry))
        
        self.style.configure('Frame.TFrame', background=self.bg_atual)
        frm2 = ttk.Frame(self.tlv_cadastro, style='Frame.TFrame')
        frm2.grid(row=4, column=0)

        frmv1 = ttk.Label(frm2)
        frmv1.pack(fill='x', anchor='w')
        self.vv1 = ttk.Label(frmv1, text='❌')
        self.vv1.pack(side='left')
        v1 = ttk.Label(frmv1, text='No mínimo 8 caracteres', font=('Times New Roman', 12))
        v1.pack(side='left')
        
        frmv2 = ttk.Label(frm2)
        frmv2.pack(fill='x', anchor='w')
        self.vv2 = ttk.Label(frmv2, text='❌')
        self.vv2.pack(side='left')
        v2 = ttk.Label(frmv2, text='Uma letra maiúscula', font=('Times New Roman', 12))
        v2.pack(side='left')
        
        frmv3 = ttk.Label(frm2)
        frmv3.pack(fill='x', anchor='w')
        self.vv3 = ttk.Label(frmv3, text='❌')
        self.vv3.pack(side='left')
        v3 = ttk.Label(frmv3, text='Um caracter especial', font=('Times New Roman', 12))
        v3.pack(side='left')
                
        frmv4 = ttk.Label(frm2)
        frmv4.pack(fill='x', anchor='w')
        self.vv4 = ttk.Label(frmv4, text='❌')
        self.vv4.pack(side='left')
        v4 = ttk.Label(frmv4, text='Um número', font=('Times New Roman', 12))
        v4.pack(side='left')
        
        btn_confirmar = ttk.Button(self.tlv_cadastro, text='Confirmar', style='Button.TButton', command=self.confirmar_cadastro, state='disabled')
        btn_confirmar.grid(row=5, column=0)
        btn_confirmar.bind('<Enter>', habilitar_botao)

    def confirmar_cadastro(self):
        nome = self.ent_nome.get()
        senha = self.ent_senha.get()
        sql_inserir = f"INSERT INTO usuario VALUES (NULL, '{nome}', '{senha}');"
        bd.inserir(sql_inserir)
        messagebox.showinfo('Aviso', 'Usuário cadastrado com sucesso!')
        self.tlv_cadastro.destroy()
    
    def login(self):
        self.tlv_login = tk.Toplevel(self.janela)
        self.tlv_login.title('Entre na sua conta')
        self.tlv_login.geometry('500x400')
        self.tlv_login.grab_set()
        
        self.tlv_login.grid_columnconfigure(0, weight=1)
        self.tlv_login.grid_rowconfigure(0, weight=1)
        self.tlv_login.grid_rowconfigure(1, weight=1)
        self.tlv_login.grid_rowconfigure(2, weight=1)
        self.tlv_login.grid_rowconfigure(3, weight=1)
        self.tlv_login.grid_rowconfigure(4, weight=1)
        
        self.imagem = Image.open('logo.png')
        self.logo = ImageTk.PhotoImage(self.imagem)
        self.logo_label = ttk.Label(self.header, image=self.logo)
        self.logo_label.grid(row=0, column=0)
        
        frm1 = ttk.Frame(self.tlv_login)
        frm1.grid(row=1, column=0)
        lbl1 = ttk.Label(frm1, text='Não possui uma conta', font=('Times New Roman', 16))
        lbl1.pack(side='left')
        lbl2 = ttk.Label(frm1, text='Cadastre-se', foreground='#233dff', cursor='hand2', font=('Times New Roman', 16))
        lbl2.config(underline=6)
        fonte = font.Font(lbl2, lbl2.cget('font'))
        fonte.configure(underline=True)
        lbl2.configure(font=fonte)
        lbl2.bind('<Button-1>', self.login_cadastro)
        lbl2.pack(side='left')
        
        self.ent_nome = ttk.Entry(self.tlv_login, width=25, font=('Times New Roman', 16), justify='center')
        self.ent_nome.insert('end', 'nome de usuario')
        self.ent_nome.bind('<FocusIn>', lambda event, entry=self.ent_nome: focus_in(self.ent_nome))
        self.ent_nome.bind('<FocusOut>', lambda event, entry=self.ent_nome: focus_out(self.ent_nome))
        self.ent_nome.grid(row=2, column=0)
        self.ent_senha = ttk.Entry(self.tlv_login, width=25, font=('Times New Roman', 16), justify='center')
        self.ent_senha.insert('end', 'senha')
        self.ent_senha.grid(row=3, column=0)
        self.ent_senha.bind('<FocusIn>', lambda event, entry=self.ent_senha: focus_in(entry))
        self.ent_senha.bind('<FocusOut>', lambda event, entry=self.ent_senha: focus_out(entry))
        
        btn_confirmar = ttk.Button(self.tlv_login, text='Confirmar', style='Button.TButton', command=self.confirmar_cadastro)
        btn_confirmar.grid(row=4, column=0)
        
        def focus_in(entry):
            if entry == self.ent_nome:
                if self.ent_nome.get() == 'nome de usuario':
                    self.ent_nome.delete(0, 'end')
            elif entry == self.ent_senha:
                if self.ent_senha.get() == 'senha':
                    self.ent_senha.delete(0, 'end')
                    self.ent_senha.configure(show='*')
        
        def focus_out(entry):
            if entry == self.ent_nome:
                if self.ent_nome.get() == '':
                    self.ent_nome.insert('end', 'nome de usuario')
            elif entry == self.ent_senha:
                if self.ent_senha.get() == '':
                    self.ent_senha.insert('end', 'senha')
                    self.ent_senha.configure(show='')

    def cadastro_login(self, e):
        self.tlv_cadastro.destroy()
        self.login()
    
    def login_cadastro(self, e):
        self.tlv_login.destroy()
        self.cadastro()

app = tk.Tk()
janelaPrincipal = Tela(app)
app.mainloop()