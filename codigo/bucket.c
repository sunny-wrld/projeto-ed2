#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <direct.h>

void criar_diretorios(const char *caminho) {
    char temp[200];
    char *p = NULL;
    size_t len;
    
    snprintf(temp, sizeof(temp), "%s", caminho);
    len = strlen(temp);
    if (temp[len - 1] == '/' || temp[len - 1] == '\\')
        temp[len - 1] = 0;
    
    for (p = temp + 1; *p; p++) {
        if (*p == '/' || *p == '\\') {
            *p = 0;
            _mkdir(temp);
            *p = '/';
        }
    }
    _mkdir(temp);
}

double get_time_ms() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (tv.tv_sec * 1000.0) + (tv.tv_usec / 1000.0);
}

void insertion_sort(int vetor[], int tamanho) {
    int i, j, chave;
    for (i = 1; i < tamanho; i++) {
        chave = vetor[i];
        j = i - 1;
        while (j >= 0 && vetor[j] > chave) {
            vetor[j + 1] = vetor[j];
            j = j - 1;
        }
        vetor[j + 1] = chave;
    }
}

void bucket_sort(int vetor[], int tamanho) {
    int i, j, k;
    
    if (tamanho <= 0) return;
    
    int minimo = vetor[0];
    int maximo = vetor[0];
    for (i = 1; i < tamanho; i++) {
        if (vetor[i] < minimo) minimo = vetor[i];
        if (vetor[i] > maximo) maximo = vetor[i];
    }
    
    if (maximo == minimo) return;
    
    int num_baldes = 1000;
    
    int **baldes = (int**)malloc(num_baldes * sizeof(int*));
    int *capacidades = (int*)malloc(num_baldes * sizeof(int));
    int *tamanhos = (int*)malloc(num_baldes * sizeof(int));
    
    for (i = 0; i < num_baldes; i++) {
        capacidades[i] = 10;
        baldes[i] = (int*)malloc(capacidades[i] * sizeof(int));
        tamanhos[i] = 0;
    }
    
    for (i = 0; i < tamanho; i++) {
        int indice = (int)((double)(vetor[i] - minimo) / (double)(maximo - minimo) * (num_baldes - 1));
        if (indice >= num_baldes) indice = num_baldes - 1;
        
        if (tamanhos[indice] >= capacidades[indice]) {
            capacidades[indice] *= 2;
            baldes[indice] = (int*)realloc(baldes[indice], capacidades[indice] * sizeof(int));
        }
        
        baldes[indice][tamanhos[indice]] = vetor[i];
        tamanhos[indice]++;
    }
    
    k = 0;
    for (i = 0; i < num_baldes; i++) {
        if (tamanhos[i] > 0) {
            insertion_sort(baldes[i], tamanhos[i]);
            for (j = 0; j < tamanhos[i]; j++) {
                vetor[k] = baldes[i][j];
                k++;
            }
        }
        free(baldes[i]);
    }
    
    free(baldes);
    free(capacidades);
    free(tamanhos);
}

int ler_csv_dados(const char *caminho, int *vetor, int n) {
    FILE *f = fopen(caminho, "r");
    if (!f) return 0;
    
    fseek(f, 0, SEEK_END);
    long tamanho_arquivo = ftell(f);
    fseek(f, 0, SEEK_SET);
    
    char *buffer = (char*)malloc(tamanho_arquivo + 1);
    if (!buffer) {
        fclose(f);
        return 0;
    }
    
    size_t lidos = fread(buffer, 1, tamanho_arquivo, f);
    buffer[lidos] = '\0';
    fclose(f);
    
    int count = 0;
    int i = 0;
    int num_start = 0;
    int in_number = 0;
    
    for (i = 0; i <= lidos && count < n; i++) {
        char c = buffer[i];
        
        if (c >= '0' && c <= '9') {
            if (!in_number) {
                num_start = i;
                in_number = 1;
            }
        } else if (in_number) {
            buffer[i] = '\0';
            vetor[count] = atoi(&buffer[num_start]);
            count++;
            in_number = 0;
        }
    }
    
    free(buffer);
    return count;
}

int main() {
    int tamanhos[] = {10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000};
    int num_tamanhos = 10;
    int i, execucao;
    
    for (i = 0; i < num_tamanhos; i++) {
        int n = tamanhos[i];
        int *vetor = (int*)malloc(n * sizeof(int));
        
        char dir_dados[150];
        char dir_resultados[150];
        sprintf(dir_dados, "dados/n%06d", n);
        sprintf(dir_resultados, "resultados/c/n%06d", n);
        
        criar_diretorios(dir_resultados);
        
        printf("\nn=%d\n", n);
        
        for (execucao = 1; execucao <= 50; execucao++) {
            char arquivo_entrada[200];
            char arquivo_saida[200];
            sprintf(arquivo_entrada, "%s/run_%03d.csv", dir_dados, execucao);
            sprintf(arquivo_saida, "%s/run_%03d.csv", dir_resultados, execucao);
            
            int lidos = ler_csv_dados(arquivo_entrada, vetor, n);
            if (lidos != n) {
                printf("ERRO: esperado %d, lido %d de %s\n", n, lidos, arquivo_entrada);
                continue;
            }
            
            double inicio = get_time_ms();
            bucket_sort(vetor, n);
            double fim = get_time_ms();
            
            double tempo_ms = fim - inicio;
            
            FILE *f = fopen(arquivo_saida, "w");
            if (f) {
                fprintf(f, "n,tempo_ms,run\n");
                fprintf(f, "%d,%.4f,%d\n", n, tempo_ms, execucao);
                fclose(f);
            }
            
            printf("Execucao %03d: %.4f ms\n", execucao, tempo_ms);
        }
        
        free(vetor);
    }
    
    return 0;
}