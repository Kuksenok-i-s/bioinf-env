import os
import sys
import subprocess
import threading
import secrets

def main():
    try:
        start_env = '--start-env' in sys.argv or os.getenv('START_ENV') == '1'

        if start_env:
            print("Запускаем Jupyter Lab...")

            # Генерируем случайный токен
            token = secrets.token_hex(16)

            # Получаем IP-адрес хоста из аргумента или переменной окружения, иначе используем 'localhost'
            host_ip = None
            for arg in sys.argv:
                if arg.startswith('--host-ip='):
                    host_ip = arg.split('=')[1]
                    break
            if not host_ip:
                host_ip = os.getenv('HOST_IP', 'localhost')

            # Копируем текущее окружение и устанавливаем PYTHONUNBUFFERED
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'

            # Запускаем Jupyter Lab
            process = subprocess.Popen(
                ["conda", "run", "-n", "bioinfo", "jupyter", "lab",
                 "--ip=0.0.0.0", "--allow-root", "--no-browser",
                 f"--ServerApp.token={token}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1,
                env=env
            )

            # Функция для чтения потока вывода
            def stream_reader(stream, is_stderr=False):
                for line in iter(stream.readline, ''):
                    if line:
                        print(line.strip(), file=sys.stderr if is_stderr else sys.stdout)

            # Создаем потоки для чтения stdout и stderr
            stdout_thread = threading.Thread(target=stream_reader, args=(process.stdout,))
            stderr_thread = threading.Thread(target=stream_reader, args=(process.stderr, True))

            # Запускаем потоки
            stdout_thread.start()
            stderr_thread.start()

            # Выводим информацию о запуске
            print(f"Jupyter Lab запущен! Доступен по адресу: http://{host_ip}:8888/?token={token}")

            # Ожидаем завершения процесса
            process.wait()
            stdout_thread.join()
            stderr_thread.join()

    except Exception as e:
        print(f"Ошибка при запуске Jupyter Lab: {e}")

    if not start_env:
        print("""
Контейнер запущен без аргумента '--start-env' и без переменной окружения 'START_ENV'.

Чтобы запустить Jupyter Lab, используйте один из следующих вариантов:

1. Передайте аргумент '--start-env' при запуске контейнера:

   docker run -p 8888:8888 -v $(pwd):/workspace bioinformatics-env python /usr/local/src/startup.py --start-env

2. Установите переменную окружения 'START_ENV':

   docker run -p 8888:8888 -v $(pwd):/workspace -e START_ENV=1 bioinformatics-env

Монтирование текущей директории обеспечит доступ к вашим данным внутри контейнера в директории /workspace.
        """)

if __name__ == "__main__":
    main()
