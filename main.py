from PySide6.QtWidgets import *
from Login import Ui_Form
from tela_principal import Ui_MainWindow
from PySide6.QtGui import QIcon
from PySide6 import QtCore
import sys
from banco_dados import DataBase
from PySide6 import QtGui
from PySide6.QtCore import QTimer
from funcoes import *
from PySide6.QtWidgets import QTableWidget
from relogio import Relogio

class Login(QWidget, Ui_Form):
    
    def __init__(self) -> None:
        super(Login, self).__init__()
        # variavel
        self.tentativas = 0
        self.setupUi(self)
        self.setWindowTitle("Login do Sistema")

        self.btn_login.clicked.connect(self.check_login)

    def check_login(self):
            bd = DataBase()
            bd.conecta()

            # passa texto da tela login pra função check_user
            autenticado = bd.check_user(self.login_usuario.text(), self.login_senha.text())
            usuario = self.login_usuario.text()
            senha = self.login_senha.text()
            admin = "553699"
            admin2 = "553699"
            
            if admin == usuario and senha == admin2:
                self.w = MainWindow()
                self.w.show()
                self.close()
                self.w.frame_usuarios.setMaximumHeight(45)
                self.w.btn_menu_peca_editar.setMaximumHeight(20)
                self.w.btn_editar_fornecedor.setMaximumHeight(20)
            # .upper() deixa letra tudo maiuscula  \ .lower() deixa tudo minuscula
            elif autenticado == "Admin" :
                self.w = MainWindow()
                self.w.show()
                self.close()
                self.w.frame_usuarios.setMaximumHeight(45)
                self.w.btn_menu_peca_editar.setMaximumHeight(20)
                self.w.btn_editar_fornecedor.setMaximumHeight(20)

            elif autenticado == "Usuario":
                self.w = MainWindow()
                self.w.show()
                self.close()
            else:
                if self.tentativas < 3:
                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Warning) 
                    msgBox.setWindowTitle("Erro")
                    msgBox.setText(f'Login ou senha incorreto \n\n Tentativa: {self.tentativas +1} de 3')
                    msgBox.exec()
                    self.tentativas += 1
                    self.login_usuario.setText("")
                    self.login_senha.setText("")

                if self.tentativas == 3:
                    
                    sys.exit(0)
                       
