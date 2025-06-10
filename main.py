"""
Задание 1: Управление проектной структурой и файловой системой
    1.1. Создание и управление директориями:
        - Напишите скрипт, который автоматически создаст следующую структуру директорий для вашего проекта:
            project_root/
            ├── data/
            │   ├── raw/
            │   ├── processed/
            ├── logs/
            ├── backups/
            └── output/    
        
        Убедитесь, что все директории созданы, и если они уже существуют, не вызывайте ошибку.
    
    1.2. Создание и запись данных в файлы:
        - В директории `data/raw/` создайте несколько текстовых файлов с произвольным содержимым на разных языках, используя разные кодировки (например, UTF-8, ISO-8859-1).
        - Заполните директорию `logs/` лог-файлом с записями о выполнении предыдущих шагов, включая дату и время создания файлов и директорий.
"""

import os
from datetime import datetime

def create_project_structure() -> str:
    """ Создание и управление директориями """
    project_root = "project_root"

    if os.path.exists(project_root):
        print("Структура директорий уже создана")
        return
    
    dirs = [
        os.path.join(project_root, "logs"), # Сначала создать этот каталог, иначе логи будет некуда писать
        os.path.join(project_root, "data/raw"),
        os.path.join(project_root, "data/processed"),
        os.path.join(project_root, "backups"),
        os.path.join(project_root, "output"),
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        log_creation(dir_path, "directory")
    
    return project_root

def log_creation(path, obj_type):
    """ Логирование создания файлов/директорий """
    log_file = os.path.join("project_root", "logs", "creation.log")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - Создан {obj_type}: {path}\n"
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry)

def create_sample_files(project_root):
    """ Создание и запись текста на разных языках в файлы с разной кодировкой """
    raw_data_dir = os.path.join(project_root, "data", "raw")
    
    # Файлы с разными кодировками
    text = "Hello World! This is a test file. Привет, мир! Это тестовый файл. Hallo Welt! Dies ist eine Testdatei. Bonjour le monde! Ceci est un fichier test."
    files_content = [
        ("text_utf8.txt", text, "utf-8"),
        ("text_windows1251.txt", text, "windows-1251"),
    ]
    
    for filename, content, encoding in files_content:
        filepath = os.path.join(raw_data_dir, filename)
        with open(filepath, "w", encoding=encoding) as f:
            f.write(content)
        log_creation(filepath, "file") # Логгирование

"""
Задание 2: Чтение, преобразование и сериализация данных
    2.1. Чтение и обработка данных:
        - Напишите скрипт, который будет автоматически читать все файлы из директории `data/raw/`, корректно определяя их кодировки.
        - Выполните преобразование данных из каждого файла, заменяя в них все заглавные буквы на строчные и наоборот.
        - Сохраните обработанные данные в новые файлы в директорию `data/processed/` с сохранением исходных имен файлов, но добавив к ним суффикс `_processed`.

    2.2. Сериализация данных:
        - Напишите скрипт для сериализации содержимого всех файлов из директории `data/processed/` в один JSON-файл.
        - Включите в этот JSON-файл следующую информацию:
            - Имя файла.
            - Исходный текст.
            - Преобразованный текст.
            - Размер файла в байтах.
            - Дата последнего изменения файла.
       - Сохраните JSON-файл в директорию `output/` с именем `processed_data.json`.

"""

import chardet
import json

def detect_encoding(filepath):
    """ Определение кодировки файла """
    with open(filepath, 'rb') as f:
        raw_data = f.read()
    return chardet.detect(raw_data)['encoding']

def process_text(text):
    """ Преобразование текста: инверсия регистра букв """
    return text.swapcase()

def process_raw_files(project_root):
    """ 2.1. Чтение и обработка данных """
    
    raw_dir = os.path.join(project_root, "data", "raw")
    processed_dir = os.path.join(project_root, "data", "processed")
    
    for filename in os.listdir(raw_dir):
        raw_filepath = os.path.join(raw_dir, filename)
        if os.path.isfile(raw_filepath):
            try:
                encoding = detect_encoding(raw_filepath)
                
                with open(raw_filepath, "r", encoding=encoding) as f:
                    content = f.read()
                
                processed_content = process_text(content)
                
                processed_filename = f"{os.path.splitext(filename)[0]}_processed.txt"
                processed_filepath = os.path.join(processed_dir, processed_filename)
                
                with open(processed_filepath, "w", encoding="utf-8") as f:
                    f.write(processed_content)
                
            except Exception as e:
                print(f"Error processing file {filename}: {str(e)}")

