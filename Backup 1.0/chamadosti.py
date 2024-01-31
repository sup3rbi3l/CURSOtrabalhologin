from hashlib import scrypt
import logging
import warnings
from flask import Flask, redirect, render_template, request, url_for,flash,session
import mysql.connector

#Esta linha cria uma nova conexão com o servidor MySQL usando a biblioteca mysql.connector. A conexão é armazenada na variável cnx
cnx = mysql.connector.connect(
  host='127.0.0.1',# Endereço IP do servidor MySQL (neste caso, o servidor local)
  user='root',# Nome de usuário para a conexão
  password=''# Senha para o usuário especificado
)

# Executar a instrução SQL para verificar se o banco de dados existe
cursor = cnx.cursor()
cursor.execute('SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = "chamadosti";')

# Obter o número de resultados
num_results = cursor.fetchone()[0]

# Fechar a conexão com o banco de dados
cnx.close()

# Se o número de resultados for maior que zero, o banco de dados existe
if num_results > 0:
  print('O banco de dados agenda existe e esta pronto para uso.')
else:
    # Conectar-se ao servidor MySQL para criar o banco de dados
    cnx = mysql.connector.connect(
        host='127.0.0.1',# Endereço IP do servidor MySQL (neste caso, o servidor local)
        user='root',# Nome de usuário para a conexão
        password=''# Senha para o usuário especificado
    )

    # Criar o banco de dados chamadosti
    cursor = cnx.cursor()
    cursor.execute('CREATE DATABASE chamadosti;')
    cnx.commit()

    # Conectar-se ao banco de dados agenda recém-criado
    cnx = mysql.connector.connect(
        host='127.0.0.1',# Endereço IP do servidor MySQL (neste caso, o servidor local)
        user='root',# Nome de usuário para a conexão
        password='',# Senha para o usuário especificado
        database='chamadosti'  # Especificar o banco de dados
    )
    cursor = cnx.cursor()
# Cria um cursor para a conexão com o banco de dados.
# O cursor é um objeto que permite executar instruções SQL no banco de dados.

    cursor.execute('CREATE TABLE usuarios (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), email VARCHAR(255),senha VARCHAR(255));')
# Cria a tabela `usuarios` com a chave primária `id` e as seguintes colunas:
# * `id`: ID do usuário.
# * `nome`: Nome do usuário.
# * `email`: Endereço de e-mail do usuário.
# * `senha`: Senha do usuário.
#
# A tabela `usuarios` armazena informações sobre os usuários do sistema.

    cursor.execute("""
      CREATE TABLE chamados (id INT AUTO_INCREMENT PRIMARY KEY,
      numero	int,
      data_abertura datetime,
      data_fechamento datetime,
      status varchar(20),
      prioridade varchar(20),
      tipo_problema varchar(20),
      descricao VARCHAR(500),
      solucao VARCHAR(500),
      usuario_id int,
      tecnico_id int,
      equipamento_id int,
      aplicativo_id int
    )
  """)  
# Cria a tabela `chamados` com a chave primária `id` e as seguintes colunas:
# * `id`: ID do chamado.
# * `numero`: Número do chamado.
# * `data_abertura`: Data de abertura do chamado.
# * `data_fechamento`: Data de fechamento do chamado.
# * `status`: Status do chamado.
# * `prioridade`: Prioridade do chamado.
# * `tipo_problema`: Tipo do problema.
# * `descricao`: Descrição do chamado.
# * `solucao`: Solução do chamado.
# * `usuario_id`: ID do usuário que criou o chamado.
# * `tecnico_id`: ID do técnico que está trabalhando no chamado.
# * `equipamento_id`: ID do equipamento que está com o problema.
# * `aplicativo_id`: ID do aplicativo que está com o problema.
   
    cursor.execute('CREATE TABLE tecnicos(id INT AUTO_INCREMENT PRIMARY KEY, nome varchar(100),email varchar(100),telefone varchar(20),departamento varchar(50));')
# Cria a tabela `tecnicos` com a chave primária `id` e as seguintes colunas:
# * `id`: ID do tecnico.
# * `nome`: Nome do tecnico.
# * `email`: Endereço de e-mail do tecnico.
# * `senha`: Senha do tecnico.
#
# A tabela `tecnicos` armazena informações sobre os tecnicos do sistema do sistema.
    
    cursor.execute('CREATE TABLE equipamentos(id int AUTO_INCREMENT PRIMARY KEY,nome	varchar(100),modelo	varchar(50),numero_de_serie	varchar(50));')
# Cria a tabela `equipamentos` com a chave primária `id` e as seguintes colunas:
#
# * `id`: ID do equipamento.
# * `nome`: Nome do equipamento.
# * `modelo`: Modelo do equipamento.
# * `número de série`: Número de série do equipamento.
#
# A tabela `equipamentos` armazena informações sobre os equipamentos do sistema.
   
    
    
    
     
    cursor.execute('CREATE TABLE aplicativos(id int AUTO_INCREMENT PRIMARY KEY,nome	varchar(100),versao	varchar(10));')
