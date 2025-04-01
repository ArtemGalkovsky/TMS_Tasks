"""
5. В текстовый файл построчно записаны фамилия и имя
учащихся класса и оценка за контрольную. Вывести на экран
всех учащихся, чья оценка меньше трёх баллов.
"""

with open("students_marks", "r", encoding="utf-8") as fl:
    data = fl.readlines()

noobs: dict[str, int] = {} # dict[str name, int mark]
for student_data in data:
    split_student_data = student_data.strip().split()

    name, mark = " ".join(split_student_data[:-1]), split_student_data[-1]

    print(f"Checking {name}: {mark}")

    if not mark.isnumeric():
        raise ValueError(f"Incorrect mark for {name}: {mark}")

    mark = int(mark)
    if mark > 2:
        continue

    print("NOOOOOOOOOOOOOOB FOUND:", name, "MARK IS", mark)
    noobs[name] = mark



print("AND......... NOOBS ARE:")
for noob, mark in noobs.items():
    print(noob, mark)

# ))))))))))