class MainWindow (QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("JbpG - Sistema de gerenciamento de dados")
        appIcon = QIcon(u"")
        self.setWindowIcon(appIcon)
        self.atualiza_tabelas()
        


        # tempo pro relogio atualizar
        time = QTimer(self)
        time.timeout.connect(self.relogio)
        time.start(1000)
        self.data()

               
           


 #-------------------------------------------------------------
    #pesquisa na tabela
        self.pesquisa_tb_produtos.textChanged.connect(self.filtro_edita)
        self.pesquisar_produtos.textChanged.connect(self.filtro_pesquisa)
        self.pesquisa_nome_excluirUsuario.textChanged.connect(self.filtro_nomeUsuario)
        self.pesquisa_id_excluir.textChanged.connect(self.filtro_idUsuario)
        self.pesquisa_nomeUsuario.textChanged.connect(self.filtro_nomeUsuario2)
        self.pesquisa_IDusuario.textChanged.connect(self.filtro_idUsuario2)
        self.pesquisa_CNPJ_fornecedor.textChanged.connect(self.filtro_CNPJ)
        self.pesquisa_nome_fornecedor.textChanged.connect(self.filtro_fornecedor)
        self.pesquisa_CNPJ_excluir.textChanged.connect(self.filtro_CNPJ2)
        self.pesquisa_nome_excluirFornecedor.textChanged.connect(self.filtro_fornecedor2)
        self.btn_add_venda.clicked.connect(self.alimenta_tela_venda)
        self.btn_addVenda_tabela.clicked.connect(self.alimenta_tabela_vendas)
        self.btn_removeItemVenda.clicked.connect(self.deleta_campo)
        self.btn_vendeItem.clicked.connect(self.somar_valores)

        

    # botao de excluir
        self.Btn_excluirUsuario.clicked.connect(self.deletaUsuario)
        self.btn_excluir_produto_2.clicked.connect(self.excluir_produto)
        self.Btn_excluirFornecedor.clicked.connect(self.excluir_fornecedor)
        
    #botao que vai cadastrar no banco
        self.btn_cadastrar_produtos.clicked.connect(self.cadastrar_produto)
        self.btn_salvar_user.clicked.connect(self.cadastrarUsuario)
        self.btn_pesquisa_alterar.clicked.connect(self.update_tabela)
        self.btn_pesquisa_excluir.clicked.connect(self.alimenta_excluir_tabela)
        self.btn_salvar_fornecedor.clicked.connect(self.cadastrar_fornecedor)
        self.btn_alterarFornecedor.clicked.connect(self.alterar_fornecedor)

        

    # radio buttons
        self.radioButton_excluir.clicked.connect(self.check_radiobutton)
        self.radioButton_excluirUsuario.clicked.connect(self.check_radiobutton)
        self.radioButton_excluirFornecedor.clicked.connect(self.check_radiobutton)
        

    #botao que vai ser animado
        self.btn_menu_principal.clicked.connect(self.btnMenu)
        self.btn_menu_produtos.clicked.connect(self.btnPecas)
        self.btn_fornecedores.clicked.connect(self.btnVendas)
        self.btn_usuarios.clicked.connect(self.btnOutros)
        self.btn_menu_produtos.clicked.connect(self.esconder_produtos)
        self.btn_fornecedores.clicked.connect(self.esconder_fornecedor)
        self.btn_usuarios.clicked.connect(self.esconder_usuario)

    #botao abre paginas do sistema tem que usar a função lamba
        self.btn_menu_peca_cadastrar.clicked.connect(lambda: self.Widget_das_tabelas.setCurrentWidget(self.page_cadastrar_produto))
        self.btn_menu_peca_pesquisar.clicked.connect(lambda:self.Widget_das_tabelas.setCurrentWidget(self.page_peca_pesquisar))
        self.btn_menu_peca_editar.clicked.connect(lambda:self.Widget_das_tabelas.setCurrentWidget(self.page_editar_tabela))
        self.btn_menu_cadastrarUsuario.clicked.connect(lambda:self.Widget_das_tabelas.setCurrentWidget(self.page_cadastrarUsuario))
        self.btn_pesquisa_excluir.clicked.connect(lambda:self.Widget_das_tabelas.setCurrentWidget(self.page_peca_excluir))
        self.btn_pesquisa_excluir.clicked.connect(lambda: self.Widget_das_tabelas.setCurrentWidget(self.page_peca_excluir))
        self.btn_menu_excluirUsuario.clicked.connect(lambda: self.Widget_das_tabelas.setCurrentWidget(self.page_excluir_usuario))
        self.btn_menu_Usuarios.clicked.connect(lambda: self.Widget_das_tabelas.setCurrentWidget(self.page_pesquisa_usuario))
        self.btn_menu_cadastrarFornecedor.clicked.connect(lambda: self.Widget_das_tabelas.setCurrentWidget(self.page_casdastrar_fornecedor))
        self.btn_menu_fornecedor.clicked.connect(lambda: self.Widget_das_tabelas.setCurrentWidget(self.page_pesquisa_fornecedor))
        self.btn_editar_fornecedor.clicked.connect(lambda: self.Widget_das_tabelas.setCurrentWidget(self.page_excluir_fornecedor))
        self.btn_ir_venda.clicked.connect(lambda: self.Widget_das_tabelas.setCurrentWidget(self.page_venda))
        self.btn_add_venda.clicked.connect(lambda: self.Widget_das_tabelas.setCurrentWidget(self.page_venda))
        self.btn_addVenda_tabela_2.clicked.connect(lambda: self.Widget_das_tabelas.setCurrentWidget(self.page_peca_pesquisar))


    # animação de botao
    def btnMenu(self):
        width = self.frame_menu.width()

        if width == 9:
            newWidth = 200
        else:
            newWidth = 9
        
        #lugar que vai ser animado
        self.animation = QtCore.QPropertyAnimation(self.frame_menu, b"maximumWidth")
        # configurações de animação
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        # tipo de animação
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()  
    # animação de botao 
    def btnPecas(self):
        heigth = self.frame_menu_pecas.height()

        if heigth == 0:
            newHeigth = 135
        else:
            newHeigth = 0
        #lugar que vai ser animado
        self.animation = QtCore.QPropertyAnimation(self.frame_menu_pecas, b"minimumHeight")
        # configurações de animação
        self.animation.setDuration(500)
        self.animation.setStartValue(heigth)
        self.animation.setEndValue(newHeigth)
        # tipo de animação
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()   
    # animação de botao
    def btnVendas(self):
        heigth = self.frame_menu_vendas.height()

        if heigth == 0:
            newHeigth = 135
        else:
            newHeigth = 0
        #lugar que vai ser animado
        self.animation = QtCore.QPropertyAnimation(self.frame_menu_vendas, b"minimumHeight")
        # configurações de animação
        self.animation.setDuration(500)
        self.animation.setStartValue(heigth)
        self.animation.setEndValue(newHeigth)
        # tipo de animação
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()   
    # animação de botao
    def btnOutros(self):
        heigth = self.frame_menu_outros.height()

        if heigth == 0:
            newHeigth = 135
        else:
            newHeigth = 0
        #lugar que vai ser animado
        self.animation = QtCore.QPropertyAnimation(self.frame_menu_outros, b"minimumHeight")
        # configurações de animação
        self.animation.setDuration(500)
        self.animation.setStartValue(heigth)
        self.animation.setEndValue(newHeigth)
        # tipo de animação
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()    
   
   # Funçoes de Produto
   
    # cadastra produto     
    def cadastrar_produto(self):
        #pegas o conteudo da tela e salva nas variaveis ja convertidas
        nome = self.cadastrar_nome.text()
        marca = self.cadastrar_marca.text()
        setor = self.cadastrar_setor.text()
        valor_custo = self.cadastrar_valor_custo.text()
        valor_custo = valor_custo.replace(",", ".")
        valor_venda = self.cadastrar_lavor_venda.text()
        valor_venda = valor_venda.replace(",", ".")
        descricao = self.cadastrar_descricao.text()
        quantidade = self.cadastrar_quantidade.text()
        # chama a função
        funcoes = Produtos()
        funcoes.cadastrar_Produto(nome,marca,setor,valor_custo,valor_venda,descricao,quantidade)
        self.atualiza_tabelas()
        self.limpa_campo()
    # Exclui um Produto
    def excluir_produto(self):

        # pega os textos da tela cadastrar
        cod = self.exclui_cod.text()
        # Realiza uma condição if para o chebox
        if self.radioButton_excluir.isChecked():
            # chama o arquivo funcoes
            funcoes = Produtos()
            # chama a função do arquivo
            funcoes.excluir_Produto(cod)
            self.atualiza_tabelas()
            self.limpa_campo()

        else:
            msg = QMessageBox() 
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Erro")
            msg.setText("Selecione o check box para excluir o produto")
            msg.exec()

    # Funçoes de Usuario

    # cadastrar usuarios 
    def cadastrarUsuario(self):

        # pega os textos digitados na tela
        nome = self.user_nome.text()
        usuario = self.user_usuario.text()
        senha = self.user_senha.text()
        senha2 = self.user_repetirSenha.text()
        
        # currentText 'pega o texto do combobox
        acesso = self.user_acesso.currentText()
        funcoes = Usuario()
        funcoes.cadastrar_Usuario(nome,usuario,senha,senha2,acesso)
        
        
    # deleta um usuario
    def deletaUsuario(self):

        id = self.id_excluirUsuario.text()

        if id == "":
            # alerta messagebox
            msg = QMessageBox() 
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Campo vazio")
            msg.setText("Digite o id de Usuario no campo Obrigatorio somente numeros")
            msg.exec()
            texto = self.id_excluirUsuario.setStyleSheet("border:2px solid rgb(255, 0, 0);")
        else:

            validacao = self.radioButton_excluirUsuario.isChecked()             
            funcao = Usuario()
            funcao.deleta_Usuario(id,validacao)
    
    # Funçoes de Fornecedor

    # Cadastra um Fornecedor
    def cadastrar_fornecedor(self):
        CNPJ = self.fornecedor_cnpj.text()
        empresa = self.fornecedor_nome.text()
        tel_empresa = self.fornecedor_telEmpresa.text()
        vendedor = self.fornecedor_nomeVendedor.text()
        tel_vendedor = self.fornecedor_telVendedor.text()
        email = self.fornecedor_email.text()
        # pega texto selecionado do comboBox
        estado = self.fornecedor_comboBox.currentText()
        cidade = self.fornecedor_cidade.text()
        bairro = self.fornecedor_bairro.text()
        cep = self.fornecedor_cep.text()
        rua = self.fornecedor_rua.text()

        fornecedor = Fornecedor()
        fornecedor.cadastrar_fornecedor(CNPJ,empresa,tel_empresa,vendedor,tel_vendedor,email,estado,cidade,bairro,cep,rua)
    #exclui um fornecedor
    def excluir_fornecedor(self):
        db  = DataBase()
        db.conecta()
        try:
            id = int(self.CNJ_excluirFornecedor.text())
            cnpj = db.check_cnpj(id)

            radioButton = 0
            if self.radioButton_excluirFornecedor.isChecked():
                radioButton = 1
            else:
                radioBButton = 2
            
            funcoes = Fornecedor()
            funcoes.excluir_fornecedor(id,cnpj,radioButton)
            self.atualiza_tabelas()



        except ValueError:
            mgs = QMessageBox()
            mgs.setIcon(QMessageBox.Information)
            mgs.setWindowTitle("Somente numeros")
            mgs.setText("Digite somento numeros inteiros")
            mgs.exec()     
    
    
    

       


    # atualizar as tabelas de pesquisa e editar         
    def atualiza_tabelas(self):
        self.tabela_edita()
        self.tabela_pesquisar()
        self.tabelaUsuario()
        self.tabelaFornecedor()  
        self.colorir(self.tabela_pesquisa) 
        self.colorir(self.tabela_produtos)
        self.tabela_pesquisa.resizeColumnsToContents()
        self.tabela_fornecedor.resizeColumnsToContents()
        self.tabela_fornecedor_2.resizeColumnsToContents()
    # alimenta a tabela de excluir
    def alimenta_excluir_tabela(self,id):

        db = DataBase()
        db.conecta()
        id = int(self.exclui_cod.text())
        # cria um cursor 
        cursor = db.conexao.cursor()
        # realiza um comando sql
        cursor.execute('SELECT * FROM produtos WHERE cod = ? ',(id,))
        # tranforma a pesquisa em uma lista
        lista = cursor.fetchall()

        cod = 1
        nome =""
        quantidade= 1
        marca= ""
        valor_custo= 1
        valor_venda=1
        descricao=""

        for linha in lista:
            cod = linha[0]
            nome = linha[1]
            quantidade = linha[2]
            marca = linha[3]
            valor_custo = linha[4]
            valor_venda = linha[5]
            descricao = linha[6]

        cod = str(cod)
        # string formatada f'{varial:.2f}'   :.2f tansforma em casa decimal
        custo = str(f'{valor_custo:.2f}') 
        venda = str(f'{valor_venda:.2f}')
        quantidade =  str(quantidade)
        
        self.nome_excluir.setText(nome)
        self.marca_excluir.setText(marca)
        self.codigo_excluir.setText(cod)
        self.valor_custo_excluir.setText(custo.replace(".", ","))
        self.valor_venda_excluir.setText(venda.replace(".", ","))
        self.quantidade_excluir.setText(quantidade)
        self.descricao_excluir.setText(descricao)    
    # antes de excluir check o botão radio button
    def check_radiobutton(self):

            msg = QMessageBox() 
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Excluir")
            msg.setText("Tem certeza que deseja excluir")
            msg.exec()
    # alimenta tabela de pesquisa
    def tabela_pesquisar(self):
        db = DataBase()
        db.conecta()

        lista = db.preencher_tabela()
        # limpa todos os dados da tabela
        self.tabela_pesquisa.clearContents()
        # coloca tanto de linhas na tabela de acordo com a lista do banco
        self.tabela_pesquisa.setRowCount(len(lista))

            # linha é a linha 0 │ Texto é tudo que tem na lista
        for linha, texto in enumerate(lista): # numera as linhas de acordo com a lista

                #coluna inicia como 0  dado indo de acordo com a coluna
            for coluna, dado in enumerate(texto): # pega 1 dado do meu texto
                    #set item vai colocando coluna por coluna ate fecha no final ai pula pra linha 2 e coloca tudo denovo

                    self.tabela_pesquisa.setItem(linha, coluna,QTableWidgetItem(str(dado)))
                    

        db.fecha_conexao()       
    # alimenta a tabela de editar
    def tabela_edita(self):
        db = DataBase()
        db.conecta()
        lista = db.preencher_tabela()
        # limpa todos os dados da tabela
        self.tabela_produtos.clearContents()
        # coloca tanto de linhas na tabela de acordo com a lista do banco
        self.tabela_produtos.setRowCount(len(lista))

            # linha é a linha 0 │ Texto é tudo que tem na lista
        for linha, texto in enumerate(lista): # numera as linhas de acordo com a lista

                #coluna inicia como 0  dado indo de acordo com a coluna
            for coluna, dado in enumerate(texto): # pega 1 dado do meu texto
                    #set item vai colocando coluna por coluna ate fecha no final ai pula pra linha 2 e coloca tudo denovo

                    self.tabela_produtos.setItem(linha, coluna,QTableWidgetItem(str(dado)))

        db.fecha_conexao() 
    # filtro pra pesquisar
    def filtro_pesquisa(self, filter_text):
        for i in range(self.tabela_pesquisa.rowCount()):
            for j in range(self.tabela_pesquisa.columnCount()):
                item = self.tabela_pesquisa.item(i, 1)
                match = filter_text.lower() not in item.text().lower()
                self.tabela_pesquisa.setRowHidden(i, match)
                if not match:
                    break   
    # filtro pra tabela editar
    def filtro_edita(self, filter_text):
        for i in range(self.tabela_produtos.rowCount()):
            for j in range(self.tabela_produtos.columnCount()):
                item = self.tabela_produtos.item(i, 1)
                match = filter_text.lower() not in item.text().lower()
                self.tabela_produtos.setRowHidden(i, match)
                if not match:
                    break       
    # altera no banco de dados a mudança
    def update_tabela(self):
        dados = []
        update_dados = []

        for linha in range(self.tabela_produtos.rowCount()): #conta nmr de linhas
            for coluna in range(self.tabela_produtos.columnCount()): # conta numero de colunas
                dados.append(self.tabela_produtos.item(linha, coluna).text()) # adiciono pesquina na lista dados

            update_dados.append(dados)
            dados =[]
        self.atualiza_tabelas()
        # atualizar dados no banco

        db = DataBase()
        db.conecta()

        for lista in update_dados:
            db.salva_produtos_banco(tuple(lista))

        db.fecha_conexao()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Atualização de protudo")
        msg.setText("Produto atualizado com sucesso! ")
        # start the app
        msg.exec()
        #reseta a tabela
        self.tabela_produtos.reset()
        self.atualiza_tabelas()    
    # preenche a tabela usuario
    def tabelaUsuario(self):
        db = DataBase()
        db.conecta()
        lista = db.tabela_usuario()

        self.tabela_usuario.clearContents()
        self.tabela_usuario2.clearContents()
        self.tabela_usuario.setRowCount(len(lista))
        self.tabela_usuario2.setRowCount(len(lista))

        for linha, texto in enumerate (lista):
            for coluna, dado in enumerate(texto):
                self.tabela_usuario.setItem(linha,coluna,QTableWidgetItem(str(dado)))
                self.tabela_usuario2.setItem(linha,coluna,QTableWidgetItem(str(dado)))
        db.fecha_conexao()


    #filtra por nome
    def filtro_nomeUsuario(self,texto):
        self.filtro(texto,1,self.tabela_usuario)
    #filtra por nome
    def filtro_idUsuario(self,texto):
        self.filtro(texto,0,self.tabela_usuario)    
    #filtra por nome
    def filtro_idUsuario2(self,texto):
        self.filtro(texto,0,self.tabela_usuario2)   
    #filtra por nome
    def filtro_nomeUsuario2(self,texto):
        self.filtro(texto,1,self.tabela_usuario2)    
    #filtro generico
    def filtro(self,filtro_texto,coluna,tabela):
        for i in range(tabela.rowCount()):
            for j in range(tabela.columnCount()):
                item = tabela.item(i, coluna)
                match = filtro_texto.lower() not in item.text().lower()
                tabela.setRowHidden(i, match)
                if not match:
                    break
    #filtra por nome
    def filtro_fornecedor(self,texto):
        self.filtro(texto,1,self.tabela_fornecedor)
    #filtra por nome
    def filtro_fornecedor2(self,texto):
        self.filtro(texto,1,self.tabela_fornecedor_2)
    #filtra por nome
    def filtro_CNPJ(self,texto):
        self.filtro(texto,0,self.tabela_fornecedor)
    #filtra por nome
    def filtro_CNPJ2(self,texto):
        self.filtro(texto,0,self.tabela_fornecedor_2)  
    #Cadastrar um fornecedor
  
    #preencher a tabela fornecedor
    def tabelaFornecedor(self):
        db = DataBase()
        db.conecta()
        lista = db.tabela_fornecedor()
        self.tabela_fornecedor.clearContents()
        self.tabela_fornecedor_2.clearContents()
        self.tabela_fornecedor.setRowCount(len(lista))
        self.tabela_fornecedor_2.setRowCount(len(lista))

        for linha, texto in enumerate(lista):
            for coluna , dado in enumerate (texto):
                self.tabela_fornecedor.setItem(linha,coluna,QTableWidgetItem(str(dado)))
                self.tabela_fornecedor_2.setItem(linha,coluna,QTableWidgetItem(str(dado)))




        db.fecha_conexao()    

    #Altera um fornecedor
    def alterar_fornecedor(self):
        dados = []
        atualidaDados = []
       
        for linha in range(self.tabela_fornecedor_2.rowCount()): #conta nmr de linhas
            for coluna in range(self.tabela_fornecedor_2.columnCount()): # conta numero de colunas
                dados.append(self.tabela_fornecedor_2.item(linha, coluna).text()) # adiciono pesquina na lista dados

            atualidaDados.append(dados)
            dados =[]
        self.atualiza_tabelas()
        # atualizar dados no banco

        db = DataBase()
        db.conecta()

        for lista in atualidaDados:
            db.editar_fornecedor(tuple(lista))

        db.fecha_conexao()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Atualização de protudo")
        msg.setText("Produto atualizado com sucesso! ")
        # start the app
        msg.exec()
        #reseta a tabela
        self.tabela_produtos.reset()
        self.atualiza_tabelas()    
    # colori a tela pela quantidade de estoque
    def colorir(self,tabela):
     
        for linha in range (tabela.rowCount()):
            for coluna in range(tabela.columnCount()):
                item = tabela.item(linha,2).text()
                
                valor = int(item)
                if valor < 3:
                    tabela.item(linha, coluna).setBackground(QtGui.QColor(255,171,175))
                elif valor < 5:
                    tabela.item(linha, coluna).setBackground(QtGui.QColor(255,253,3))
                else:
                    tabela.item(linha, coluna).setBackground(QtGui.QColor(87,211,102))    
    # esconder usuario
    def esconder_usuario(self):
        self.frame_menu_vendas.setMinimumHeight(0)
        self.frame_menu_pecas.setMinimumHeight(0)           
    # esconde fornecedor
    def esconder_fornecedor(self):
        self.frame_menu_pecas.setMinimumHeight(0)
        self.frame_menu_outros.setMinimumHeight(0)    
    # esconde protudo
    def esconder_produtos(self):
        vendas = self.frame_menu_vendas.setMinimumHeight(0)
        outros = self.frame_menu_outros.setMinimumHeight(0)   
    # relogio Hora
    def relogio(self):
            anima = Relogio()
            hora = anima.relogio()
            return self.label_23.setText(hora)
    # Relogio Data
    def data(self):
            anima = Relogio()
            data = anima.data()
            return self.label_32.setText(data)
                    
    def alimenta_tela_venda(self):
        db = DataBase()
        db.conecta()
        id = self.cod_iten.text()
        lista = db.alimenta_itens(id)
        


        for linha in lista:
            nome = linha[0]
            valor = linha[1]
            cod = linha[2]
            qtd_estoque = linha[3]

            valor = str(valor)
            valorString = valor.replace(".",",")

            self.nome_produto.setText(nome)
            self.valor_produto.setText(valorString)
            return nome, valor, cod, qtd_estoque

    def calculo(self):
        nome = self.nome_produto.text()
        valor = self.valor_produto.text()
        valor = valor.replace(",",".")
        valor = float(valor)

        qts = self.quantidade_produto_2.text()
        desconto = self.valor_desconto.text()
        desconto = desconto.replace(",",".")
        if desconto == '':
            desconto = 0
            
        des = float(desconto)
        
        if des == 0:
            qts = int(qts)
            total = float(valor * qts)
            texto = (f"{total:_.2f}")
            texto = texto.replace('.',',').replace('_','.')
            
        elif des != 0:
            qts = int(qts)
            total =  qts * (valor - (valor / 100 * des))
            texto = (f'{total:_.2f}')
            texto = texto.replace('.',',').replace('_','.')
            
            
        valor_sem  = valor * qts
        valor_sem  = (f'{valor_sem:_.2f}').replace('.',',').replace('_','.')
        
        valor = (f'{valor:_.2f}').replace('.',',').replace('_','.')
        desconto = (f'{des:_.2f}').replace('.',',').replace('_','.')
        lista = [nome,qts,valor,texto,valor_sem,desconto]

        return lista 
    
    def alimenta_tabela_vendas(self):
        lista = self.calculo()
        list = self.alimenta_tela_venda()
        
        

        if list[3] >= lista[1]:

            linha = self.table_produtos_vendas.rowCount()
            self.table_produtos_vendas.insertRow(linha)
            self.table_produtos_vendas.setItem(linha, 0, QTableWidgetItem(str(list[2])))
            self.table_produtos_vendas.setItem(linha, 1, QTableWidgetItem(str(lista[0])))
            self.table_produtos_vendas.setItem(linha, 2, QTableWidgetItem(str(lista[1])))
            self.table_produtos_vendas.setItem(linha, 3, QTableWidgetItem(str(lista[2])))
            self.table_produtos_vendas.setItem(linha, 4, QTableWidgetItem(str(lista[3])))
            self.table_produtos_vendas.setItem(linha, 5, QTableWidgetItem(str(lista[4])))
            self.table_produtos_vendas.setItem(linha, 6, QTableWidgetItem(str(lista[5])))

            self.limpa_campo()
            self.table_produtos_vendas.resizeColumnsToContents()
            self.total()
            self.cod_iten.clear()
        else:
            mgs = QMessageBox()
            mgs.setIcon(QMessageBox.Warning)
            mgs.setWindowTitle("Erro")
            mgs.setText(f'A quantidade  é maior que no estoque, disponivel no estoque é de {list[3]} unidades')
            mgs.exec()
            self.quantidade_produto_2.clear()
            self.cod_iten.clear()
               
    
    def deleta_campo(self):

        linha = self.table_produtos_vendas.currentRow()
        if linha < 0:
            return QMessageBox.warning(self, 'ERRO','Necessario selecionar o que deseja remover da lista')
        
        botao = self.btn_removeItemVenda 
        botao = QMessageBox.question(
            self,
            'confirmação',
            'Tem certeza que deseja excluir o item selecionado?',
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No)
        
        if botao == QMessageBox.StandardButton.Yes:
            self.table_produtos_vendas.removeRow(linha) 

    def somar_valores(self):

        db = DataBase()
        db.conecta()

        

        col = self.table_produtos_vendas.columnCount()
        qtds = []
        codigo = []
        for row in range(self.table_produtos_vendas.rowCount()):
            cod =self.table_produtos_vendas.item(row, 0)
            qts = self.table_produtos_vendas.item(row, 2)
            quanti = int(qts.text())
            codi = int(cod.text())
            codigo.append(codi)
            qtds.append(quanti)


        linha = row
        i = 0
        while(i <= linha):
            id = codigo[i]
          #  print(f'esse é  o id {id}  \n \n')
            dados = db.edita_qtds(id)

            lista = list(map(list, dados))
        
            valor = lista[0]
            valor = valor[0]
            
            total =  valor - qtds[i]
            
            
            db.atualiza_quantidade(id,total)
            self.atualiza_tabelas()


            
            i+=1
        db.fecha_conexao()

        mgs = QMessageBox()
        mgs.setIcon(QMessageBox.Information)
        mgs.setWindowTitle("Vendido")
        mgs.setText("Item Vendido com Sucesso ")
        mgs.exec()
        self.limpa_campo()

    def total(self):
         
        col = self.table_produtos_vendas.columnCount()
        valor_sem = []
        valor_com = []
        
        for row in range(self.table_produtos_vendas.rowCount()):
            # pega na tabela o valor com desconto
            valor_c =self.table_produtos_vendas.item(row, 4)
            # pega na tabela o valor sem desconto
            valor_s = self.table_produtos_vendas.item(row, 5)

            # converte os valores em float
            v_com = valor_c.text().replace('.','').replace(',','.')
            v_sem = valor_s.text().replace('.','').replace(',','.')
            tex = float(v_sem)
            text = float(v_com)
            # adiciona os valores em uma lista ( .append é comando de adicionar na lista ) 
            valor_sem.append(tex)
            valor_com.append(text)
            a = 0       
            i = 0
            # cria um for pra somas as linhas da tabela na parte de valores
            for valor in valor_sem:
                i += valor
                result = str(f'{i:_.2f}').replace('.',',').replace('_','.')
            self.total_s_desconto.setText(result)

            for valo in valor_com:
                
                a += valo
                result = str(f'{a:_.2f}').replace('.',',').replace('_','.')
                

            self.total_c_desconto.setText(result)


class Limpa(MainWindow):
        # limpar os campos
    def limpa_campo(self):
        #Tabela cadastrar
        self.cadastrar_nome.clear()
        self.cadastrar_marca.clear()
        self.cadastrar_valor_custo.clear()
        self.cadastrar_lavor_venda.clear()
        self.cadastrar_descricao.clear()
        self.cadastrar_quantidade.clear()
        
        #usuario
        self.user_nome.clear()
        self.user_usuario.clear()
        self.user_senha.clear()
        self.user_repetirSenha.clear()

        #tabela excluir
        self.nome_excluir.clear()
        self.marca_excluir.clear()
        self.valor_custo_excluir.clear()
        self.valor_venda_excluir.clear()
        self.descricao_excluir.clear()
        self.quantidade_excluir.clear()
        self.codigo_excluir.clear()  

        self.nome_produto.clear()
        self.valor_produto.clear()
        self.quantidade_produto_2.clear()
        self.valor_desconto.clear()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec()