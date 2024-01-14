#Bibliotecas importadas
import datetime
import json

#Declaracao de variavel global
global id_global

#Criacao de arquivo JSON para guardar os dados
def save_data_to_json(file_path, data):
#Tenta executar o bloco de codigo senao dispara excecao
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, default=str)
        #print(f"Dados salvos em {file_path}")
    except Exception as e:
        print(f"Erro ao salvar os dados em {file_path}: {e}")

#Recuperacao de dados do arquivo JSON
def load_data_from_json(file_path):
#Tenta executar a leitura de um arquivo JSON
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        #print(f"Dados carregados de {file_path}")
        return data
    except Exception as e:
        print(f"Erro ao carregar os dados de {file_path}: {e}")
        return []

#Variaveis recebem do arquivo JSON
pacientes_file_path = 'pacientes.json'
agendamentos_file_path = 'agendamentos.json'
id_global_file_path = 'id_global.json'

#As listas sao iniciadas
listaPacientes = load_data_from_json(pacientes_file_path)
listaAgendamentos = load_data_from_json(agendamentos_file_path)

#Faz a variavel ID global continuar contando da onde parou
try:
    with open(id_global_file_path, 'r') as json_file:
        id_global = json.load(json_file)
except FileNotFoundError:
    id_global = 0

while True:
    op = input("1 - Cadastrar Paciente\n2 - Marcações de consultas\n3 - Cancelamento de consultas\n4 - Sair\n>>")
    if op == "1":
        try:
           nome = input("Digite o nome do paciente: ")
           telefone = input("Digite o telefone do paciente: ")
           if any(paciente["telefone"] == telefone for paciente in listaPacientes):
               print("Telefone já cadastrado para outro paciente.")
           else:
               paciente = {"ID" : id_global, "telefone" : telefone, "paciente" : nome}
               listaPacientes.append(paciente)
               id_global += 1
               print("paciente cadastrado com sucesso")
               save_data_to_json(pacientes_file_path, listaPacientes)
               save_data_to_json(id_global_file_path, id_global)


        except Exception as e:
            print(f"Erro ao cadastrar paciente: {e}")

    elif op == "2":
        print("Pacientes cadastrados:")
        for paciente in listaPacientes:
            print("ID:", paciente["ID"], "Nome:", paciente["paciente"])

        opcao = input("Digite o número do paciente: ")

        for paciente in listaPacientes:
            if opcao == str(paciente["ID"]):
                try:
                    id_paciente = paciente["ID"]
                    nome_paciente = paciente["paciente"]
                    dia = input("Digite o dia para agendamento(DD/MM/AAAA)): ")
                    #Testa se o Dia ja foi previamente agendado
                    if any(agendamento["dia"] == dia for agendamento in listaAgendamentos):
                        print("Dia já agendado por outro paciente.")
                        continue
                    else:
                        #Testa se a hora foi previamente agendada
                        hora = input("Digite a hora para o agendamento: ")
                        if any(agendamento["hora"] == hora for agendamento in listaAgendamentos):
                            print("Hora já agendada por outro paciente")
                            continue
                        else:
                            #Testa se a data marcada e valida
                            data_de_entrada = datetime.datetime.strptime(f"{dia} {hora}", "%d/%m/%Y %H:%M")
                            if data_de_entrada < datetime.datetime.now():
                                print("Data e hora devem ser no futuro.")
                                continue
                            else:
                                especialidade = input("Digite a especialidade desejada para consulta: ")
                                agendamento = {"ID": id_paciente, "nome" : nome_paciente, "dia": dia, "hora": hora, "Especialidade": especialidade}
                                listaAgendamentos.append(agendamento)
                                print("Agendamento cadastrado com sucesso")
                                save_data_to_json(agendamentos_file_path, listaAgendamentos)
                except Exception as e:
                    print(f"Erro no agendamento: {e}")

    elif op == "3":
        print("Agendamentos existentes:")
        for i, agendamento in enumerate(listaAgendamentos, start=1):
            print(f"{i}. ID: {agendamento['ID']}, Nome: {agendamento['nome']} Dia: {agendamento['dia']}, Hora: {agendamento['hora']}, Especialidade: {agendamento['Especialidade']}")
        opcao = input("Digite o número do agendamento que deseja remarcar (ou '0' para sair): ")

        if opcao == "0":
            print("Retornando ao menu principal.")
        else:
            try:
                opcao = int(opcao)
                if 1 <= opcao <= len(listaAgendamentos):
                    agendamento_selecionado = listaAgendamentos[opcao - 1]
                    print(f"\nDetalhes do Agendamento Selecionado:")
                    print(f"ID: {agendamento_selecionado['ID']}")
                    print(f"Nome: {agendamento_selecionado['nome']}")
                    print(f"Dia: {agendamento_selecionado['dia']}")
                    print(f"Hora: {agendamento_selecionado['hora']}")
                    print(f"Especialidade: {agendamento_selecionado['Especialidade']}")
                    cancelar = input("Deseja cancelar este agendamento? (S/N): ")

                    if cancelar.upper() == "S":
                        del listaAgendamentos[opcao - 1]
                        print("Agendamento cancelado com sucesso.")
                    else:
                        print("Agendamento não cancelado.")
                else:
                    print("Número de agendamento inválido.")
            except ValueError:
                print("Por favor, insira um número válido.")
        save_data_to_json(agendamentos_file_path, listaAgendamentos)
        save_data_to_json(id_global_file_path, id_global)

    elif op == "4":
        print("Encerrando o programa")
        break
    else:
        print("Digite uma opção válida")
        continue

