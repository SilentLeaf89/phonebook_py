import json
import sys

from utils import messages
from utils.printer import printer_contacts
from utils.info import _request_info


def create_note() -> tuple[str, dict[str, str]]:
    """Создание записи в телефонной книге

    Returns:
        tuple[str, dict[str, str]]: кортеж с id и содержимым добавленной записи
    """
    print(messages.CREATE_NEW_NOTE)
    note = _request_info()
    id = " ".join([note["first_name"], note["middle_name"], note["last_name"]])
    for notes in storage:
        if notes.get(id):
            print(messages.NOTE_EXISTS)
            return "", {}
    with open("phonebook.txt", "a", encoding="utf-8") as phonebook:
        phonebook.write(json.dumps({id: note}, ensure_ascii=False) + "\n")

    print(messages.CREATE_SUCCESSFUL)
    printer_contacts([{id: note}])
    return id, note


def update_note(
    find_note: dict[str, dict[str, str]]
) -> tuple[str, dict[str, str]]:
    """Обновление записи через общение с пользователем

    Args:
        find_note (dict[str, dict[str, str]]): найденные записи после поиска

    Returns:
        tuple[str, dict[str, str]]: кортеж из обновленного id и
        содержимого записи
    """
    print(messages.UPDATE_NOTE)
    printer_contacts([find_note])

    update_note = _request_info()
    update_id = " ".join(
        [
            update_note["first_name"],
            update_note["middle_name"],
            update_note["last_name"],
        ]
    )
    for notes in storage:
        if notes.get(update_id):
            print(messages.NOTE_EXISTS)
            return "", {}
    return update_id, update_note


def update_find_notes(find_notes: list[dict[str, dict[str, str]]]):
    """Обновляет найденную запись, если она одна

    Args:
        find_notes (list[dict[str, dict[str, str]]]): найденные записи
        после поиска
    """
    find_note = _check_find_notes(find_notes)
    if find_note:
        updated_id, updated_note = update_note(find_note)
        if updated_id:
            storage.remove(find_note)
            storage.append({updated_id: updated_note})
            save_storage_to_file()
            print(messages.UPDATE_SUCCESSFUL)
            printer_contacts([{updated_id: updated_note}])


def delete_find_note(find_notes: list[dict[str, dict[str, str]]]):
    """Удаление найденной записи через подтверждение пользователем, если
    найдено больше записей - информационное сообщение

    Args:
        find_notes (list[dict[str, dict[str, str]]]): найденные записи
        после поиска
    """
    find_note = _check_find_notes(find_notes)
    if find_note:
        printer_contacts(find_notes)
        deleter_note = input(messages.CONFIRM_DELETE)
        match deleter_note:
            case "Y" | "y" | "yes" | "Да" | "да" | "Ок" | "ок" | "ОК" | "ДА":
                storage.remove(find_notes[0])
                save_storage_to_file()
                print(f"{messages.DELETE_SUCCESSFUL}")
            case _:
                print(messages.CANCEL_DELETE)


def search_note() -> list[dict[str, dict[str, str]]]:
    """Поиск по id и содержимому записей. Сначала проводится поиск по
    уникальным id, а если ничего не найдено, то поиск расширяется на значения
    остальных полей

    Returns:
        list[dict[str, dict[str, str]]]: найденные записи в формате списка
    """
    query = input(messages.SEARCH)
    result = []

    # поиск по id
    for line in storage:
        for id in line.keys():
            if query in id:
                result.append(line)
    if len(result) > 0:
        return result

    # поиск по полям
    for line in storage:
        for notes in line.values():
            for note in notes.values():
                if query in note:
                    result.append(line)
    return result


