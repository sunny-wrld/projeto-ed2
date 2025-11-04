import os
import csv
import statistics
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

#inteiro gerado por ia

# Configurações globais para gráficos acadêmicos
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 14

def ler_resultados(linguagem, tamanhos):
    """Lê todos os resultados de uma linguagem e retorna dicionário organizado por tamanho"""
    resultados = {}
    
    for n in tamanhos:
        dir_resultados = f"resultados/{linguagem}/n{n:06d}"
        tempos = []
        
        for execucao in range(1, 51):
            arquivo = os.path.join(dir_resultados, f"run_{execucao:03d}.csv")
            
            if os.path.exists(arquivo):
                with open(arquivo, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        tempos.append(float(row['tempo_ms']))
        
        if tempos:
            resultados[n] = tempos
    
    return resultados

def calcular_estatisticas(resultados):
    """Calcula média e desvio padrão para cada tamanho"""
    stats = {}
    for n, tempos in resultados.items():
        stats[n] = {
            'media': statistics.mean(tempos),
            'desvio': statistics.stdev(tempos) if len(tempos) > 1 else 0,
            'tempos': tempos
        }
    return stats

def gerar_tabela_resumo(stats_python, stats_c, stats_java, tamanhos):
    """Gera arquivo de texto com tabela resumo formatada"""
    
    with open('resultados/Tabela1_Resumo_Geral.txt', 'w', encoding='utf-8') as f:
        f.write("="*90 + "\n")
        f.write("Tabela 1: Resumo Geral dos Resultados Experimentais\n")
        f.write("Bucket Sort com 1000 baldes e Insertion Sort manual\n")
        f.write("="*90 + "\n\n")
        
        # Cabeçalho
        f.write(f"{'n':<10} {'Python':<28} {'C':<28} {'Java':<28}\n")
        f.write(f"{'':10} {'Média (ms)':<13} {'Desvio (ms)':<13} ")
        f.write(f"{'Média (ms)':<13} {'Desvio (ms)':<13} ")
        f.write(f"{'Média (ms)':<13} {'Desvio (ms)':<13}\n")
        f.write("-"*90 + "\n")
        
        # Dados
        for n in sorted(tamanhos):
            py = stats_python.get(n, {'media': 0, 'desvio': 0})
            c = stats_c.get(n, {'media': 0, 'desvio': 0})
            java = stats_java.get(n, {'media': 0, 'desvio': 0})
            
            f.write(f"{n:<10} ")
            f.write(f"{py['media']:>12.4f} {py['desvio']:>12.4f}  ")
            f.write(f"{c['media']:>12.4f} {c['desvio']:>12.4f}  ")
            f.write(f"{java['media']:>12.4f} {java['desvio']:>12.4f}\n")
        
        f.write("="*90 + "\n\n")
        f.write("Legenda:\n")
        f.write("  n: Tamanho do vetor de entrada\n")
        f.write("  Média (ms): Tempo médio de execução em milissegundos (50 execuções)\n")
        f.write("  Desvio (ms): Desvio padrão dos tempos de execução\n")
        f.write("\nObservações:\n")
        f.write("  - Algoritmo: Bucket Sort com 1000 baldes\n")
        f.write("  - Ordenação interna: Insertion Sort manual\n")
        f.write("  - Dados: Números inteiros aleatórios\n")
        f.write("  - Repetições: 50 execuções por tamanho\n")
    
    print("✅ Tabela 1 salva: Tabela1_Resumo_Geral.txt")

def grafico_desempenho_c(stats_c):
    """Gráfico 1: Desempenho do algoritmo em C"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    tamanhos = sorted(stats_c.keys())
    medias = [stats_c[n]['media'] for n in tamanhos]
    
    ax.loglog(tamanhos, medias, 's-', label='Dados aleatórios', 
            linewidth=1.5, markersize=6, color='black', 
            markerfacecolor='white', markeredgewidth=1.5, base=10)
    
    ax.set_xlabel('Tamanho da entrada (n) - escala log', fontweight='bold')
    ax.set_ylabel('Tempo médio de execução (ms) - escala log', fontweight='bold')
    ax.set_title('Gráfico 1: Desempenho do Bucket Sort em C\n1000 baldes com Insertion Sort manual')
    ax.legend(loc='upper left', frameon=True, fancybox=False, shadow=False)
    ax.grid(True, which='both', linestyle='--', alpha=0.5, linewidth=0.5)
    
    plt.tight_layout()
    plt.savefig('resultados/Grafico1_Desempenho_C.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig('resultados/Grafico1_Desempenho_C.pdf', bbox_inches='tight', facecolor='white')
    print("✅ Gráfico 1 salvo: Grafico1_Desempenho_C.png e .pdf")
    plt.close()

def grafico_desempenho_java(stats_java):
    """Gráfico 2: Desempenho do algoritmo em Java"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    tamanhos = sorted(stats_java.keys())
    medias = [stats_java[n]['media'] for n in tamanhos]
    
    ax.loglog(tamanhos, medias, 'o-', label='Dados aleatórios', 
            linewidth=1.5, markersize=6, color='black', 
            markerfacecolor='gray', markeredgewidth=1.5, base=10)
    
    ax.set_xlabel('Tamanho da entrada (n) - escala log', fontweight='bold')
    ax.set_ylabel('Tempo médio de execução (ms) - escala log', fontweight='bold')
    ax.set_title('Gráfico 2: Desempenho do Bucket Sort em Java\n1000 baldes com Insertion Sort manual')
    ax.legend(loc='upper left', frameon=True, fancybox=False, shadow=False)
    ax.grid(True, which='both', linestyle='--', alpha=0.5, linewidth=0.5)
    
    plt.tight_layout()
    plt.savefig('resultados/Grafico2_Desempenho_Java.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig('resultados/Grafico2_Desempenho_Java.pdf', bbox_inches='tight', facecolor='white')
    print("✅ Gráfico 2 salvo: Grafico2_Desempenho_Java.png e .pdf")
    plt.close()

def grafico_desempenho_python(stats_python):
    """Gráfico 3: Desempenho do algoritmo em Python"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    tamanhos = sorted(stats_python.keys())
    medias = [stats_python[n]['media'] for n in tamanhos]
    
    ax.loglog(tamanhos, medias, '^-', label='Dados aleatórios', 
            linewidth=1.5, markersize=6, color='black', 
            markerfacecolor='black', markeredgewidth=1.5, base=10)
    
    ax.set_xlabel('Tamanho da entrada (n) - escala log', fontweight='bold')
    ax.set_ylabel('Tempo médio de execução (ms) - escala log', fontweight='bold')
    ax.set_title('Gráfico 3: Desempenho do Bucket Sort em Python\n1000 baldes com Insertion Sort manual')
    ax.legend(loc='upper left', frameon=True, fancybox=False, shadow=False)
    ax.grid(True, which='both', linestyle='--', alpha=0.5, linewidth=0.5)
    
    plt.tight_layout()
    plt.savefig('resultados/Grafico3_Desempenho_Python.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig('resultados/Grafico3_Desempenho_Python.pdf', bbox_inches='tight', facecolor='white')
    print("✅ Gráfico 3 salvo: Grafico3_Desempenho_Python.png e .pdf")
    plt.close()

def grafico_comparativo(stats_python, stats_c, stats_java):
    """Gráfico 4: Comparativo das três linguagens"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    tamanhos = sorted(stats_python.keys())
    
    medias_c = [stats_c[n]['media'] for n in tamanhos]
    medias_java = [stats_java[n]['media'] for n in tamanhos]
    medias_python = [stats_python[n]['media'] for n in tamanhos]
    
    ax.loglog(tamanhos, medias_c, 's-', label='C (dados aleatórios)', 
            linewidth=1.5, markersize=6, color='black', 
            markerfacecolor='white', markeredgewidth=1.5, base=10)
    ax.loglog(tamanhos, medias_java, 'o-', label='Java (dados aleatórios)', 
            linewidth=1.5, markersize=6, color='black', 
            markerfacecolor='gray', markeredgewidth=1.5, base=10)
    ax.loglog(tamanhos, medias_python, '^-', label='Python (dados aleatórios)', 
            linewidth=1.5, markersize=6, color='black', 
            markerfacecolor='black', markeredgewidth=1.5, base=10)
    
    ax.set_xlabel('Tamanho da entrada (n) - escala log', fontweight='bold')
    ax.set_ylabel('Tempo médio de execução (ms) - escala log', fontweight='bold')
    ax.set_title('Gráfico 4: Comparativo de desempenho entre linguagens\nBucket Sort com 1000 baldes e Insertion Sort manual')
    ax.legend(loc='upper left', frameon=True, fancybox=False, shadow=False)
    ax.grid(True, which='both', linestyle='--', alpha=0.5, linewidth=0.5)
    
    plt.tight_layout()
    plt.savefig('resultados/Grafico4_Comparativo.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig('resultados/Grafico4_Comparativo.pdf', bbox_inches='tight', facecolor='white')
    print("✅ Gráfico 4 salvo: Grafico4_Comparativo.png e .pdf")
    plt.close()

def grafico_comparativo_loglog(stats_python, stats_c, stats_java):
    """Gráfico 5: Comparativo em escala log-log para análise de crescimento"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    tamanhos = sorted(stats_python.keys())
    
    medias_c = [stats_c[n]['media'] for n in tamanhos]
    medias_java = [stats_java[n]['media'] for n in tamanhos]
    medias_python = [stats_python[n]['media'] for n in tamanhos]
    
    ax.loglog(tamanhos, medias_c, 's-', label='C (dados aleatórios)', 
              linewidth=1.5, markersize=6, color='black', 
              markerfacecolor='white', markeredgewidth=1.5, base=10)
    ax.loglog(tamanhos, medias_java, 'o-', label='Java (dados aleatórios)', 
              linewidth=1.5, markersize=6, color='black', 
              markerfacecolor='gray', markeredgewidth=1.5, base=10)
    ax.loglog(tamanhos, medias_python, '^-', label='Python (dados aleatórios)', 
              linewidth=1.5, markersize=6, color='black', 
              markerfacecolor='black', markeredgewidth=1.5, base=10)
    
    # Linhas de referência teóricas
    ax.loglog(tamanhos, [tamanhos[0]/10 * (n/tamanhos[0]) for n in tamanhos], 
              ':', label='O(n) referência', linewidth=1, color='gray', alpha=0.5)
    ax.loglog(tamanhos, [tamanhos[0]/1000 * (n/tamanhos[0])**2 for n in tamanhos], 
              '--', label='O(n²) referência', linewidth=1, color='gray', alpha=0.5)
    
    ax.set_xlabel('Tamanho da entrada (n) - escala log', fontweight='bold')
    ax.set_ylabel('Tempo de execução (ms) - escala log', fontweight='bold')
    ax.set_title('Gráfico 5: Análise de crescimento em escala log-log\nBucket Sort - Comparação com complexidade teórica')
    ax.legend(loc='upper left', frameon=True, fancybox=False, shadow=False)
    ax.grid(True, which='both', linestyle='--', alpha=0.5, linewidth=0.5)
    
    plt.tight_layout()
    plt.savefig('resultados/Grafico5_Loglog.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig('resultados/Grafico5_Loglog.pdf', bbox_inches='tight', facecolor='white')
    print("✅ Gráfico 5 salvo: Grafico5_Loglog.png e .pdf")
    plt.close()

def main():
    print("="*70)
    print(" GERADOR DE TABELAS E GRÁFICOS - PROJETO AED2")
    print("="*70)
    print("\nCarregando dados dos experimentos...")
    
    tamanhos = [10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]
    
    resultados_python = ler_resultados('python', tamanhos)
    resultados_c = ler_resultados('c', tamanhos)
    resultados_java = ler_resultados('java', tamanhos)
    
    print("Calculando estatísticas...")
    stats_python = calcular_estatisticas(resultados_python)
    stats_c = calcular_estatisticas(resultados_c)
    stats_java = calcular_estatisticas(resultados_java)
    
    print("\nGerando tabela resumo...")
    gerar_tabela_resumo(stats_python, stats_c, stats_java, tamanhos)
    
    print("\nGerando gráficos acadêmicos...\n")
    os.makedirs('resultados', exist_ok=True)
    
    grafico_desempenho_c(stats_c)
    grafico_desempenho_java(stats_java)
    grafico_desempenho_python(stats_python)
    grafico_comparativo(stats_python, stats_c, stats_java)
    grafico_comparativo_loglog(stats_python, stats_c, stats_java)
    
    print("\n" + "="*70)
    print("✅ TABELAS E GRÁFICOS GERADOS COM SUCESSO!")
    print("="*70)
    print("\nArquivos gerados em 'resultados/':")
    print("\n📋 TABELA:")
    print("  • Tabela1_Resumo_Geral.txt")
    print("\n📊 GRÁFICOS (PNG 300 DPI + PDF vetorial):")
    print("  • Gráfico 1: Grafico1_Desempenho_C")
    print("  • Gráfico 2: Grafico2_Desempenho_Java")
    print("  • Gráfico 3: Grafico3_Desempenho_Python")
    print("  • Gráfico 4: Grafico4_Comparativo")
    print("  • Gráfico 5: Grafico5_Loglog (escala logarítmica)")
    print("\n💡 Formato acadêmico:")
    print("   • Escala log-log em TODOS os gráficos")
    print("   • Facilita comparação com análise de complexidade teórica")
    print("   • Preto e branco com padrões distintos")
    print("   • Legendas, títulos e grid padronizados")
    print("="*70)
    print()

if __name__ == "__main__":
    main()
