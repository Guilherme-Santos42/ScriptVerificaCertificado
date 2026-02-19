import ssl
import socket
import datetime

# --- CONFIGURAÇÕES ---
DOMINIOS = ["google.com", "uol.com.br", "expired.badssl.com"] # Adicionei um de teste que falha
DIAS_CRITICO = 7
DIAS_ALERTA = 30

# Cores para o terminal
VERDE = '\033[92m'
AMARELO = '\033[93m'
VERMELHO = '\033[91m'
RESET = '\033[0m'

def verificar_vencimento(dominio):
    contexto = ssl.create_default_context()
    try:
        with socket.create_connection((dominio, 443), timeout=3) as sock:
            with contexto.wrap_socket(sock, server_hostname=dominio) as ssock:
                cert = ssock.getpeercert()
                data_venc_str = cert['notAfter']
                # Converte a string do certificado para objeto datetime
                data_venc = datetime.datetime.strptime(data_venc_str, '%b %d %H:%M:%S %Y %Z')
                return data_venc
    except Exception as e:
        return str(e)

print(f"\n{'DOMÍNIO':<25} | {'STATUS':<15} | {'DIAS RESTANTES'}")
print("-" * 60)

for d in DOMINIOS:
    resultado = verificar_vencimento(d)
    
    # Se o resultado for uma string, é porque deu erro na conexão
    if isinstance(resultado, str):
        print(f"{d:<25} | {VERMELHO}{'ERRO/EXPIROU':<15}{RESET} | {resultado}")
        continue

    # Cálculo dos dias
    dias_restantes = (resultado - datetime.datetime.utcnow()).days
    
    # Lógica de criticidade
    if dias_restantes <= DIAS_CRITICO:
        cor = VERMELHO
        status = "CRÍTICO"
    elif dias_restantes <= DIAS_ALERTA:
        cor = AMARELO
        status = "ALERTA"
    else:
        cor = VERDE
        status = "OK"

    print(f"{d:<25} | {cor}{status:<15}{RESET} | {dias_restantes} dias")

print("-" * 60 + "\n")