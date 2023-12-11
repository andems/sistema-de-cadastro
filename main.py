from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser

main = Tk()

class relatorio():
    def printCli(self):
        webbrowser.open("cliente.pdf")

    def gerarRelatorio(self):
        self.c = canvas.Canvas("cliente.pdf")

        self.codigoR = self.eCodigo.get()
        self.nomeR = self.eNome.get()
        self.telefoneR = self.eTelefone.get()
        self.cidadeR = self.eCidade.get()

        # nome do titulo
        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, "Ficha de Cliente")

        # codigo
        self.c.setFont("Helvetica-Bold", 15)
        self.c.drawString(60, 700, "Codigo:")
        self.c.setFont("Helvetica", 12)
        self.c.drawString(150, 700, self.codigoR)

        # nome
        self.c.setFont("Helvetica-Bold", 15)
        self.c.drawString(60, 680, "Nome:")
        self.c.setFont("Helvetica", 12)
        self.c.drawString(150, 680, self.nomeR)

        # Telefone
        self.c.setFont("Helvetica-Bold", 15)
        self.c.drawString(60, 660, "Telefone:")
        self.c.setFont("Helvetica", 12)
        self.c.drawString(150, 660, self.telefoneR)

        # CidadeS
        self.c.setFont("Helvetica-Bold", 15)
        self.c.drawString(60, 640, "Cidade:")
        self.c.setFont("Helvetica", 12)
        self.c.drawString(150, 640, self.cidadeR)

        #borda em volta
        self.c.rect(40, 720, 500, -100, fill=False, stroke=True)

        #chamar a web
        self.c.showPage()
        #salvar o pdf
        self.c.save()
        self.printCli()

