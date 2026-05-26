# Sistema Bancário em Python — Desafio de Programação Orientada a Objetos (POO)

Este repositório contém a evolução de um sistema bancário simplificado, desenvolvido como um desafio prático para consolidar os pilares da **Programação Orientada a Objetos (POO)** em Python. 

O principal objetivo do projeto foi migrar a arquitetura legada — que armazenava dados de clientes, contas e operações em dicionários — para um modelo robusto de objetos estruturado, seguindo rigorosamente as especificações de um diagrama de classes UML.

---

## Objetivos do Desafio

* **Abstração de Dados:** Substituir estruturas de dados primitivas (dicionários e listas puras) por entidades do mundo real representadas por classes.
* **Encapsulamento Rígido:** Proteger os dados sensíveis das contas (como número, agência e saldo), tornando-os privados e controlando o acesso de leitura e escrita através de **Propriedades (`@property`)**.
* **Gerenciamento de Histórico:** Implementar uma relação de composição onde cada conta possui seu próprio objeto `Historico`, responsável por registrar o log de transações.
* **Interface e Polimorfismo:** Criar um contrato abstrato para operações através da classe mãe `Transacao`, permitindo que as classes filhas `Deposito` e `Saque` executem suas regras específicas de maneira polimórfica.

---

## Estrutura do Modelo UML Implementado

O design do código reflete a seguinte hierarquia e conexões entre classes:

| Classe | Tipo / Papel | Descrição |
| :--- | :--- | :--- |
| **`Cliente` / `PessoaFisica`** | Herança | Modela os dados dos usuários e centraliza a capacidade de disparar transações e vincular novas contas. |
| **`Conta` / `ContaCorrente`** | Herança / Polimorfismo | A `ContaCorrente` herda a estrutura base da `Conta`, mas sobrescreve o método `sacar` para aplicar validações de limites de valor e teto máximo de saques diários. |
| **`Transacao`** | Classe Abstrata / Interface | Define o método obrigatório `registrar(conta)` que serve de molde para qualquer nova modalidade de movimentação financeira. |
| **`Historico`** | Composição | Acoplado à conta, registra a data, hora e tipo de cada movimentação bem-sucedida. |

---

## Tecnologias e Conceitos Aplicados

* **Python 3.x**
* Módulo **`abc`** *(Abstract Base Classes)* para criação de contratos/interfaces.
* Decoradores **`@property`** e **`@classmethod`** para encapsulamento e fábricas de objetos.
* Manipulação de datas com **`datetime`**.

---

## Como Executar o Projeto

1. Certifique-se de ter o Python instalado na sua máquina.
2. Clone o repositório:
   ```bash
   git clone https://github.com/lucianocsd/dio-modelando-sistema-bancario-poo-python.git
