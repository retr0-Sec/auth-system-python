# SECURE_AUTH_SECURIT_PROJECT

 SISTEMA DE AUTENTICAÇÃO FEITO COM FINS DE ESTUDOS. NESSE PROJETO TRABALHEI HABILIDADES COM HASH(ARGON2),VALIDAÇÕES REGEX,MANIPULAÇÃO DE JSON

# FUNCIONALIDADES:

- Cadastro de Usuarios
- Login de Usuarios com Verificação de senha
- Controle de Tentativas
- Logs de Segurança (com um usuario especial voce tem acesso aos logs, simulando um root)
- Uma pequena ASCII a efetuar o Login

# TECNOLOGIAS:

- PYTHON 3.10+
- POETRY
- ARGON2-CFFI

## INSTALAÇÃO:

 CLONE O REPOSITORIO:

~~~bash
  git clone https://github.com/retr0-Sec/secure_authetication_system
  cd secure_authetication_system
  poetry install
~~~

# SEGURANÇA:

- Senhas Armazenadas apenas em Hash(ARGON2)
- Controle de Tentativas(Anti Brute Force)
- Senhas Nunca são Logadas
Acesso aos logs

O sistema implementa controle de acesso lógico, permitindo a visualização dos logs apenas por usuários autenticados com permissões administrativas.

Para fins de portfólio, a proteção do arquivo de log é tratada no nível da aplicação.

# OBSERVAÇÃO:

TRATA-SE DE UM PROJETO PESSOAL COM OBJETIVO DE ESTUDO/APRENDIZADO. NÃO UTILE PARA CASO REAIS SEM ADAPTAÇOES DE SEGURANÇAS E MELHORIAS DE CODIGO.

(
Este projeto é focado em aprendizado e evolução constante.
Críticas construtivas, sugestões de hardening e melhorias no código são bem-vindas.
)