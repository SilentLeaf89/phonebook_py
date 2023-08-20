def printer_contacts(storage: list[dict[str, dict[str, str]]]):
    counter = {}
    for notes in storage[0].values():
        for id in notes.keys():
            counter[id] = len(id)

    # расчёт максимальной длины колонок
    for line in storage:
        for notes in line.values():
            for k, v in notes.items():
                if len(v) > counter.get(k, 0):
                    counter[k] = len(v)

    # шапка
    print()
    for k, v in counter.items():
        print(f"{k:{v}} | ", end="")
    print()

    # разделитель
    r = f'{"-"*sum(counter.values(), len(counter) * 3)}'
    print(r[:-1])

    # содержимое
    for line in storage:
        for notes in line.values():
            for k, v in notes.items():
                print(f"{v:{counter[k]}} | ", end="")
            print()
    print()