def viewer(notes: list[dict[str, dict[str, str]]], page_number: int) -> None:
    """Команда постраничного просмотра записей

    Args:
        notes (list[dict[str, dict[str, str]]]): записи телефонной книжки
        в формате списка
        page_number (int): текущая страница просмотра записей
    """
    size = len(notes)
    slice_start, slice_end = _calc_slices(size, page_number)
    printer_contacts(notes[slice_start:slice_end])
    print(
        f"""Показаны с {slice_start + 1} по {slice_end} записи.
Всего записей: {size}\n"""
    )
    while True:
        operation = input(messages.SLICE_MENU)
        match operation:
            case "N" | "n" | "next":  # next page
                if size > slice_end:
                    page_number += 1
                    slice_start, slice_end = _calc_slices(size, page_number)
                    printer_contacts(notes[slice_start:slice_end])
                else:
                    print(f"{messages.END_SLICE}")
                    printer_contacts(notes[slice_start:slice_end])
            case "P" | "p" | "prev":  # prev page
                if page_number > 1:
                    page_number -= 1
                    slice_start, slice_end = _calc_slices(size, page_number)
                    printer_contacts(notes[slice_start:slice_end])
                else:
                    print(messages.START_SLICE)
                    printer_contacts(notes[slice_start:slice_end])

            case _:
                break
        print(
            f"""Показаны с {slice_start + 1} по {slice_end} записи.
Всего записей: {size}\n"""
        )


def load_phonebook() -> list[dict[str, dict[str, str]]]:
    """Загрузка телефонной книги из файла в "хранилище"

    Returns:
        list: список с записями из телефонной книги
    """
    storage = []
    try:
        with open("phonebook.txt", "r", encoding="utf-8") as f:
            for line in f.readlines():
                note = json.loads(line)
                storage.append(dict(note))
    except FileNotFoundError:
        return []
    return storage


def save_storage_to_file():
    """Сохранение данных из хранилища (storage) в файл"""
    with open("phonebook.txt", "w", encoding="utf-8") as phonebook:
        for line in storage:
            phonebook.write(json.dumps(line, ensure_ascii=False) + "\n")


def _calc_slices(size: int, page_number: int) -> tuple[int, int]:
    """Расчитывает индексы срезов списка просматриваемых записей

    Args:
        size (int): количество элементов в списке записей
        page_number (int): текущая страница команды просмотра

    Returns:
        tuple[int, int]: начальный и конечный индекс среза
    """
    slice_start = (page_number - 1) * PAGE_SIZE
    slice_end = min(page_number * PAGE_SIZE, size)
    return slice_start, slice_end


def _check_find_notes(
    find_notes: list[dict[str, dict[str, str]]]
) -> dict[str, dict[str, str]] | None:
    """Возвращает либо найденный объект, если он один,
    иначе - сообщение об ошибке

    Args:
        find_notes (list[dict[str, dict[str, str]]]): найденные записи
        после поиска
    Returns:
        dict[str, dict[str, str]] | None: формат записи в storage,
    если запись одна
    """
    if len(find_notes) == 0:
        print(messages.SEARCH_NOT_FOUND)
    elif len(find_notes) > 1:
        print(messages.SEARCH_MORE_ONE)
    elif len(find_notes) == 1:
        return find_notes[0]
    else:
        print(messages.UNEXPECTED_ERROR)
        sys.exit(0)


def main_menu(storage: list[dict[str, dict[str, str]]], page_number: int):
    """Основное меню, позволяющее взаимодействовать пользователю
    с телефонной книжкой

    Args:
        storage (list[dict[str, dict[str, str]]]): список записей в
    телефонной книжке
    """
    operation = input(messages.MAIN_MENU)
    match operation:
        case "C" | "c" | "create":
            id, note = create_note()
            if id:
                storage.append({id: note})
        case "U" | "u" | "update":
            find_notes = search_note()
            update_find_notes(find_notes)
        case "D" | "d" | "delete":
            find_notes = search_note()
            delete_find_note(find_notes)
        case "V" | "v" | "view":
            if len(storage) == 0:
                print(messages.STORAGE_IS_EMPTY)
            else:
                viewer(storage, page_number)
        case "S" | "s" | "search":
            find_notes = search_note()
            if len(find_notes) == 0:
                print(messages.SEARCH_NOT_FOUND)
            else:
                viewer(find_notes, page_number)

        case "Q" | "q" | "exit" | "quit":
            sys.exit(0)


if __name__ == "__main__":
    PAGE_SIZE = 20  # количество записей на странице команды просмотра
    page_number = 1
    print(messages.WELCOME)
    storage = load_phonebook()
    while True:
        main_menu(storage, page_number)
