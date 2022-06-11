После загрузки папки с проектом с gitlab на локальный компьютер сделать следующее:
1. Открыть командную строку (cmd.exe)
2. Войти в папку scrumgitlab
3. Запустить команду: python -m venv venv
4. Запустить виртуальное окружение: venv\scripts\activate
5. перейти в папку hh: cd hh
6. Установить все зависимости: pip install -r requirements.txt

Готово! 
После этого: python manage.py runserver


{% csrf_token %} ERROR == Debug=False
