# 1
initial_sum = float(input("Начальная сумма вклада: "))
percent = float(input("Процент по вкладу: "))
years_number = float(input("Количество лет: "))

result_percents = initial_sum * percent * years_number / 100

print("Начисленные проценты:", result_percents)

print("-------------------------------")
# 2
celsius = float(input("Введите температуру в градусах Цельсия: "))
fahrenheits = 9/5 * celsius + 32
print(f"{celsius} градусов Цельсия равны {fahrenheits} градусам Фаренгейта")

print("-------------------------------")

# 3
n = input("n > ")
print(f"{n}{int(n) * 2}")
