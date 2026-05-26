from abc import ABC, abstractmethod
from datetime import datetime

# ----------------------------------------------------------
# 1. INTERFACE / CLASSE ABSTRATA
# ----------------------------------------------------------
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self) -> float:
        """Retorna o valor da transação."""
        pass

    @abstractmethod
    def registrar(self, conta):
        """Aplica a regra da transação na conta informada."""
        pass


# ----------------------------------------------------------
# 2. POLIMORFISMO: IMPLEMENTAÇÕES DA INTERFACE
# ----------------------------------------------------------
class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor  # Atributo protegido/privado

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


# ----------------------------------------------------------
# 3. COMPOSIÇÃO: HISTÓRICO DAS CONTAS
# ----------------------------------------------------------
class Historico:
    def __init__(self):
        self._transacoes = []  # Armazena objetos/dicionários das transações

    @property
    def transacoes(self) -> list:
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })


# ----------------------------------------------------------
# 4. HERANÇA: CLASSES DE CLIENTES
# ----------------------------------------------------------
class Cliente:
    def __init__(self, endereco: str):
        self._endereco = endereco
        self._contas = []

    @property
    def contas(self) -> list:
        return self._contas

    def realizar_transacao(self, conta, transacao: Transacao):
        # Polimorfismo puro em ação: a transação decide como se registrar
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: str, endereco: str):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self) -> str:
        return self._cpf

    @property
    def nome(self) -> str:
        return self._nome


# ----------------------------------------------------------
# 5. ENCAPSULAMENTO: CLASSES DE CONTAS BANCÁRIAS
# ----------------------------------------------------------
class Conta:
    def __init__(self, numero: int, cliente: Cliente, agencia: str = "0001"):
        self._saldo = 0.0          # Modificador de acesso privado (-)
        self._numero = numero      # Modificador de acesso privado (-)
        self._agencia = agencia    # Modificador de acesso privado (-)
        self._cliente = cliente    # Relacionamento com Cliente
        self._historico = Historico()  # A conta TEM um histórico

    # Atributos gerenciados via propriedades (Getters)
    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def historico(self) -> Historico:
        return self._historico

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int) -> 'Conta':
        """Método de classe que atua como fábrica (Factory) para novas instâncias."""
        return cls(numero, cliente)

    def sacar(self, valor: float) -> bool:
        if valor > self.saldo:
            print("\nOperação falhou! Saldo insuficiente.")
            return False

        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!")
            return True
        else:
            print("\nOperação falhou! O valor informado é inválido.")
            return False

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso!")
            return True
        else:
            print("\nOperação falhou! O valor informado é inválido.")
            return False


# Especialização de Conta usando Herança
class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: Cliente, agencia: str = "0001", limite: float = 500.0, limite_saques: int = 3):
        super().__init__(numero, cliente, agencia)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        # Recupera quantas transações do tipo "Saque" existem no histórico
        numero_saques = len(
            [t for t in self.historico.transacoes if t["tipo"] == "Saque"]
        )

        if valor > self._limite:
            print(f"\nOperação falhou! O valor excede o limite por saque de R$ {self._limite:.2f}.")
            return False

        elif numero_saques >= self._limite_saques:
            print("\nOperação falhou! Número máximo de saques diários atingido.")
            return False

        # Caso passe pelas regras da Conta Corrente, valida o saldo na classe pai
        return super().sacar(valor)


# ----------------------------------------------------------
# FLUXO INTERATIVO DO SISTEMA (MENU)
# ----------------------------------------------------------
def filtrar_cliente(cpf, clientes):
    filtrados = [c for c in clientes if c.cpf == cpf]
    return filtrados[0] if filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nEste cliente não possui uma conta vinculada!")
        return None
    return cliente.contas[0] # Retorna a primeira conta para fins de exemplo

def main():
    clientes = []
    contas = []
    numero_conta_sequencial = 1

    while True:
        menu = """
        ============= MENU BANCÁRIO ================
        [1] Cadastrar Cliente (PF)
        [2] Abrir Conta Corrente
        [3] Realizar Depósito
        [4] Realizar Saque
        [5] Emitir Extrato
        [0] Sair
        ============================================
        Escolha uma opção: """
        
        opcao = input(menu)

        if opcao == "1":
            cpf = input("CPF (Somente números): ")
            if filtrar_cliente(cpf, clientes):
                print("\nErro: Já existe um cliente com este CPF.")
                continue

            nome = input("Nome completo: ")
            data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
            endereco = input("Endereço (Rua, num - Bairro - Cidade/UF): ")

            novo_cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
            clientes.append(novo_cliente)
            print("\nCliente cadastrado com sucesso!")

        elif opcao == "2":
            cpf = input("CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\nCliente não localizado! Realize o cadastro primeiro.")
                continue

            # Utilizando o Método de Classe (nova_conta) para instanciar
            nova_cc = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta_sequencial)
            contas.append(nova_cc)
            cliente.adicionar_conta(nova_cc)
            
            print(f"\nConta Corrente Nº {numero_conta_sequencial} aberta com sucesso!")
            numero_conta_sequencial += 1

        elif opcao == "3":
            cpf = input("CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)
            if not cliente:
                print("\nCliente não localizado!")
                continue

            conta = recuperar_conta_cliente(cliente)
            if not conta:
                continue

            valor = float(input("Valor do depósito: R$ "))
            transacao = Deposito(valor)
            
            # O cliente comanda a transação passando a conta alvo e a operação
            cliente.realizar_transacao(conta, transacao)

        elif opcao == "4":
            cpf = input("CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)
            if not cliente:
                print("\nCliente não localizado!")
                continue

            conta = recuperar_conta_cliente(cliente)
            if not conta:
                continue

            valor = float(input("Valor do saque: R$ "))
            transacao = Saque(valor)
            cliente.realizar_transacao(conta, transacao)

        elif opcao == "5":
            cpf = input("CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)
            if not cliente:
                print("\nCliente não localizado!")
                continue

            conta = recuperar_conta_cliente(cliente)
            if not conta:
                continue

            print("\n================ EXTRATO BANCÁRIO ================")
            historico_transacoes = conta.historico.transacoes

            if not historico_transacoes:
                print("Nenhuma movimentação realizada nesta conta.")
            else:
                for t in historico_transacoes:
                    print(f"{t['data']} - {t['tipo']}: R$ {t['valor']:.2f}")

            print(f"\nSaldo Atualizado: R$ {conta.saldo:.2f}")
            print("==================================================")

        elif opcao == "0":
            print("\nEncerrando o sistema bancário. Até logo!")
            break
        else:
            print("\nOpção inválida! Tente novamente.")

if __name__ == "__main__":
    main()