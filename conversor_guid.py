import base64
import uuid
import os


def guid_para_base64(guid_str):
    """Converte um GUID padrão para Base64 (Padrão MongoDB) e gera o filtro."""
    try:
        guid_str = guid_str.strip()
        obj_uuid = uuid.UUID(guid_str)

        bytes_guid = obj_uuid.bytes
        base64_bytes = base64.b64encode(bytes_guid) 
        b64_str = base64_bytes.decode("utf-8")

        mongo_filter = f'{{ "_id" : BinData(3,"{b64_str}") }}'
        
        return b64_str, mongo_filter
    except ValueError:
        return "⚠️ Erro: Formato de GUID inválido.", None
    except Exception as e:
        return f"⚠️ Erro crítico: {str(e)}", None


def base64_para_guid(b64_str):
    """Converte um Base64 de volta para o formato GUID padrão."""
    try:
        b64_str = b64_str.strip()

        padding = len(b64_str) % 4
        if padding:
            b64_str += "=" * (4 - padding)

        b64_str = b64_str.replace('-', '+').replace('_', '/')

        bytes_guid = base64.b64decode(b64_str)
        return str(uuid.UUID(bytes=bytes_guid))
    except Exception:
        return "⚠️ Erro: String Base64 inválida ou não corresponde a um GUID de 16 bytes."


def main():
    # Ativa o estilo Matrix no terminal do Windows (Fundo preto, letras verdes)
    os.system('color 0a')

    # Loop infinito para manter o programa aberto fazendo várias consultas
    while True:
        print("\n" + "=" * 55)
        print("       CONVERSOR LOCAL: GUID <=> BASE64      ")
        print("=" * 55)

        print("Escolha a operação:")
        print("1 - Codificar (GUID para Base64 + MongoDB Filter)")
        print("2 - Decodificar (Base64 para GUID)")
        opcao = input("> ").strip()

        print("\n" + "-" * 55)

        if opcao == "1":
            entrada = input("Cole o seu GUID aqui:\n> ")
            resultado_b64, mongo_filter = guid_para_base64(entrada)
            
            if mongo_filter:
                print("\n[RESULTADO]")
                print(f"Base64:         {resultado_b64}")
                print(f"MongoDB filter: {mongo_filter}")
            else:
                print(f"\n{resultado_b64}") 

        elif opcao == "2":
            entrada = input("Cole o seu Base64 aqui:\n> ")
            resultado = base64_para_guid(entrada)
            print("\n[RESULTADO]")
            print(f"GUID:           {resultado}")

        else:
            print("⚠️ Opção inválida!")

        print("-" * 55)
        
        # Pergunta se deseja continuar ou sair
        continuar = input("\nDeseja fazer outra consulta? (S/N): ").strip().upper()
        if continuar != 'S':
            break

    # Trava final antes de fechar a janela definitivamente
    print("\nEncerrando o conversor...")
    input("Pressione Enter para fechar a janela.")


if __name__ == "__main__":
    main()