def serialize_to_json(project_root):
    """2.2. Сериализация данных в JSON"""
    processed_dir = os.path.join(project_root, "data", "processed")
    output_dir = os.path.join(project_root, "output")
    output_file = os.path.join(output_dir, "processed_data.json")
    
    data = []
    
    for filename in os.listdir(processed_dir):
        filepath = os.path.join(processed_dir, filename)
        if os.path.isfile(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    processed_content = f.read()
                
                file_stats = os.stat(filepath)
                size = file_stats.st_size
                last_modified = datetime.fromtimestamp(file_stats.st_mtime).isoformat()
                
                raw_filename = filename.replace("_processed", "")
                raw_filepath = os.path.join(project_root, "data", "raw", raw_filename)
                
                if os.path.exists(raw_filepath):
                    encoding = detect_encoding(raw_filepath)
                    with open(raw_filepath, "r", encoding=encoding) as f:
                        original_content = f.read()
                else:
                    original_content = "Оригинальный файл не найден"
                
                data.append({
                    "filename": filename,
                    "original_text": original_content,
                    "processed_text": processed_content,
                    "file_size_bytes": size,
                    "last_modified": last_modified
                })
                
            except Exception as e:
                print(f"Ошибка обработки файла {filename} : {str(e)}")
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

"""
Задание 3: Работа с резервными копиями и восстановлением данных
    1. Создание резервной копии:
        - Напишите скрипт, который автоматически создаст архив резервной копии всех файлов из директории `data/`
        и сохранит его в директорию `backups/` с именем `backup_<дата>.zip`, где `<дата>` — текущая дата в формате `YYYYMMDD`.
    
    2. Восстановление данных:
        - Напишите скрипт для разархивирования и восстановления данных из созданного архива резервной копии.
        Убедитесь, что все файлы восстановлены в соответствующие директории, и их содержимое не повреждено.
"""

import zipfile

def create_backup(project_root):
    """ Создание резервной копии """
    data_dir = os.path.join(project_root, "data")
    backups_dir = os.path.join(project_root, "backups")
    today = datetime.now().strftime("%Y%m%d")
    backup_filename = f"backup_{today}.zip"
    backup_path = os.path.join(backups_dir, backup_filename)
    
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(data_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=project_root)
                zipf.write(file_path, arcname)
    
    return backup_path

def restore_backup(project_root, backup_path=None):
    """ Восстановление данных из резервной копии """
    if backup_path is None:
        backups_dir = os.path.join(project_root, "backups")
        backups = sorted([f for f in os.listdir(backups_dir) if f.startswith("backup_")], reverse=True)
        if not backups:
            raise FileNotFoundError("Файл архива не найден")
        backup_path = os.path.join(backups_dir, backups[0])
    
    with zipfile.ZipFile(backup_path, 'r') as zipf:
        zipf.extractall(project_root)

"""
Задание 4: Дополнительные задачи с сериализацией и JSON Schema
    1. Работа с пользовательскими классами и JSON:
        - Создайте класс `FileInfo`, который будет хранить информацию о файлах, включающую:
            - Имя файла.
            - Полный путь к файлу.
            - Размер файла.
            - Дата создания и последнего изменения файла.
        - Напишите скрипт, который собирает информацию обо всех файлах в директории `data/processed/` и сериализует их в JSON-файл.
        Убедитесь, что при десериализации данные восстанавливаются корректно.
    2. Валидация JSON с использованием JSON Schema:
        - Создайте JSON Schema для проверки структуры данных, созданной в предыдущем задании.
        - Напишите скрипт, который проверяет валидность JSON-файла, созданного в предыдущем задании, с использованием созданной JSON Schema.
        - Обработайте возможные ошибки валидации, предоставив отчет о найденных несоответствиях.
"""

from jsonschema import validate, ValidationError

class FileInfo:
    """ Класс для хранения информации о файлах"""
    def __init__(self, filepath):
        self.filename = os.path.basename(filepath)
        self.full_path = os.path.abspath(filepath)
        self.size = os.path.getsize(filepath)
        self.created = datetime.fromtimestamp(os.path.getctime(filepath)).isoformat()
        self.modified = datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
    
    def to_dict(self):
        return {
            "filename": self.filename,
            "full_path": self.full_path,
            "size": self.size,
            "created": self.created,
            "modified": self.modified
        }
    
def serialize_file_info(project_root):
    """ Сбор информации о файлах и сериализация в JSON """
    processed_dir = os.path.join(project_root, "data", "processed")
    output_dir = os.path.join(project_root, "output")
    output_file = os.path.join(output_dir, "file_info.json")
    
    file_info_list = []
    
    for filename in os.listdir(processed_dir):
        filepath = os.path.join(processed_dir, filename)
        if os.path.isfile(filepath):
            file_info = FileInfo(filepath)
            file_info_list.append(file_info.to_dict())
    
    # Сериализация в JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump([fi for fi in file_info_list], f, indent=4, ensure_ascii=False)
    
    return output_file

def validate_json_with_schema(json_file):
    """ Валидация JSON с использованием JSON Schema """
    # Описание схемы
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "filename": {"type": "string"},
                "full_path": {"type": "string"},
                "size": {"type": "integer", "minimum": 0},
                "created": {"type": "string", "format": "date-time"},
                "modified": {"type": "string", "format": "date-time"}
            },
            "required": ["filename", "full_path", "size", "created", "modified"],
            "additionalProperties": False
        }
    }
    
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    validation_errors = []
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        validation_errors.append(str(e))
    
    report = {
        "valid": len(validation_errors) == 0,
        "errors": validation_errors,
        "checked_files": len(data),
        "schema_used": schema
    }
    
    report_file = os.path.join(os.path.dirname(json_file), "validation_report.json")
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    
    return report

