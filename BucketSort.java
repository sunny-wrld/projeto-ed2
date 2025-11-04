import java.io.*;
import java.nio.file.*;
import java.util.*;

public class BucketSort {
    
    public static void insertionSort(int[] vetor) {
        for (int i = 1; i < vetor.length; i++) {
            int chave = vetor[i];
            int j = i - 1;
            while (j >= 0 && vetor[j] > chave) {
                vetor[j + 1] = vetor[j];
                j = j - 1;
            }
            vetor[j + 1] = chave;
        }
    }
    
    public static void bucketSort(int[] vetor) {
        int tamanho = vetor.length;
        if (tamanho <= 0) return;
        
        int minimo = vetor[0];
        int maximo = vetor[0];
        for (int i = 1; i < tamanho; i++) {
            if (vetor[i] < minimo) minimo = vetor[i];
            if (vetor[i] > maximo) maximo = vetor[i];
        }
        
        if (maximo == minimo) return;
        
        int numBaldes = 1000;
        ArrayList<ArrayList<Integer>> baldes = new ArrayList<>();
        for (int i = 0; i < numBaldes; i++) {
            baldes.add(new ArrayList<>());
        }
        
        for (int elemento : vetor) {
            int indice = (int)((double)(elemento - minimo) / (double)(maximo - minimo) * (numBaldes - 1));
            if (indice >= numBaldes) indice = numBaldes - 1;
            baldes.get(indice).add(elemento);
        }
        
        int k = 0;
        for (int i = 0; i < numBaldes; i++) {
            ArrayList<Integer> balde = baldes.get(i);
            if (balde.size() > 0) {
                int[] baldeTmp = new int[balde.size()];
                for (int j = 0; j < balde.size(); j++) {
                    baldeTmp[j] = balde.get(j);
                }
                insertionSort(baldeTmp);
                for (int valor : baldeTmp) {
                    vetor[k] = valor;
                    k++;
                }
            }
        }
    }
    
    public static int[] lerCsvDados(String caminho) throws IOException {
        String conteudo = new String(Files.readAllBytes(Paths.get(caminho)));
        String[] valores = conteudo.trim().split(",");
        int[] vetor = new int[valores.length];
        for (int i = 0; i < valores.length; i++) {
            if (!valores[i].isEmpty()) {
                vetor[i] = Integer.parseInt(valores[i].trim());
            }
        }
        return vetor;
    }
    
    public static void main(String[] args) {
        int[] tamanhos = {10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000};
        
        for (int n : tamanhos) {
            String dirDados = String.format("dados/n%06d", n);
            String dirResultados = String.format("resultados/java/n%06d", n);
            
            try {
                Files.createDirectories(Paths.get(dirResultados));
            } catch (IOException e) {
                System.err.println("Erro ao criar diretorio: " + e.getMessage());
                continue;
            }
            
            System.out.println("\nn=" + n);
            
            for (int execucao = 1; execucao <= 50; execucao++) {
                String arquivoEntrada = String.format("%s/run_%03d.csv", dirDados, execucao);
                String arquivoSaida = String.format("%s/run_%03d.csv", dirResultados, execucao);
                
                try {
                    int[] vetor = lerCsvDados(arquivoEntrada);
                    
                    long inicio = System.nanoTime();
                    bucketSort(vetor);
                    long fim = System.nanoTime();
                    
                    double tempoMs = (fim - inicio) / 1_000_000.0;
                    
                    try (PrintWriter writer = new PrintWriter(new FileWriter(arquivoSaida))) {
                        writer.println("n,tempo_ms,run");
                        writer.printf("%d,%.4f,%d%n", n, tempoMs, execucao);
                    }
                    
                    System.out.printf("Execucao %03d: %.4f ms%n", execucao, tempoMs);
                    
                } catch (IOException e) {
                    System.err.println("Erro ao processar " + arquivoEntrada);
                    continue;
                }
            }
        }
    }
}
