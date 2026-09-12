import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
django.setup()
from mainapp.models import Staff, StaffInfo


def populate():
    # Очищаем таблицы перед заполнением
    Staff.objects.all().delete()
    StaffInfo.objects.all().delete()

    # Создаём тестовые записи для Staff
    staff_data = [
        {'login': 'doctor1', 'specialization': 'Терапевт'},
        {'login': 'doctor2', 'specialization': 'Кардиолог'},
        {'login': 'doctor3', 'specialization': 'Невролог'},
        {'login': 'doctor4', 'specialization': 'Педиатр'},
        {'login': 'doctor5', 'specialization': 'Хирург'},
    ]

    for data in staff_data:
        staff = Staff.objects.create(**data)
        print(f"Создан Staff: {staff.login} ({staff.specialization})")

        # Создаём соответствующие записи для StaffInfo
        staff_info = StaffInfo.objects.create(
            staff=staff,
            education=f"Высшее медицинское ({staff.specialization})",
            description=f"Опытный специалист в области {staff.specialization.lower()}"
        )
        print(f"Создан StaffInfo для {staff.login}")

    print("\nБаза данных заполнена тестовыми данными!")


if __name__ == '__main__':
    populate()