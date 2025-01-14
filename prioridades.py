import ctypes
import time

# Função para alterar a prioridade
def set_process_priority(priority_class):
    # Obtém o identificador do processo atual
    process_handle = ctypes.windll.kernel32.GetCurrentProcess()
    # Altera a prioridade do processo
    ctypes.windll.kernel32.SetPriorityClass(process_handle, priority_class)

# Prioridades disponíveis
IDLE_PRIORITY_CLASS = 0x00000040
BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
NORMAL_PRIORITY_CLASS = 0x00000020
ABOVE_NORMAL_PRIORITY_CLASS = 0x00040000
HIGH_PRIORITY_CLASS = 0x00000080
REALTIME_PRIORITY_CLASS = 0x00000100

# Defina a prioridade desejada, por exemplo, abaixo do normal
set_process_priority(BELOW_NORMAL_PRIORITY_CLASS)

while True:
    # Seu código aqui
    print("Executando...")
    time.sleep(5)  # Pausa de 5 segundos