#classe que vai atribuir funções a os butões
class func():
    def limparTela(self):
        self.eCodigo.delete(0, END)
        self.eNome.delete(0, END)
        self.eTelefone.delete(0, END)
        self.eCidade.delete(0, END)

    # connectar o banco de dados
    def connectBD(self):
        self.conn = sqlite3.connect("clientes.bd")
        self.cursor = self.conn.cursor()

    # desconnectar o banco de dados
    def desconnectarBD(self):
        self.conn.close(); print('Desconectando ao banco.')
    
    # criar tabelas no banco de dados
    def montaTabelas(self):
        self.connectBD(); print('Conectando ao banco....')

        #criando as tabelas
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                telefone INTEGER(20),
                cidade CHAR(40)
            );
        """)
        self.conn.commit(); print('Banco de dados criado.')
        self.desconnectarBD()

    #so para guardar as variaveis
    def variaveis(self):
        self.codigo = self.eCodigo.get()
        self.nome = self.eNome.get()
        self.telefone = self.eTelefone.get()
        self.cidade = self.eCidade.get()

    # Adicionar valores
    def add(self):
        self.variaveis()
        self.connectBD()

        self.cursor.execute("""INSERT INTO clientes (nome, telefone, cidade) VALUES(?, ?, ?)""", (self.nome, self.telefone, self.cidade))
        self.conn.commit()
        messagebox.showinfo('Cadastramento', "sucesso")
        self.desconnectarBD()
        self.select()
        self.limparTela()
    
    #selecionar os clientes no frame de baixo
    def select(self):
        self.lCliente.delete(*self.lCliente.get_children())
        self.connectBD()

        lista = self.cursor.execute("""
                    SELECT id, nome, telefone, cidade FROM clientes ORDER BY nome ASC; """)
        
        for i in lista:
            self.lCliente.insert("", END, values=i)
        self.desconnectarBD()

    # seleciona quando clicar duas vezes
    def onTrueClick(self, event):
        self.limparTela()
        self.lCliente.selection()

        for n in self.lCliente.selection():
            col1, col2, col3, col4 = self.lCliente.item(n, 'values')
            self.eCodigo.insert(END, col1)
            self.eNome.insert(END, col2)
            self.eTelefone.insert(END, col3)
            self.eCidade.insert(END, col4)

    #deletar os clientes
    def deleta(self):
        self.variaveis()
        self.connectBD()
        self.cursor.execute("""DELETE FROM clientes WHERE id = ? """, (self.codigo))
        
        self.test = messagebox.askquestion('Exclusão', "Deseja Excluir ?")

        if self.test == "yes":
            self.conn.commit()
            messagebox.showinfo('INFOR','Excluido')
        else:
            self.limparTela()      
        
        self.desconnectarBD()
        self.limparTela()
        self.select()

    # Alterar os dados
    def alterar(self):
        self.variaveis()
        self.connectBD()
        self.cursor.execute("""UPDATE clientes set nome= ?, telefone= ?, cidade= ? WHERE id= ? ;""",(self.nome, self.telefone, self.cidade, self.codigo))
        self.conn.commit()
        messagebox.showinfo('Alteração', "Editado com Sucesso")
        self.desconnectarBD()
        self.limparTela()
        self.select()

    # Buscar os clientes
    def buscaCli(self):
        self.connectBD()
        self.lCliente.delete(*self.lCliente.get_children())

        self.eNome.insert(END, '%')
        nomecli = self.eNome.get()
        self.cursor.execute(""" SELECT id, nome, telefone, cidade FROM clientes WHERE nome LIKE '%s' ORDER BY nome ASC""" %nomecli)
        
        buscaNomeCli = self.cursor.fetchall()
        for i in buscaNomeCli:
            self.lCliente.insert("", END, values=i)
        
        self.limparTela()
        self.desconnectarBD()
#classe de criação do sistema
class application(func, relatorio):

    #funcão que vai chamar as funções.obs: colocar em ordem
    def __init__(self):
        self.root = main
        self.tela()
        self.frameTela()
        self.wedgetsFram1()
        self.wedgetsFrame2()
        self.montaTabelas()
        self.select()
        self.menu()
        main.mainloop()

    #configuração da tela, tamanho    
    def tela(self):
        
        self.root.title('Cadastro')
        self.root.configure(background="#4B0082")
        self.root.geometry("700x500")
        self.root.maxsize(width='900', height='700')
        self.root.minsize(width='650', height='450')

    def frameTela(self):
        #divisao da tela
        #parte de cima
        self.frame1 = Frame(self.root, bd=4, bg='#D8BFD8', highlightbackground='#000000', highlightthickness='1')
        self.frame1.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.48)
        
        # parte cadastro
        self.fCadastro = Frame(self.root, bd=4, bg='#D8BFD8', highlightbackground='#000000', highlightthickness='1')
        self.fCadastro.place(relx=0.01, rely=0.15, relwidth=0.98, relheight=0.34)

        # parte de baixo
        self.frame2 = Frame(self.root, bd=4, bg='#D8BFD8', highlightbackground='#000000', highlightthickness='1')
        self.frame2.place(relx=0.01, rely=0.5, relwidth=0.98, relheight=0.48)
    
    def wedgetsFram1(self):
        # botao Limpar
        self.btLimpar = Button(self.frame1, text="Limpar", bg='#363636', fg='#ffffff', bd=2, command=self.limparTela)
        self.btLimpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.1)
        
        # botao Buscar
        self.btBuscar = Button(self.frame1, text="Buscar", bg='#363636', fg='#ffffff', bd=2, command=self.buscaCli)
        self.btBuscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.1)
                
        #Criação da label codigo
        self.lbCodigo = Label(self.frame1, text='Codigo', bg='#D8BFD8')
        self.lbCodigo.place(relx=0.02, rely=0.11, relwidth=0.07, relheight=0.1)
        
        # Entrada do codigo
        self.eCodigo = Entry(self.frame1)
        self.eCodigo.place(relx=0.09, rely=0.1, relwidth=0.11, relheight=0.1)

        # parte do cadastro
        # botao Cadastar
        self.btCadastar = Button(self.fCadastro, text="Cadastar", bg='#363636', fg='#ffffff', bd=2, command= self.add)
        self.btCadastar.place(relx=0.65, rely=0.7, relwidth=0.1, relheight=0.15)

        # botao Alterar
        self.btAlterar = Button(self.fCadastro, text="Editar", bg='#363636', fg='#ffffff', bd=2, command= self.alterar)
        self.btAlterar.place(relx=0.75, rely=0.7, relwidth=0.1, relheight=0.15)
        
        # botao Apagar
        self.btApagar = Button(self.fCadastro, text="Excluir", bg='#DC143C', fg='#ffffff', bd=2, command=self.deleta)
        self.btApagar.place(relx=0.85, rely=0.7, relwidth=0.1, relheight=0.15)

        #Criação da label nome
        self.lbNome = Label(self.fCadastro, text='Nome:', bg='#D8BFD8')
        self.lbNome.place(relx=0.02, rely=0.11, relwidth=0.07, relheight=0.15)
        # Entrada do Nome
        self.eNome = Entry(self.fCadastro)
        self.eNome.place(relx=0.12, rely=0.1, relwidth=0.86, relheight=0.15)

        #Criação da label Telefone
        self.lbTelefone = Label(self.fCadastro, text='Telefone:', bg='#D8BFD8')
        self.lbTelefone.place(relx=0.02, rely=0.31, relwidth=0.1, relheight=0.15)
        # Entrada do Telefone
        self.eTelefone = Entry(self.fCadastro)
        self.eTelefone.place(relx=0.12, rely=0.3, relwidth=0.3, relheight=0.15)

        #Criação da label Cidade
        self.lbCidade = Label(self.fCadastro, text='Cidade:', bg='#D8BFD8')
        self.lbCidade.place(relx=0.5, rely=0.31, relwidth=0.07, relheight=0.15)
        # Entrada do Cidade
        self.eCidade = Entry(self.fCadastro)
        self.eCidade.place(relx=0.57, rely=0.3, relwidth=0.38, relheight=0.15)

    def wedgetsFrame2(self):
        #criando as colunas
        self.lCliente = ttk.Treeview(self.frame2, height=3, columns=('col1', 'col2', 'col3', 'col4'))
        self.lCliente.place(relx=0.01, rely=0.01, relwidth=0.96, relheight=0.88)
        self.lCliente.heading("#0", text='')
        self.lCliente.heading("#1", text='Codigo')
        self.lCliente.heading("#2", text='Nome')
        self.lCliente.heading("#3", text='Telefone')
        self.lCliente.heading("#4", text='Cidade')

        #definindo o tamanho
        #tamanho total é 500 e um pouco
        self.lCliente.column("#0", width=1)
        self.lCliente.column("#1", width=50)
        self.lCliente.column("#2", width=200)
        self.lCliente.column("#3", width=125)
        self.lCliente.column("#4", width=125)
        
        # barra de rolagem
        self.scrollista = Scrollbar(self.frame2, orient='vertical')
        self.lCliente.configure(yscroll=self.scrollista.set)
        self.scrollista.place(relx=0.97, rely=0.1, relwidth=0.02, relheight=0.79)

        #chamando a função de dois click
        self.lCliente.bind("<Double-1>", self.onTrueClick)
    #menu, parte de cima
    def menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()

        menubar.add_cascade(label="Opções", menu= filemenu)
        menubar.add_cascade(label="Relatorios", menu=filemenu2)

        filemenu.add_command(label="Sair", command= Quit)
        filemenu.add_command(label="limpar Cliente", command= self.limparTela)

        filemenu2.add_command(label="Ficha Cliente", command=self.gerarRelatorio)

application()
