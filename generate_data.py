import sqlite3
import random
from datetime import date, timedelta

DB_PATH = "clinical_trials.db"


def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # На всякий случай очищаем таблицы перед новой генерацией
    cursor.execute("DELETE FROM measurements")
    cursor.execute("DELETE FROM patients")
    cursor.execute("DELETE FROM trials")

    # -------------------------
    # 1. Пациенты
    # -------------------------
    first_names = [
        "Иван", "Петр", "Анна", "Мария", "Олег", "Елена", "Сергей", "Наталья",
        "Дмитрий", "Ольга", "Алексей", "Татьяна", "Максим", "Ирина", "Артем",
        "Светлана", "Никита", "Юлия", "Андрей", "Виктория", "Павел", "Екатерина",
        "Михаил", "Дарья", "Константин", "Валерия", "Роман", "Алина", "Егор", "Полина"
    ]

    conditions = [
        "Гипертония", "Сахарный диабет", "Астма", "Артрит", "Мигрень",
        "Ишемическая болезнь сердца", "ХОБЛ", "Остеопороз"
    ]

    genders = ["Male", "Female"]

    patients = []
    for i in range(30):  # > 20
        name = random.choice(first_names) + f"_{i+1}"
        age = random.randint(18, 80)
        gender = random.choice(genders)
        condition = random.choice(conditions)
        patients.append((name, age, gender, condition))

    cursor.executemany("""
        INSERT INTO patients (name, age, gender, condition)
        VALUES (?, ?, ?, ?)
    """, patients)

    # -------------------------
    # 2. Исследования
    # -------------------------
    trial_names = [
        "Trial_Aspirin",
        "Trial_Ibuprofen",
        "Trial_Metformin",
        "Trial_Atorvastatin",
        "Trial_Lisinopril",
        "Trial_Amoxicillin"
    ]

    active_drugs = [
        "Аспирин",
        "Ибупрофен",
        "Метформин",
        "Аторвастатин",
        "Лизиноприл",
        "Амоксициллин"
    ]

    trials = []
    trial_date_ranges = []

    base_start = date(2023, 1, 1)

    for i in range(6):  # > 5
        start_date = base_start + timedelta(days=i * 30)
        end_date = start_date + timedelta(days=14)
        trials.append((trial_names[i], start_date.isoformat(), end_date.isoformat()))
        trial_date_ranges.append((start_date, end_date, active_drugs[i]))

    cursor.executemany("""
        INSERT INTO trials (trial_name, start_date, end_date)
        VALUES (?, ?, ?)
    """, trials)

    # -------------------------
    # 3. Измерения
    # -------------------------
    # Берем id пациентов и исследований из базы
    cursor.execute("SELECT patient_id FROM patients")
    patient_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT trial_id FROM trials ORDER BY trial_id")
    trial_ids = [row[0] for row in cursor.fetchall()]

    measurements = []

    # Для каждого исследования:
    # - 10 пациентов на плацебо
    # - 10 пациентов на активном препарате
    # - по 3 измерения на каждого пациента
    # Итого: 6 * 20 * 3 = 360 измерений (> 200)
    for idx, trial_id in enumerate(trial_ids):
        start_date, end_date, active_drug = trial_date_ranges[idx]

        shuffled_patients = patient_ids[:]
        random.shuffle(shuffled_patients)

        placebo_group = shuffled_patients[:10]
        active_group = shuffled_patients[10:20]

        # Плацебо
        for patient_id in placebo_group:
            measurement_dates = [
                start_date,
                start_date + timedelta(days=7),
                end_date
            ]
            base_score = random.randint(30, 70)
            scores = [
                max(0, min(100, base_score + random.randint(-5, 5))),
                max(0, min(100, base_score + random.randint(-7, 7))),
                max(0, min(100, base_score + random.randint(-10, 10))),
            ]
            for m_date, score in zip(measurement_dates, scores):
                measurements.append((
                    patient_id,
                    trial_id,
                    m_date.isoformat(),
                    "Плацебо",
                    score
                ))

        # Активный препарат
        for patient_id in active_group:
            measurement_dates = [
                start_date,
                start_date + timedelta(days=7),
                end_date
            ]
            base_score = random.randint(30, 70)
            # делаем небольшую тенденцию к улучшению
            scores = [
                max(0, min(100, base_score + random.randint(-5, 5))),
                max(0, min(100, base_score + random.randint(0, 10))),
                max(0, min(100, base_score + random.randint(5, 20))),
            ]
            for m_date, score in zip(measurement_dates, scores):
                measurements.append((
                    patient_id,
                    trial_id,
                    m_date.isoformat(),
                    active_drug,
                    score
                ))

    cursor.executemany("""
        INSERT INTO measurements (patient_id, trial_id, measurement_date, drug, condition_score)
        VALUES (?, ?, ?, ?, ?)
    """, measurements)

    conn.commit()

    # Выведем контрольные числа
    cursor.execute("SELECT COUNT(*) FROM patients")
    print("Patients:", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM trials")
    print("Trials:", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM measurements")
    print("Measurements:", cursor.fetchone()[0])

    conn.close()


if __name__ == "__main__":
    main()