"""
Задание 5: Отчёт и анализ проделанной работы
    1. Создание итогового отчёта:
        - Сгенерируйте отчёт в текстовом файле или в формате JSON с анализом выполнения всех заданий:
        - Описание возникших трудностей и способы их решения.
        - Время, затраченное на выполнение каждого задания.
        - Выводы о проделанной работе и предложенные улучшения.
    2. Логирование и контроль версий: по желанию, но если хотите, то сделайте)
    "   - Подумайте о добавлении логирования во все скрипты для отслеживания ошибок и прогресса выполнения заданий.
    "   - Опишите, как можно было бы интегрировать систему контроля версий (например, Git) в выполнение этого задания для отслеживания изменений и управления проектом.
"""
def home_work_report(project_root: str):
    report_file = os.path.join(os.path.dirname(project_root), "home_work_report.json")
    report = {
        "Возникшие трудности и способы их решения": {
            "1": "Особых трудностей не было",
            "2": "Совершил досадную ошибку с каталогом logs (см. комментарий к первому заданию)",
            "3": "Работа в целом несложная, но объёмная. Потратил в итоге 3 часа"
        },
        "Логирование и контроль версий": {
            "1": "Добавления логгирования для отслеживания ошибок и прогрессы выполнения заданий можно использовать декораторы, позволяющие отслежитвать время и количество запуска скриптов",
            "2": "Git позволяет создавать перехватчики событий (hooks) - пример Husky. Может перехватчики можно как-то задействовать, но при этом придётся разворачивать систему тестирования"
        }
    }
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    
# Основной скрипт для выполнения всех заданий
def main():
    print("Задание 1: Управление проектной структурой и файловой системой")
    project_root = create_project_structure()
    print(f"Root: {project_root}")
    create_sample_files(project_root)
    
    print("Задание 2: Чтение, преобразование и сериализация данных")
    process_raw_files(project_root)
    serialize_to_json(project_root)
    
    print("Задание 3: Работа с резервными копиями и восстановлением данных")
    backup_path = create_backup(project_root)
    print(f"Создана резервная копия: {backup_path}")
    
    restore_backup(project_root, backup_path)
    print("Восстановление из резервной копии выполнено")
    
    print("Задание 4: Дополнительные задачи с сериализацией и JSON Schema")
    json_file = serialize_file_info(project_root)
    print(f"Создан JSON с информацией о файлах: {json_file}")
    
    report = validate_json_with_schema(json_file)
    print(f"Результат валидации: {'Успешно' if report['valid'] else 'С ошибками'}")
    if not report['valid']:
        print("Ошибки валидации:")
        for error in report['errors']:
            print(f"- {error}")

    home_work_report(project_root)

if __name__ == "__main__":
    if os.path.exists("project_root"):
        print("Структура директорий уже создана. Удалите 'project_root', и запустите программу снова")
    else:
        main()