# Cria a tabela `aplicativos` com a chave primária `id` e as seguintes colunas:
#
# * `id`: ID do aplicativo.
# * `nome`: Nome do aplicativo.
# * `versão`: Versão do aplicativo.
#
# A tabela `aplicativos` armazena informações sobre os aplicativos do sistema.


#cursor.execute('ALTER TABLE chamados ADD CONSTRAINT fk_chamados_usuarios FOREIGN KEY (usuario_id) REFERENCES usuarios (id),ADD CONSTRAINT fk_chamados_tecnicos FOREIGN KEY (tecnico_id) REFERENCES tecnicos (id),ADD CONSTRAINT fk_chamados_equipamentos FOREIGN KEY (equipamento_id) REFERENCES equipamentos (id),ADD CONSTRAINT fk_chamados_aplicativos FOREIGN KEY (aplicativo_id) REFERENCES aplicativos (id)')
# Adiciona os relacionamentos entre as tabelas `chamados` e `usuarios`, `equipamentos`, `tecnicos` e `aplicativos`.
#
# Os relacionamentos são definidos da seguinte forma:
#
# * `usuario_id` na tabela `chamados` refere-se a `id` na tabela `usuarios`.
# * `tecnico_id` na tabela `chamados` refere-se a `id` na tabela `tecnicos`.
# * `equipamento_id` na tabela `chamados` refere-se a `id` na tabela `equipamentos`.
# * `aplicativo_id` na tabela `chamados` refere-se a `id` na tabela `aplicativos`.
#
# Esses relacionamentos garantem a integridade referencial entre as tabelas.
    cnx.close()
# Fecha a conexão com o banco de dados.
# Essa linha de código é importante para liberar os recursos do banco de dados e evitar vazamentos de memória.    
 


app = Flask(__name__)
app.config['SECRET_KEY']='TESTE'

# Cria uma instância da classe Flask.
# A classe Flask é a base para todas as aplicações Flask. Ela fornece um conjunto de métodos e propriedades que permitem criar e executar aplicações web.
# O argumento `__name__` é o nome do módulo atual. Ele é usado pelo Flask para determinar onde encontrar os templates, arquivos estáticos e outros recursos da aplicação.
# Por exemplo, se o código está sendo executado no módulo `my_app`, o Flask irá procurar os templates no diretório `my_app/templates` e os arquivos estáticos no diretório `my_app/static`.

# Define uma rota para a URL '/login', permitindo tanto requisições POST quanto GET.
@app.route('/',methods=['POST','GET'])
def pagina_login():
     # Limpa os dados da sessão
     session.clear()
      # Limpa o cookie do ID do usuário
     session.pop('usuario_id', None)
     # Renderiza o template 'login.html' e retorna a página HTML gerada.
     return render_template("login.html")

#Requisição POST: Método HTTP usado para enviar dados para um servidor. Os dados são enviados no corpo da requisição, e o servidor pode processá-los como quiser. 
#É frequentemente usada para criar novos recursos ou enviar dados para processamento.

#Requisição GET: Método HTTP usado para obter dados de um servidor. Os dados são enviados na URL, e o servidor pode processá-los como quiser. 
#É frequentemente usada para obter informações de um recurso, como uma lista de itens ou os detalhes de um item.







# Define uma rota para a URL '/paginainicial'.
@app.route('/paginainicial')

def pagina_inicial():
     if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    # Renderiza o template 'paginainicial.htmlp' e retorna a página HTML gerada.
     return render_template("paginainicial.html")
   
   
   
@app.route('/chamados')
def pagina_chamados():
  if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
  cnx = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='chamadosti'  # Especificar o banco de dados
    )
  cursor = cnx.cursor()
  cursor.execute('SELECT * FROM chamados')
  chamados = cursor.fetchall()

  return render_template("chamados.html", chamados=chamados)


@app.route('/usuarios')
def pagina_usuarios():
  if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
  cnx = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='chamadosti'  # Especificar o banco de dados
    )
  cursor = cnx.cursor()
  cursor.execute('SELECT * FROM usuarios')
  usuarios = cursor.fetchall()

  return render_template("usuarios.html", usuarios=usuarios)


# Define a rota '/cadastro', permitindo tanto requisições POST quanto GET.
@app.route('/cadastro', methods=["POST","GET"])
def abre_cadastro():
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    return render_template("cadastro.html")




