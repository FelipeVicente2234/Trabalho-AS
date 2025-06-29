from dataclasses import dataclass

@dataclass
class Livro:
    codigo: str
    titulo: str
    autor: str
    ano: int
    genero: str
    quantidade: int
    disponiveis: int 

@dataclass
class Usuario:
    id_usuario: str
    nome: str
    tipo: str

@dataclass
class Emprestimo:
    id_usuario: str
    codigo_livro: str
    dia_emprestimo: int
    dia_devolucao_prevista: int 
    status: str
    dia_devolucao_efetiva: int = 0 

class Biblioteca:
    def __init__(self):
        self.livros = {}
        self.usuarios = {}
        self.emprestimos = []
        self.dia_sistema_atual = 1 
        self.multa_por_dia = 1.00

    def cadastrar_livro(self, codigo, titulo, autor, ano, genero, quantidade):
        if codigo in self.livros:
            print(f"Erro: Livro com código {codigo} já existe.")
            return False

        livro_novo = Livro(codigo, titulo, autor, ano, genero, quantidade, quantidade)
        self.livros[codigo] = livro_novo
        print(f"Livro '{titulo}' cadastrado com sucesso.")
        return True

    def listar_todos_livros(self):
        if not self.livros:
            print("Nenhum livro cadastrado.")
            return
        print("\n=== Livros Cadastrados ===")
        for livro in self.livros.values():
            print(f"Código: {livro.codigo}")
            print(f"Título: {livro.titulo}")
            print(f"Autor: {livro.autor}")
            print(f"Ano: {livro.ano}")
            print(f"Gênero: {livro.genero}")
            print(f"Total: {livro.quantidade}")
            print(f"Disponível: {livro.disponiveis}")
            print("=========================")

    def buscar_livros(self, termo_busca):
        resultados = [
            livro for livro in self.livros.values()
            if termo_busca.lower() in livro.codigo.lower() or
               termo_busca.lower() in livro.titulo.lower() or
               termo_busca.lower() in livro.autor.lower()
        ]

        if not resultados:
            print(f"Nenhum livro encontrado para '{termo_busca}'.")
            return []

        print(f"\n=== Resultados da busca para '{termo_busca}' ===")
        for livro in resultados:
            print(f"Código: {livro.codigo}")
            print(f"Título: {livro.titulo}")
            print(f"Autor: {livro.autor}")
            print(f"Ano: {livro.ano}")
            print(f"Gênero: {livro.genero}")
            print(f"Total: {livro.quantidade}")
            print(f"Disponível: {livro.disponiveis}")
            print("=========================")
        return resultados

    def cadastrar_usuario(self, id_usuario, nome, tipo): 
        if id_usuario in self.usuarios:
            print(f"Erro: Usuário com ID {id_usuario} já existe.")
            return False
        if tipo.lower() not in ["aluno", "professor"]:
            print("Erro: Tipo de usuário incorreto. Deve selecionar 'aluno' ou 'professor'.")
            return False

        novo_usuario = Usuario(id_usuario, nome, tipo.lower())
        self.usuarios[id_usuario] = novo_usuario
        print(f"Usuário '{nome}' ({tipo}) cadastrado com sucesso.")
        return True

    def listar_todos_usuarios(self):
        if not self.usuarios:
            print("Nenhum usuário cadastrado.")
            return
        print("\n=== Usuários Cadastrados ===")
        for usuario in self.usuarios.values():
            print(f"ID: {usuario.id_usuario}")
            print(f"Nome: {usuario.nome}")
            print(f"Tipo: {usuario.tipo.capitalize()}")
            print("==========================")

    # Métodos para Gerenciamento de Tempo
    def avancar_dias(self, dias):
        if dias > 0:
            self.dia_sistema_atual += dias
            print(f"Sistema avançou {dias} dias. Novo dia: {self.dia_sistema_atual}.")
        else:
            print("Por favor, insira um número positivo de dias.")

    def consultar_dia_atual(self):
        print(f"O dia atual do sistema é: {self.dia_sistema_atual}.")

    # Gerenciamento de Empréstimos
    def realizar_emprestimo(self, id_usuario, codigo_livro): 
        usuario_encontrado = self.usuarios.get(id_usuario)
        if not usuario_encontrado:
            print(f"Erro: Usuário com ID {id_usuario} não encontrado.")
            return False
        livro_encontrado = self.livros.get(codigo_livro)
        if not livro_encontrado:
            print(f"Erro: Livro com código {codigo_livro} não encontrado.")
            return False

        if livro_encontrado.disponiveis <= 0: 
            print(f"Erro: Livro '{livro_encontrado.titulo}' não disponível para empréstimo.")
            return False

        prazo = 7 if usuario_encontrado.tipo == "aluno" else 10
        dia_devolucao_prevista = self.dia_sistema_atual + prazo

        novo_emprestimo = Emprestimo(
            id_usuario=id_usuario,
            codigo_livro=codigo_livro,
            dia_emprestimo=self.dia_sistema_atual,
            dia_devolucao_prevista=dia_devolucao_prevista,
            status="ativo"
        )
        self.emprestimos.append(novo_emprestimo)
        livro_encontrado.disponiveis -= 1 
        print(f"Empréstimo do livro '{livro_encontrado.titulo}' para o usuário '{usuario_encontrado.nome}' realizado com sucesso. Devolução prevista para o dia {dia_devolucao_prevista}.")
        return True

    def realizar_devolucao(self, id_usuario, codigo_livro):
        emprestimo_encontrado = None
        for emp in self.emprestimos:
            if emp.id_usuario == id_usuario and emp.codigo_livro == codigo_livro and emp.status == "ativo": 
                emprestimo_encontrado = emp
                break

        if not emprestimo_encontrado:
            print(f"Erro: Nenhum empréstimo ativo encontrado para o usuário {id_usuario} e livro {codigo_livro}.")
            return False

        emprestimo_encontrado.dia_devolucao_efetiva = self.dia_sistema_atual
        emprestimo_encontrado.status = "devolvido"

        livro_devolvido = self.livros.get(codigo_livro)
        if livro_devolvido:
            livro_devolvido.disponiveis += 1 #

        multa = 0
        if emprestimo_encontrado.dia_devolucao_efetiva > emprestimo_encontrado.dia_devolucao_prevista:
            dias_atraso = emprestimo_encontrado.dia_devolucao_efetiva - emprestimo_encontrado.dia_devolucao_prevista
            multa = dias_atraso * self.multa_por_dia 
            print(f"Devolução realizada com {dias_atraso} dias de atraso. Multa a ser paga: R${multa:.2f}.")
        else:
            print("Devolução sem dias de atraso. Nenhuma multa a ser paga.")
        print(f"Devolução do livro '{livro_devolvido.titulo}' pelo usuário '{id_usuario}' registrada com sucesso.")
        return True 

    # Métodos para Relatórios
    def relatorio_livros_emprestados_atualmente(self):
        encontrados = False
        print("\n=== Livros Emprestados Atualmente ===")
        for emp in self.emprestimos:
            if emp.status == "ativo":
                encontrados = True
                livro_info = self.livros.get(emp.codigo_livro)
                usuario_info = self.usuarios.get(emp.id_usuario) 
                titulo_livro = livro_info.titulo if livro_info else "Desconhecido"
                nome_usuario = usuario_info.nome if usuario_info else "Desconhecido"

                print(f"Livro: {titulo_livro}")
                print(f"Usuário: {nome_usuario}")
                print(f"Devolução prevista: dia {emp.dia_devolucao_prevista}")
                print("=============================")

        if not encontrados:
            print("Nenhum livro em empréstimo atualmente.")

    def relatorio_livros_em_atraso(self):
        encontrados = False
        print("\n=== Livros com Devolução em Atraso ===")
        for emp in self.emprestimos:
            if emp.status == "ativo" and emp.dia_devolucao_prevista < self.dia_sistema_atual:
                encontrados = True
                livro_info = self.livros.get(emp.codigo_livro)
                usuario_info = self.usuarios.get(emp.id_usuario) 
                titulo_livro = livro_info.titulo if livro_info else "Desconhecido"
                nome_usuario = usuario_info.nome if usuario_info else "Desconhecido"
                dias_atraso = self.dia_sistema_atual - emp.dia_devolucao_prevista
                multa_estimada = dias_atraso * self.multa_por_dia

                print(f"Livro: {titulo_livro}")
                print(f"Usuário: {nome_usuario}")
                print(f"Devolução prevista: dia {emp.dia_devolucao_prevista}")
                print(f"Dias atrasados: {dias_atraso}")
                print(f"Multa estimada: R${multa_estimada:.2f}")
                print("===========================")
        if not encontrados:
            print("Nenhum livro com atraso encontrado.")

    # Menus de Interação
    def menu_gerenciar_livros(self):
        while True:
            print("\n=== Gerenciamento de Livros ===")
            print("1. Cadastrar novo livro")
            print("2. Listar todos os livros")
            print("3. Buscar livros")
            print("4. Voltar ao menu principal")

            opcao = input("Escolha uma opção: ")
            if opcao == '1':
                codigo = input("Código do livro: ")
                titulo = input("Título: ")
                autor = input("Autor: ")
                while True:
                    try:
                        ano = int(input("Ano de publicação: "))
                        break
                    except ValueError:
                        print("Ano inválido. Por favor, insira um número.")
                genero = input("Gênero: ")
                while True:
                    try:
                        quantidade = int(input("Quantidade total de exemplares: "))
                        if quantidade > 0:
                            break
                        else:
                            print("A quantidade deve ser um número maior que 0.")
                    except ValueError:
                        print("Quantidade inválida. Por favor, digite um número.")
                self.cadastrar_livro(codigo, titulo, autor, ano, genero, quantidade)
            elif opcao == '2':
                self.listar_todos_livros()
            elif opcao == '3':
                termo = input("Digite o código, título ou autor para buscar: ")
                self.buscar_livros(termo) 
            elif opcao == '4':
                print("Retornando ao menu principal.")
                break
            else:
                print("Opção inválida. Digite um número de 1 a 4.")

    def menu_gerenciar_usuarios(self):
        while True:
            print("\n=== Gerenciamento de Usuários ===")
            print("1. Cadastrar novo usuário")
            print("2. Listar todos os usuários cadastrados")
            print("3. Voltar ao menu principal")

            opcao = input("Escolha uma opção: ")
            if opcao == '1':
                id_usuario = input("ID do usuário: ")
                nome = input("Nome do usuário: ")
                tipo = input("Tipo (aluno/professor): ")
                self.cadastrar_usuario(id_usuario, nome, tipo)
            elif opcao == '2':
                self.listar_todos_usuarios()
            elif opcao == '3':
                print("Retornando ao menu principal.")
                break
            else:
                print("Opção inválida. Tente novamente.")

    def menu_gerenciar_tempo(self):
        while True:
            print("\n=== Gerenciamento de Tempo ===")
            print(f"Dia atual do sistema: {self.dia_sistema_atual}")
            print("1. Avançar 1 dia")
            print("2. Avançar 7 dias")
            print("3. Avançar N dias")
            print("4. Consultar dia atual")
            print("5. Voltar ao Menu principal")

            opcao_tempo = input("Escolha uma opção: ")

            if opcao_tempo == '1':
                self.avancar_dias(1)
            elif opcao_tempo == '2':
                self.avancar_dias(7)
            elif opcao_tempo == '3':
                try:
                    n_dias = int(input("Quantos dias você deseja avançar? "))
                    if n_dias > 0:
                        self.avancar_dias(n_dias)
                    else:
                        print("Por favor, insira um número positivo de dias.")
                except ValueError:
                    print("Entrada inválida. Por favor, insira um número.")
            elif opcao_tempo == '4':
                self.consultar_dia_atual()
            elif opcao_tempo == '5':
                print("Retornando ao menu principal.")
                break
            else:
                print("Opção inválida, tente novamente.")

    def menu_relatorios(self): 
        while True:
            print("\n=== Relatórios ===")
            print("1. Livros emprestados atualmente")
            print("2. Livros com devolução em atraso")
            print("3. Voltar ao menu principal")

            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                self.relatorio_livros_emprestados_atualmente()
            elif opcao == '2':
                self.relatorio_livros_em_atraso()
            elif opcao == '3':
                print("Retornando ao menu principal.")
                break
            else:
                print("Opção inválida, tente novamente.")

    def main_menu(self):
        while True:
            print("\n=== Menu Principal do Sistema de Gerenciamento de Biblioteca ===")
            print("1. Gerenciar Livros")
            print("2. Gerenciar Usuários")
            print("3. Realizar Empréstimos")
            print("4. Realizar Devolução")
            print("5. Relatórios")
            print("6. Gerenciar o Tempo")
            print("7. Sair")

            opcao_principal = input("Escolha uma opção: ")

            if opcao_principal == '1':
                self.menu_gerenciar_livros()
            elif opcao_principal == '2':
                self.menu_gerenciar_usuarios()
            elif opcao_principal == '3':
                id_usuario = input("ID do usuário: ")
                codigo_livro = input("Código do livro: ")
                self.realizar_emprestimo(id_usuario, codigo_livro)
            elif opcao_principal == '4':
                id_usuario = input("ID do usuário: ")
                codigo_livro = input("Código do livro: ")
                self.realizar_devolucao(id_usuario, codigo_livro)
            elif opcao_principal == '5':
                self.menu_relatorios()
            elif opcao_principal == '6':
                self.menu_gerenciar_tempo()
            elif opcao_principal == '7':
                print("Saindo do sistema. Até mais!")
                break
            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    biblioteca = Biblioteca()
    biblioteca.main_menu()