from re import findall

with open("numbers_and_trash.txt", "r", encoding="UTF-8") as fl:
    data = fl.read()

summary = 0
for found in findall(r"\d+", data):
    summary += int(found)

print("SUMMARY:", summary)