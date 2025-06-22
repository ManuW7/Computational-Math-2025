package Program;

import java.io.*;
import java.util.*;

public class Program {
    
    // Проверяет, является ли матрица диагонально преобладающей
    private static boolean isDiagonallyDominant(double[][] A) {
        int n = A.length;
        for (int i = 0; i < n; i++) {
            double sum = 0;
            for (int j = 0; j < n; j++) {
                if (i != j) sum += Math.abs(A[i][j]);
            }
            if (Math.abs(A[i][i]) < sum) return false;
        }
        return true;
    }

    private static double[] gaussSeidel(double[][] A, double[] b, double tol, List<Double> errors) {
        int n = A.length;
        double[] x = new double[n]; // Начальное приближение (нулевое)
        int iterations = 0;
        double maxError;

        do {
            maxError = 0;
            for (int i = 0; i < n; i++) {
                double sum = 0;
                for (int j = 0; j < n; j++) {
                    if (i != j) {
                        sum += A[i][j] * x[j]; // Используем уже обновленные значения
                    }
                }
                double newX = (b[i] - sum) / A[i][i]; 
                maxError = Math.max(maxError, Math.abs(newX - x[i])); // Считаем максимальную ошибку
                x[i] = newX; // Обновляем x[i]
            }
            errors.add(maxError);
            iterations++;
        } while (maxError > tol);

        System.out.println("Итерации: " + iterations);
        return x;
    }
    
    // Чтение матрицы и вектора из файла
    private static void readFromFile(String filename, double[][] A, double[] b) throws IOException {
        BufferedReader reader = new BufferedReader(new FileReader(filename));
        int n = A.length;
        for (int i = 0; i < n; i++) {
            String[] line = reader.readLine().split(" ");
            for (int j = 0; j < n; j++) {
                A[i][j] = Double.parseDouble(line[j]);
            }
        }
        String[] line = reader.readLine().split(" ");
        for (int i = 0; i < n; i++) {
            b[i] = Double.parseDouble(line[i]);
        }
        reader.close();
    }

    public static void main(String[] args) throws IOException {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Введите размерность матрицы (n <= 20): ");
        int n = scanner.nextInt();
        if (n > 20 || n < 1) {
            System.out.println("Неверно введенная размерность");
            return;
        }
        
        double[][] A = new double[n][n];
        double[] b = new double[n];
        
        System.out.print("Прочитать данные из файла (f) или с клавиатуры (k)? ");
        char inputChoice = scanner.next().charAt(0);
        
        if (inputChoice == 'f') {
            System.out.print("Введите имя файла ");
            String filename = scanner.next();
            readFromFile(filename, A, b);
        } else {
            System.out.println("Введите коэффиценты матрицы ряд за рядом:");
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    A[i][j] = scanner.nextDouble();
                }
            }
            System.out.println("Введите вектор b:");
            for (int i = 0; i < n; i++) {
                b[i] = scanner.nextDouble();
            }
        }
        
        System.out.print("Введите точность: ");
        double tol = scanner.nextDouble();
        scanner.close();
        
        if (!isDiagonallyDominant(A)) {
            System.out.println("В матрице нет диагонального преобладания. Дальнейшее выполнение программы невозможно.");
            return;
        }
        
        // Вычисляем норму матрицы (максимальная сумма по строкам)
        double norm = Arrays.stream(A).mapToDouble(row -> Arrays.stream(row).map(Math::abs).sum()).max().orElse(0);
        System.out.println("Норма матрицы " + norm);
        
        List<Double> errors = new ArrayList<>();
        double[] result = gaussSeidel(A, b, tol, errors);
        System.out.println("Решение: " + Arrays.toString(result));
        System.out.println("Вектор погрешностей: " + errors);
    }
}
