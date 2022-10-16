import subprocess

from datetime import datetime

command = subprocess.run(["ps", "aux"], stdout=subprocess.PIPE, encoding='utf-8')

process_system_list = command.stdout.splitlines()
headers = process_system_list.pop(0).split()

users = {}
cpu_total = 0.0
cpu_max = (0.0, "")
mem_total = 0.0
mem_max = (0.0, "")

for l in process_system_list:
    process_list = l.split()

    users.update({process_list[headers.index("USER")]: users.get(process_list[headers.index("USER")], 0) + 1})

    cpu_total += float(process_list[headers.index("%CPU")])
    mem_total += float(process_list[headers.index("%MEM")])

    if mem_max[0] <= float(process_list[headers.index("%MEM")]):
        mem_max = (float(process_list[headers.index("%MEM")]), process_list[headers.index("COMMAND")])
    if cpu_max[0] <= float(process_list[headers.index("%CPU")]):
        cpu_max = (float(process_list[headers.index("%CPU")]), process_list[headers.index("COMMAND")])

result = f"Отчёт о состоянии системы:\n" \
         f"Пользователи системы: {', '.join(users)}\n" \
         f"Процессов запущено: {len(process_system_list)}\n" \
         f"Пользовательских процессов:\n" \
         f"{'new_line'.join(map(lambda x: f'{x[0]}: {x[1]}', users.items()))}\n" \
         f"Всего памяти используется: {mem_total}%\n" \
         f"Всего CPU используется: {cpu_total}%\n" \
         f"Больше всего памяти использует: {mem_max[1][:20]} ({mem_max[0]}%)\n" \
         f"Больше всего CPU использует: {cpu_max[1][:20]} ({cpu_max[0]}%)".replace("new_line", "\n")

print(result)

with open(f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year}-"
          f"{datetime.now().hour}-{datetime.now().minute}-scan.txt", "w") as f:
    f.write(result)
