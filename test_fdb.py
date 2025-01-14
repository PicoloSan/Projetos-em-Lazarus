import ctypes

try:
    ctypes.WinDLL(r'C:\Users\CMP010\Downloads\robo\database\fbembed.dll')
    print("fbembed.dll carregado com sucesso")
except Exception as e:
    print("Erro ao carregar fbembed.dll:", e)
