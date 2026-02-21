async def handle(request):
    user_id = request.query.get('user_id', 'Неизвестно')
    
    # Получаем данные из базы
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT name, balance FROM users WHERE id = ?", (user_id,))
    user_data = cur.fetchone()
    
    # Получаем список всех заданий
    cur.execute("SELECT title, reward, link FROM tasks")
    tasks = cur.fetchall()
    conn.close()

    name = user_data[0] if user_data else "Пользователь"
    balance = user_data[1] if user_data else 0

    # Генерируем список заданий для HTML
    tasks_html = ""
    for t in tasks:
        tasks_html += f'''
        <div class="task-card">
            <div><b>{t[0]}</b><br><small>{t[1]} ₽</small></div>
            <a href="{t[2]}" class="btn">Выполнить</a>
        </div>'''

    # Читаем шаблон и меняем в нем данные на лету
    path = os.path.join(os.getcwd(), "index.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        content = content.replace("Привет, Bond", f"Привет, {name}")
        content = content.replace("⭐️ 0", f"⭐️ {balance}")
        content = content.replace("", tasks_html)
        return web.Response(text=content, content_type='text/html')
