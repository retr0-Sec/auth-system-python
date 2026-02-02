import json
import os
import re
import logging
from time import sleep
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # src/
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

arq = "users.json"  # Arquivo JSON usado para simular um banco de dados.

usuario_logado = None
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "system.logs"),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO
)

def salvar_usuarios(dados):
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def Sala():
    print("""
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣴⣶⣶⣶⣦⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣴⣶⣶⣶⣦⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⣿⣿⡿⠿⠛⠛⠛⠛⠛⠻⠿⢿⣿⣷⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⡿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠿⣷⣄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⣾⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣷⡄⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣧⠀⠀
⠀⠀⠀⠀⠀⠀⣾⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣷⠀
⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡇
⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀⠀⠀⠀⢀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡇
⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀⠀⣠⣶⣿⡿⠟⠛⠉⠉⠉⠉⠉⠉⠉⠛⠻⢿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡇
⠀⠀⠀⠀⠀⠘⣿⣿⣆⠀⣴⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⢿⣷⣦⠀⠀⠀⠀⠀⣸⣿⣿⠃
⠀⠀⠀⠀⠀⠀⠈⠻⢿⣿⣿⠟⠁⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠉⠻⢿⣿⣶⣶⡿⠟⠋⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⣠⣴⣶⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣿⡿⠟⠛⠉⠉⠉⠉⠉⠉⠛⠻⢿⣿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠿⣷⣄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣷⣦⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣾⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣷⣆⠀
⠀⠀⠀⠀⠀⣠⣾⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣷

    """)


