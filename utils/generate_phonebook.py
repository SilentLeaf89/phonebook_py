import json

from faker import Faker

fake = Faker("ru_RU")

NUM_NOTES = 300

storage = []
for _ in range(NUM_NOTES):
    note = {
        "last_name": fake.last_name(),
        "first_name": fake.first_name(),
        "middle_name": fake.middle_name(),
        "organization": fake.company(),
        "work_phone": fake.phone_number(),
        "personal_phone": fake.phone_number(),
    }
    id = " ".join([note["first_name"], note["middle_name"], note["last_name"]])
    storage.append({id: note})

with open("phonebook.txt", "w", encoding="utf-8") as phonebook:
    for line in storage:
        phonebook.write(json.dumps(line, ensure_ascii=False) + "\n")
