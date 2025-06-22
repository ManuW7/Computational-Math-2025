import math

class FunctionCalculator:
    @staticmethod
    def calculate(func_id, x):
        if func_id == 1:
            return math.sin(x)
        elif func_id == 2:
            return x**2
        elif func_id == 3:
            return math.exp(x)
        elif func_id == 4:
            return math.sqrt(x)
        elif func_id == 5:
            return 1 / (1 + x**2)
        else:
            raise ValueError("Неизвестный идентификатор функции")


class Integrator:
    def __init__(self, func_id, a, b, epsilon, initial_n=4):
        self.func_id = func_id
        self.a = a
        self.b = b
        self.epsilon = epsilon
        self.initial_n = initial_n
   
    def left_rectangles(self, n):
        h = (self.b - self.a) / n
        integral = 0.0
        for i in range(n):
            x = self.a + i * h
            integral += FunctionCalculator.calculate(self.func_id, x)
        return integral * h
   
    def right_rectangles(self, n):
        h = (self.b - self.a) / n
        integral = 0.0
        for i in range(1, n+1):
            x = self.a + i * h
            integral += FunctionCalculator.calculate(self.func_id, x)
        return integral * h
   
    def middle_rectangles(self, n):
        h = (self.b - self.a) / n
        integral = 0.0
        for i in range(n):
            x = self.a + (i + 0.5) * h
            integral += FunctionCalculator.calculate(self.func_id, x)
        return integral * h
   
    def trapezoids(self, n):
        h = (self.b - self.a) / n
        integral = (FunctionCalculator.calculate(self.func_id, self.a) +
                   FunctionCalculator.calculate(self.func_id, self.b)) / 2
        for i in range(1, n):
            x = self.a + i * h
            integral += FunctionCalculator.calculate(self.func_id, x)
        return integral * h
   
    def simpson(self, n):
        if n % 2 != 0:
            n += 1  # Метод Симпсона требует четное количество разбиений
        h = (self.b - self.a) / n
        integral = FunctionCalculator.calculate(self.func_id, self.a) + FunctionCalculator.calculate(self.func_id, self.b)
        for i in range(1, n):
            x = self.a + i * h
            if i % 2 == 0:
                integral += 2 * FunctionCalculator.calculate(self.func_id, x)
            else:
                integral += 4 * FunctionCalculator.calculate(self.func_id, x)
        return integral * h / 3
   
    def runge_rule(self, method, p):
        n = self.initial_n
        integral_n = method(n)
        integral_2n = method(2 * n)
        error = abs(integral_2n - integral_n) / (2**p - 1)
       
        while error > self.epsilon:
            n *= 2
            integral_n = method(n)
            integral_2n = method(2 * n)
            error = abs(integral_2n - integral_n) / (2**p - 1)
       
        return integral_2n, 2 * n
   
    def integrate(self, method_name):
        methods = {
            'left_rectangles': (self.left_rectangles, 1),
            'right_rectangles': (self.right_rectangles, 1),
            'middle_rectangles': (self.middle_rectangles, 2),
            'trapezoids': (self.trapezoids, 2),
            'simpson': (self.simpson, 4)
        }
       
        if method_name not in methods:
            raise ValueError("Неизвестный метод интегрирования")
       
        method, p = methods[method_name]
        return self.runge_rule(method, p)


def print_functions():
    print("Доступные функции:")
    print("1. sin(x)")
    print("2. x^2")
    print("3. e^x")
    print("4. sqrt(x)")
    print("5. 1/(1+x^2)")


def print_methods():
    print("Доступные методы интегрирования:")
    print("1. Метод левых прямоугольников")
    print("2. Метод правых прямоугольников")
    print("3. Метод средних прямоугольников")
    print("4. Метод трапеций")
    print("5. Метод Симпсона")


print_functions()
func_id = int(input("Выберите функцию (1-5): "))

a = float(input("Введите нижний предел интегрирования: "))
b = float(input("Введите верхний предел интегрирования: "))
epsilon = float(input("Введите точность вычисления: "))

print_methods()
method_choice = int(input("Выберите метод интегрирования (1-5): "))

method_map = {
    1: 'left_rectangles',
    2: 'right_rectangles',
    3: 'middle_rectangles',
    4: 'trapezoids',
    5: 'simpson'
}

method_name = method_map[method_choice]

integrator = Integrator(func_id, a, b, epsilon)
result, n = integrator.integrate(method_name)

print("\nРезультаты интегрирования:")
print(f"Значение интеграла: {result}")
print(f"Число разбиений интервала: {n}")
print(f"Достигнутая точность: {epsilon}")