# Carrega o JSON de usuarios
def carregar_usuarios():
    logging.info("Banco de Usuarios carregado.")
    try:
        with open(arq, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.warning(f"Erro no JSON: {e}")
        return {}

def pode_ver_logs(usuario):
    if not usuario:
        return False
    if usuario["role"] != "admin":
        return False
    return True

def ver_logs(usuario):
    if not pode_ver_logs(usuario):
        print("ACESSO NEGADO!!")
        logging.warning(
            f"Tentativa de acesso aos logs por "
            f"{usuario['username'] if usuario else 'desconhecido'}"
        )
        return
    caminho_log = os.path.join(LOG_DIR, "system.logs")
    with open(caminho_log,"r") as l:
        print(l.read())


def gerencia(usuario):
    if not pode_ver_logs(usuario):
        print("ACESSO NEGADO!!")
        logging.warning(
            f"Tentativa de acesso a gerencia por "
            f"{usuario['username'] if usuario else 'desconhecido'}"
        )
        return
    while True:
        print("===== GERENCIA DE USERS =====")
        hs = PasswordHasher()
        dados = carregar_usuarios()
        try:
            acoes = int(input("[1] Adicionar Usuarios\n[2] Excluir Usuarios\n[3] Gerenciar roles\n[4] Sair\nR: "))
        except Exception as e:
            print("Digite um numero valido!")
            continue
        if acoes == 1:
            nome_usuario = input("Digite o nome do usuario: ")
            senha_do_usuario = input("Digite a senha para o usuario: ").strip()
            validaSenha(senha_do_usuario)
            hash_senha = hs.hash(senha_do_usuario)  # Cria a hash da senha
            logging.info("Hash criado!")
            logging.info("Banco de usuarios carregados")
            if not nome_usuario in dados:
                cadastrar(nome_usuario, hash_senha)
            else:
                print("Não foi possivel registrar esse Usuario")
                logging.info("Nome de usuario já existente")
        if acoes == 2:
            name = input("Digite o nome do usuario: ").strip()
            confirmacao = input("Tem certeza que quer Excluir esse Usuario? ")
            if dados[name]["role"] == "admin":
                print("Não é possivel remover administradores!!")
                logging.warning(
                    f"Tentativa de remover administrador {name} feita pelo "
                    f"{usuario['username'] if usuario else 'desconhecido'}"
                )
                break
            if confirmacao in ("s", "sim", "y", "yes"):
                dados.pop(name,None)
                salvar_usuarios(dados)
            else:
                print("Interrompido")
                return
        if acoes == 3:
            print(list(dados.keys()))
            user = input("Digite o usuario que deseja alterar o role: ").strip()
            try:
                roles = int(input("[1] Admin [2] User\nR:"))
            except Exception as e:
                print("Erro, se oriente pelo indice!")
                continue
            if roles == 1:
                dados[user]["role"] = "admin"
                salvar_usuarios(dados)
            elif roles == 2:
                dados[user]["role"] = "user"
                salvar_usuarios(dados)
            else:
                print("Indice errado!!!")
        if acoes == 4:
            return


        # Cadastra os novos Usuarios no json
def cadastrar(user, senha):
    dados = carregar_usuarios()
    if user in dados:
        print(f"Esse nome de usuario já existe: {user}")
        print("Não foi possivel registrar usuario")
        return
    dados[user] = {
        "password":senha,
        "role":"user"
}
    print("Usuario criado com sucesso!")
    with open(arq, "w", encoding="UTF=8") as f:
        json.dump(dados, f, indent=4)
    logging.info("Usuario criado com sucesso!!")

def loginInterno(usuario):
    print(r"""
    ██████╗ ███████╗████████╗██████╗  ██████╗ 
    ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗
    ██████╔╝█████╗     ██║   ██████╔╝██║   ██║
    ██╔══██╗██╔══╝     ██║   ██╔══██╗██║   ██║
    ██║  ██║███████╗   ██║   ██║  ██║╚██████╔╝
    ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ 

          >> RETR0 ACCESS TERMINAL <<
    """)
    while True:
        try:
            op = int(input("[1] Ver logs\n[2] Gerencia de roles\n[3] Sala de Usuario\n[4] Sair\nR: "))
        except Exception as e:
            print("Digite corretamente conforme o indice!!!")
        if op == 1:
            ver_logs(usuario)
            print("----------------------------------------------------------------------------------------------------")
        elif op == 2:
           gerencia(usuario)
        elif op == 3:
            Sala()
        elif op == 4:
            exit()
        else:
            print("Não existe esse indice!!")



def banner():
    lock = r"""
                  ███████████████
               ██████           ██████
            ██████    █████████    ██████
          ██████    █████████████    ██████
         ██████    ███████████████    ██████
         ██████    ███████████████    ██████
          ██████    █████████████    ██████
            ██████    █████████    ██████
               ██████           ██████
                  ███████████████
                        ██
                        ██
            █████████████████████████████
            ██                         ██
            ██          AUTH           ██
            ██         SYSTEM          ██
            ██                         ██
            █████████████████████████████
    """
    print("\033[31m" + lock + "\033[0m")

def validaSenha(senha):
    validar = senha
    vzs = 0
    regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$"
    while vzs < 5:
        if re.match(regex,validar):
            logging.info("Senha Valida!!")
            break
        else:
            vzs += 1
            logging.info("Senha Fora dos padrões exigidos!!!")
            print("Senha Fora dos padrões exigidos!!!")
            print("A senha Precisa ter no MINIMO:\n1 Letra Maiuscula\n1 Letra Minuscula\n1 Numero\n1 Caracter especial\n Minimo 8 Caracteres")
            validar = input("Digite novamente:").strip()
            if vzs == 5:
                print("Tente novamente em outro momento!! ")
                return None
    return validar


def painel():
    logging.info("Sistema Iniciado")
    hs = PasswordHasher()  # Cria a instacia.
    print("Bem vindo ao Sistema auth")
    print("[1] Cadastro\n[2] Login\n[3] Sair")

    while True:
        try:
            opcao = int(input("O que deseja fazer? "))
        except Exception as e:
            print("Opção invalida! Por favor se localize conforme o numero do indice")
            continue
        if opcao == 1:
            logging.info("Usuario acessou Campo de Cadastro!")
            vz = 0
            while vz < 3:
                user = input("Digite um nome de usuario: ").strip()
                if not user:
                    print("Esse campo não pode estar vazio!!!")
                    logging.info("Campo de usuario vazio")
                    vz += 1
                else:
                    break
            else:
                print("Muitas tentativas Invalidas!!!")
                logging.info("Tentativas excedidas (3 vezes)")
                return

            #PASSWORD
            vezes = 0
            while vezes < 3:
                password = input("Digite uma senha: ").strip()
                password = validaSenha(password)
                if not password:
                    print("O campo Senha não pode estar vazio!!!")
                    logging.info("Campo de senhas vazio.")
                    vezes += 1
                else:
                    logging.info("Senha cadastrada!")
                    break
            else:
                print('Muitas tentativas Invalidas!!')
                logging.info("Excedeu o limite de tentativas!")
                return

            hash_senha = hs.hash(password)  # Cria a hash da senha
            logging.info("Hash criado!")
            cadastrar(user, hash_senha)  # Cadastra a hash no JSON

        elif opcao == 2:   #login
            logging.info("Usuario acessou campo de login!")
            tentativas = 0
            dado = carregar_usuarios()  # Carrega os dados do JSON para uso na função

            while tentativas < 3:
                user = input("Digite o usuario: ").strip()

                if user not in dado:
                    print("Usuario não registrado em nosso sistema!")
                    logging.info("Usuario Inexistente!")
                    break


                password = input("Digite a senha: ").strip()
                try:
                    hs.verify(dado[user]["password"], password)
                    logging.info("Acesso Autorizado!!")
                    global usuario_logado
                    usuario_logado = {
                        "username":user,
                        "role":dado[user]["role"]
                    }
                    loginInterno(usuario_logado)
                    return
                    # valida se a senha é a mesma do hash
                except VerifyMismatchError:
                    print("Senha ou Usuario Incorretos!!")
                    logging.warning("Senha Incorreta!!")
                    tentativas += 1
                except InvalidHash:  # valida se o hash está em perfeito estado
                    print("Erro critico!!! HASH quebrada")
                    logging.critical("Hash em formato incompativel!!")
                    tentativas += 1
                if tentativas == 3:
                    print("Numero de tentativas excedidos, voce será redirecionado ao menu em 10 segundos!")
                    logging.info("Numero de tentativas excedidas!")
                    sleep(10)




        elif opcao == 3:  # Interrompe o Script
            print("Adeus..")
            logging.info("Encerrando sistema!")
            return

        else:
            print("Não existe esse indice!!!!")



































