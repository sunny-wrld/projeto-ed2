import time
import csv
import os

def insertion_sort(vetor):
    for i in range(1, len(vetor)):
        chave = vetor[i]
        j = i - 1
        while j >= 0 and vetor[j] > chave:
            vetor[j + 1] = vetor[j]
            j = j - 1
        vetor[j + 1] = chave

def bucket_sort(vetor):
    tamanho = len(vetor)
    if tamanho <= 0:
        return vetor
    
    minimo = vetor[0]
    maximo = vetor[0]
    for i in range(1, tamanho):
        if vetor[i] < minimo:
            minimo = vetor[i]
        if vetor[i] > maximo:
            maximo = vetor[i]
    
    if maximo == minimo:
        return vetor
    
    num_baldes = 1000
    baldes = []
    for i in range(num_baldes):
        baldes.append([])
    
    for elemento in vetor:
        indice = int((elemento - minimo) / (maximo - minimo) * (num_baldes - 1))
        if indice >= num_baldes:
            indice = num_baldes - 1
        baldes[indice].append(elemento)
    
    k = 0
    for i in range(num_baldes):
        if len(baldes[i]) > 0:
            insertion_sort(baldes[i])
            for elemento in baldes[i]:
                vetor[k] = elemento
                k += 1
    
    return vetor

def ler_csv_dados(caminho):
    vetor = []
    with open(caminho, 'r') as f:
        conteudo = f.read().strip()
        valores = conteudo.split(',')
        for valor in valores:
            if valor:
                vetor.append(int(valor))
    return vetor

def main():
    tamanhos = [10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]
    
    for n in tamanhos:
        dir_dados = f"dados/n{n:06d}"
        dir_resultados = f"resultados/python/n{n:06d}"
        os.makedirs(dir_resultados, exist_ok=True)
        
        print(f"\nn={n}")
        
        for execucao in range(1, 51):
            arquivo_entrada = os.path.join(dir_dados, f"run_{execucao:03d}.csv")
            
            if not os.path.exists(arquivo_entrada):
                print(f"{arquivo_entrada} nao encontrado, pulando...")
                continue
            
            vetor = ler_csv_dados(arquivo_entrada)
            
            inicio = time.perf_counter()
            resultado = bucket_sort(vetor)
            fim = time.perf_counter()
            
            tempo_ms = (fim - inicio) * 1000
            
            csv_file = os.path.join(dir_resultados, f"run_{execucao:03d}.csv")
            with open(csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['n', 'tempo_ms', 'run'])
                writer.writerow([n, tempo_ms, execucao])
            
            print(f"Execucao {execucao:03d}: {tempo_ms:.4f} ms")

if __name__ == "__main__":
    main()