@app.route('/add_cadastro', methods=["POST","GET"])
def cadastro():
  if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
  # Obtém os valores dos campos "nome", "email" e "senha" do formulário submetido via POST.
  nome = request.form.get('nome')
  email = request.form.get('email')
  senha = request.form.get('senha')

   # Validação
  if not nome:
     flash('O nome é obrigatório.')
     return render_template('cadastro.html')
  if not email:
     flash('O e-mail é obrigatório.')
     return render_template('cadastro.html')
  if not senha:
    flash('A senha é obrigatória.')
    return render_template('cadastro.html')        
  # Abre uma conexão com o banco de dados MySQL usando as credenciais especificadas.
  cnx = mysql.connector.connect(
      host='127.0.0.1',
      user='root',
      password='',
      database='chamadosti'
      )
  # Cria um cursor para executar consultas no banco de dados.    
  cursor = cnx.cursor()
          
  # Executa uma consulta SQL para verificar se já existe um usuário com o email informado.
  cursor.execute("""
    SELECT COUNT(*)
    FROM usuarios
    WHERE email = %s;
    """, (email,))
          
  # Obtém o resultado da consulta (o número de usuários encontrados).
  existe = cursor.fetchone()[0]
        
  # Fecha o cursor e a conexão com o banco de dados.
  cursor.close()
  cnx.close()
  # Se a consulta anterior retornou um valor maior que zero (usuário já existe), renderiza o template 'cadastro.html' novamente, passando uma mensagem de erro.
  if existe > 0:
    flash('Email já cadastrado')
    return render_template('cadastro.html')
  else:
    try:
      # Reabre a conexão com o banco.
      cnx = mysql.connector.connect(
          host='127.0.0.1',
          user='root',
          password='',
          database='chamadosti'
          )
      cursor = cnx.cursor()
                
      # Prepara a consulta SQL de inserção.
      sql = 'INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)'
      values = (nome, email, senha)

      # Executa a consulta com os valores obtidos do formulário.
      cursor.execute(sql, list(values))
      # Fecha o cursor e confirma a transação (commit).
      cursor.close()
      cnx.commit()

      # Redireciona para a página inicial.
      return redirect(url_for('pagina_usuarios'))
    # Se ocorrer um erro de banco de dados, renderiza o template 'cadastro.html' novamente, passando a mensagem de erro SQL.
    except mysql.connector.Error as e:   
            return render_template('cadastro', error=str(e)) 
          
          # Se o usuário não existe, tenta inserir o novo usuário no banco de dados:   
 
    
    
    
    
         
   
@app.route('/excluir_usuario/<id>', methods=['GET', 'POST'])
def excluir_usuario(id):
    # Validar o ID
    if not id.isdigit():
        return render_template('excluir-usuario.html', error='ID inválido')
    # Executando a exclusão
    try:
        cnx = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='chamadosti'
        )
        cursor = cnx.cursor()
        cursor.execute("""
            DELETE FROM usuarios
            WHERE id = %s;
        """, (id,))
        cursor.close()
        cnx.commit()

        return redirect(url_for('pagina_usuarios'))
    except mysql.connector.Error as e:
        return render_template('excluir-usuario.html', error=str(e))
   
@app.route('/editarusuario/<id>', methods=['GET', 'POST'])
def atualizarusuario(id):

    # Valida o ID do usuário
    if not id.isdigit():
        return render_template('editarusuario/<id>', error='ID inválido.')

    # Obtém os dados do usuário do banco de dados
    cnx = mysql.connector.connect( host='127.0.0.1',
            user='root',
            password='',
            database='chamadosti')
    cursor = cnx.cursor()
    cursor.execute("""
        SELECT id, nome, email
        FROM usuarios
        WHERE id = %s;
    """, (id,))
    dados_usuario = cursor.fetchone()
    cursor.close()
    cnx.close()

    # Processa o formulário
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        # Valida o input
        if not nome:
            flash('O nome é obrigatório.')
            return render_template('editarusuario/<id>', dados_usuario=dados_usuario)
        if not email:
            flash('O e-mail é obrigatório.')
            return render_template('editarusuario/<id>', dados_usuario=dados_usuario)
        if not email:
            flash('A senha é obrigatório.')
            return render_template('editarusuario/<id>', dados_usuario=dados_usuario)
        # Realiza a atualização no banco de dados
        cnx = mysql.connector.connect( host='127.0.0.1',
            user='root',
            password='',
            database='chamadosti')
        cursor = cnx.cursor()
        sql = 'UPDATE usuarios SET nome = %s, email = %s, senha=%s WHERE id = %s;'
        values = (nome, email, senha, id)
        cursor.execute(sql, values)
        cnx.commit()
        cursor.close()
        cnx.close()

        # Redireciona para a página inicial
        return redirect(url_for('pagina_inicial'))

    # Exibe o formulário
    return render_template('editarusuario.html', id=id, dados_usuario=dados_usuario)





@app.route('/validalogin', methods=['POST', 'GET'])
def login():
  
  email = request.form.get('email')
  senha = request.form.get('senha')

  # Validar as credenciais
  cnx = mysql.connector.connect(
     host='127.0.0.1',
     user='root',
     password='',
     database='chamadosti'
     )
  cursor = cnx.cursor()
  cursor.execute("""
            SELECT *
            FROM usuarios
            WHERE email = %s AND senha = %s;
        """, (email, senha,))
  usuario = cursor.fetchone()
  cursor.close()
  cnx.close()

  if usuario:
  # Login bem-sucedido
   session['usuario_id'] = usuario[0]
   return redirect(url_for('pagina_usuarios'))
  else:
    # Login inválido
    
    return redirect(url_for('pagina_login'))

  
   
    

if __name__ == '__main__':
      app.run