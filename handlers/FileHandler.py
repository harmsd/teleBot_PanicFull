import io
import struct

def read_ips_file(file_path):
    try:
        f = open(file_path, 'r')
        data = f.readlines()
        return data
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден.")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None
    
file_path = "filePanicFool/panic-full-2025-06-23-183205.000.ips"
read_data = read_ips_file(file_path)


if read_data:
    print(read_data[3])