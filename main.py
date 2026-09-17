import random
from models import *
from flask import Flask,render_template,redirect,request,session,jsonify
from peewee import fn

app = Flask("myapp")
app.secret_key = 'Poawlh9aw1982;lawfi'
"""
Идеи для улучшения кода:
1.Вынос в отдельную функцию кода для возврата json-а
2.Разделение обязанностей в функции использования предметов
3.Вынос функции обновления стат игрока на бэкенде в модель таблицы


TODO: КРИТИЧЕСКИЕ БАГИ В ЛОГИКЕ КОДА (НАЙТИ И ИСПРАВИТЬ САМОМУ)

1. КРИТИЧЕСКИЙ БАГ С ID ЛОКАЦИЙ И ПОДРАБОТОК:
   В роутах вроде /trailer, /tunnel, /bottles написано:
   player.location = 2 или player.job = 1.
   Так делать нельзя! Поля ForeignKeyField в Peewee ждут целый ОБЪЕКТ, 
   а не просто цифру. Из-за этого база данных работает непредсказуемо.
   Как исправить: Либо передавать объект целиком, либо вспомнить про 
   скрытое поле с суффиксом '_id', которое принимает чистые цифры.




Обновлено:
1.В локации добавлено Base_xp
2.Все функции переработаны, макаронного кода почти нет
3.Пофикшены кулдауны
"""


"""
Структура session:
{
    login - Логин игрока
    is_auth - Авторизован ли Игрок
    location - Айди локации(Возможно ошибка с тем что в сессии не меняется локация при редиректе, 
    а возможно это поле вообще лишнее)
}
"""
#==============================================================================
"""ФУНЦКИИ-ХЕЛПЕРЫ"""
"""Общие хелперы"""
# 1.Возвращение данных игрока
def send_player_data(player, status, extra_data=None):
    data = {
        "status":status,
        "hp":player.hp,
        "energy":player.energy,
        "food":player.satiety,
        "water":player.hydration,
        "money":player.money,
        "xp":player.xp, 
        "time":player.time
    }
    if extra_data:
        data.update(extra_data)

    return jsonify(data)
# 2.

"""Хелперы для обработки клика"""
# Обработка квеста
def random_event(player):
    location = player.location_id
    # Достаем одну единственную ситуацию из всех перемешанных ситуаций
    active_cooldowns = (Cooldowns.select(Cooldowns.situation_id)
                        .where((Cooldowns.player_id == player.id) & (Cooldowns.available_at > 0)))

    situation = (Random_situation
                 .select()
                 .where(
                    (Random_situation.location_id == player.location_id) &
                    (Random_situation.id << active_cooldowns == False))
                 .order_by(fn.Random())
                 .first())
    if not situation or random.randint(0,100) >= situation.chance:
        return None
    
    cooldown = Cooldowns.get_or_none(player_id = player.id, situation_id = situation.id)
    if cooldown and cooldown.available_at > 0:
        return None

    new_cooldown = random.randrange(1440, 2881, 10)
    if cooldown:
        cooldown.available_at = new_cooldown
        cooldown.save()
    else:
        Cooldowns.create(available_at = new_cooldown, player_id = player.id, situation_id = situation.id)

    return send_player_data(player, "active", extra_data={
        "situation_id": situation.id,
        "name": situation.name,
        "description": situation.description,
        "choice": [situation.choice_name1, situation.choice_name2, situation.choice_name3]
    })  
    return None  

"""API"""

# Покупка предмета
@app.route("/buy_item", methods=["POST"])
def buy_item():
    try_to_buy_item = request.get_json()
    item = Items.get_or_none(id=try_to_buy_item.get("item_id"))
    player = Player.get_or_none(login=session.get("login"))
    # Проверка на существование игрока и предмета
    if item and player:
        # Проверка на наличие денег у игрока
        if player.money >= item.price:
            player.money -= item.price
            player.save()
            # Создание слота или увеличение количества предметов в инвентаре
            slot, created = Inventory.get_or_create(
                player_id=player.id,
                item_id=item.id,
                defaults={'quantity': 0, 'is_equipped': False}
            )
            slot.quantity += 1
            slot.save()
            
            return jsonify({"status":"success","message": f"Вы успешно купили: {item.name}","money": player.money})
        else:
            return jsonify({"status":"error","message":"Не хватает денег"})
    else:
        return jsonify({"status":"error","message":"Не найден предмет или игрок"})


    
# Отрисовка магазина
@app.route("/shop", methods=["POST"])
def shop():
    data = request.get_json()   
    
    # Немного костыльное решение, в SQL одежда хранится в 4 разных типах, а js присылает один тип cloth, приходится делить тут на четыре подтипа
    # P.S Отрисовка происходит по категориям, так что пользователь открывает категорию одежды в магазине и из за этого четыре типа превращаются в один
    if data.get("category_type") == "cloth":
        # Выбираем предметы, у которых item_type равен любому слову из списка одежды
        items = Items.select().where(
            (Items.price >= 0) & 
            (Items.item_type.in_(["jacket", "t-shirt", "pants", "boots"]))
        )
    else:
        # Для всех остальных категорий (еда, гитары, оборудование) оставляем твой старый точный поиск
        items = Items.select().where(
            (Items.price >= 0) & 
            (Items.item_type == data.get("category_type"))
        )
    # Список с предметами из базы
    sorted_items = []
    # Перебор и запихивание в sorted_items предметов пришедших из SQL в items
    for item in items:
        sorted_items.append({"id":item.id,"name":item.name,"price":item.price,"description":item.description,"item_type":item.item_type})
    return jsonify(sorted_items)

# Использование предмета (кажется логика слишком огромной)
@app.route("/use_item", methods=["POST"])
def use_item():
    # Получение данных из базы и из json
    player = Player.get_or_none(login=session.get("login"))
    data = request.get_json()
    item = Inventory.get_or_none(id=data.get("inv_id"), player_id=player.id)

    # Отлов ошибки если пользователь попытается применить предмет которого у него нет
    if not item or item.quantity <= 0:
        return jsonify({"status": "error", "message": "Предмет не найден"})
    else:
        # Можно запутаться, item_stats это обращение к таблице базовых предметов с айди используемого предмета из инвентаря игрока
        item_stats = item.item_id

        # Логика по типам, если это используемый предмет то уменьшается количество и восстанавливаются статы
        if item_stats.item_type in ["food", "drink", "meds"]:
            # Удаление/уменьшение количества (Важно что >1, если будет >0 то останется пустая карточка и запись о предмете с количеством 0)
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete_instance()
            # Лог в консоль
            print(f"Используем предмет: {item_stats.name}, Тип: {item_stats.item_type}, Восстанавливает жажды: {item_stats.restore_hydration}")
            # Применение стат предмета к статам игрока
            # (Min и Max используются для предотвращения переполнения шкалы и засчитывания статы больше максимального значения стат игрока)
            player.satiety = min(player.max_satiety, player.satiety + item_stats.restore_satiety)
            player.hydration = min(player.max_hydration, player.hydration + item_stats.restore_hydration)
            player.hp = min(player.max_hp, player.hp + item_stats.influence_on_hp)
            player.energy = min(player.max_energy, player.energy + item_stats.energy_change)
            player.save()
            return send_player_data(player, "success")

        # Логика для предметов которые нельзя использовать
        elif item_stats.item_type in ["guitar", "eqp", "jacket", "t-shirt", "pants", "boots"]:
            # Если предмет экипирован то статы снимаются и сама шмотка тоже
            if item.is_equipped:
                player.charisma_bonus -= item_stats.charismabonus 
                player.xp_bonus -= item_stats.xpbonus - 1
                item.is_equipped = False
                item.save()
                return send_player_data(player, "unequipped")
            # Если слот занят другой шмоткой такого же типа то сервер не даст надеть его
            already_equipped = (Inventory.select().join(Items).where(Inventory.player_id == player.id, Inventory.is_equipped == True, Items.item_type == item_stats.item_type).first())
            if already_equipped:
                return jsonify({"status": "item_type_is_equipped", "message": "Слот уже занят!"})
            # Обработка значений если предмет не был экипирован и слот свободный
            else:
                player.charisma_bonus += item_stats.charismabonus 
                player.xp_bonus += item_stats.xpbonus - 1
                item.is_equipped = True
                item.save()
        player.save()

        # Возвращаем ВСЕ статы, чтобы JS обновил полоски
        return send_player_data(player, "success", extra_data={"is_equipped":item.is_equipped})
    

# Отрисовка инвентаря игрока 
@app.route('/get_inventory')
def get_inventory():
    if not session.get("login"):
        return redirect("/")
    player = Player.get_or_none(login=session.get("login"))
    inv = Inventory.select(Inventory, Items).join(Items).where(Inventory.player_id == player.id)
    
    items_list = []
    for row in inv:
        items_list.append({
            "id": row.id,
            "name": row.item_id.name,
            "quantity": row.quantity,
            "description": row.item_id.description,
            "hp_bonus": row.item_id.influence_on_hp,
            "is_equipped":row.is_equipped
        })
    return jsonify(items_list)

# Функция выбора решения 
@app.route("/choice", methods=["POST"])
def choice():
    # Получение данных
    player = Player.get_or_none(login=session.get("login"))
    data = request.get_json()
    situation_id = data.get("situation_id")
    choice_num = data.get("choice_num")

    result = Situation_results.get_or_none(situation_id=situation_id, choice_num=choice_num)
    text = result.result_text

    player.hp = max(0, player.hp+result.hp_change)
    player.xp += result.xp_change
    player.charisma += result.charisma_change
    player.glory += result.glory_change
    player.money = max(0, player.money+result.money_change)
    player.energy = max(0, player.energy+result.energy_change)
    
    if result.target_npc:
        new_rel, created= Relations.get_or_create(player_id=player.id, npc_id=result.target_npc)
        new_rel.relations += result.relations_change
        new_rel.save()
    player.save()

    return send_player_data(player, "success", extra_data={"result":text})


#Обработка кликера
@app.route('/click', methods=['POST'])
def click():
    # Получение данных игрока и кулдаунов
    player = Player.get_or_none(login=session.get("login"))

    # Кулдауны
    Cooldowns.update(available_at=Cooldowns.available_at - 10).where((Cooldowns.player_id == player.id)&(Cooldowns.available_at >= 10)).execute()
    print("КЛИК")

    # Если нет воды или еды -10 энергии
    if player.satiety <= 0 or player.hydration <= 0:
        player.energy = max(0,player.energy -10)
        # Если нет энергии трата 10 хп
    if player.energy <= 0:
        player.hp = max(0,player.hp -10)

    # Убийство игрока сразу или предоставление второго шанса за 50$
    if player.hp <= 0 and player.money >= 50:
        player.hp = 30           
        player.energy = 50       
        player.satiety = 50
        player.hydration = 50
        player.money -= 50       
        player.time += 360  

    if player.hp <= 0:
        Player.delete().where(Player.id==player.id).execute()
        session.clear()
        session["death"] = True
        return jsonify({"status":"death"})
    
    
    # Трата голода и воды 
    player.satiety = max(0,player.satiety -1)
    player.hydration = max(0,player.hydration -2)

    
    if not player.job: 
        player.time += 10
        player.energy = max(0,player.energy -1 )
        player.xp += round(player.location.base_xp * player.xp_bonus)
        event = random_event(player)
        if event:
            player.save() 
            return event

    elif player.job:
        job = player.job
        player.money = round(job.salary + player.money, 2)
        player.xp += int(1 * player.xp_bonus)
        player.energy = max(0, player.energy - job.energy_cost)
        player.time += job.time_cost

        event = random_event(player)
        if event:
            player.save() 
            return event


    if player.time >= 1440:
        player.time = player.time - 1440
        player.days += 1
    player.save()   

    return send_player_data(player, "success")

"""ЧИТЫ"""
# Функции-читы
def cheat_money(player):
    player.money += request.args.get("money", default=0, type=float)
    player.save()
def cheat_xp(player):
    player.xp += request.args.get("xp", default=0, type=int)
    player.save()
def cheat_stats(player):
    player.hp, player.energy,player.satiety,player.hydration = player.max_hp, player.max_energy,player.max_satiety,player.max_hydration
    player.save()
def cheat_cooldowns(player):
    Cooldowns.update(available_at = 0).where(Cooldowns.player_id==player.id).execute()

# Словарь на читы

cheat_map = {
    "add_money": cheat_money,
    "add_xp": cheat_xp,
    "reset_cooldowns": cheat_cooldowns,
    "full_stats" : cheat_stats
}
# Описание маршрутов
@app.route("/admin")
def admin():
    player = Player.get_or_none(login = session.get("login"))
    if not player:
        return redirect("/")
    cooldowns = player.cooldowns



    return render_template("admin.html", player=player, cooldowns=cooldowns)

@app.route("/admin/cheats", methods=["GET"])
def admin_cheats():
    player = Player.get_or_none(login = session.get("login"))
    if not player:
        return redirect("/")
    
    action = request.args.get("action")
    cheat_func = cheat_map.get(action)
    if cheat_func:
        cheat_func(player)
    return redirect("/admin")
    




"""ОСНОВНЫЕ МАРШРУТЫ И ЛОКАЦИИ"""
# Тестовая ветка хедер-мейн
@app.route("/main")
def main():
    player = Player.get_or_none(Player.login == session.get("login"))

    hours = player.time // 60
    minutes = player.time % 60

    return render_template("main.html", player=player, hours=hours, minutes=minutes)


# Страница смерти игрока
@app.route("/death")
def death():
    if session.get("death") != True :
        return redirect("/trailer")
    return render_template("death.html")


#Главная страница (Карта)
@app.route("/map")
def map():
    return render_template("map.html")

@app.route("/store")
def store():
    store_items = Items.select()
    return render_template("store.html",store_items=store_items)

#Трейлер 
@app.route("/trailer")
def trailer():
    if session.get("is_auth") != True:
        return redirect("/")
    
    player = Player.get_or_none(login=session["login"])
    player.location=1
    player.job = None
    player.save()

    hours = player.time // 60
    minutes = player.time % 60
    return render_template("trailer.html", player=player, hours=hours, minutes=minutes)

@app.route("/tunnel")
def tunnel():
    if session.get("is_auth") != True:
        return redirect("/")
    
    
    player = Player.get_or_none(login=session["login"])
    player.location=2
    player.job = None
    player.save()

    hours = player.time // 60
    minutes = player.time % 60
    return render_template("tunnel.html", player=player, hours=hours, minutes=minutes)
    
@app.route("/park")
def park():
    if session.get("is_auth") != True:
        return redirect("/")
    
    player = Player.get_or_none(login=session["login"])
    player.location=3
    player.job = None
    player.save()

    hours = player.time // 60
    minutes = player.time % 60
    return render_template("park.html", player=player, hours=hours, minutes=minutes)
    



#Подработки
@app.route("/bottles")
def bottles():
    if session.get("is_auth") != True:
        return redirect("/")
    
    
    player = Player.get_or_none(login=session["login"])
    player.job = 1
    player.location = 1
    player.save()

    hours = player.time // 60
    minutes = player.time % 60
    return render_template("job1.html", player=player, hours=hours, minutes=minutes)

@app.route("/play_popular")
def play_popular():
    if session.get("is_auth") != True:
        return redirect("/")
    
    player = Player.get_or_none(login=session["login"])
    player.job = 2
    player.location = 2
    player.save()

    hours = player.time // 60
    minutes = player.time % 60
    return render_template("job2.html", player=player, hours=hours, minutes=minutes)

@app.route("/small_concert")
def small_concert():
    if session.get("is_auth") != True:
        return redirect("/")
    
    player = Player.get_or_none(login=session["login"])
    player.job = 3
    player.location = 3
    player.save()

    hours = player.time // 60
    minutes = player.time % 60
    return render_template("job3.html", player=player, hours=hours, minutes=minutes)






#Регистрация
@app.route('/', methods=["GET","POST"])
def register():
    if request.method == "POST":
        session.clear()
        login = request.form["login"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        name = request.form["name"]
        age = request.form["age"]
        location = "trailer"
        if not all([login,password1,password2,name,age]):
            return "Пропущены поля"
        if password1 == password2:
            if Player.get_or_none(login=login):
                return "Логин занят"
            else:
                new_player = Player.create(login = login, password = password1, name=name, age=age, location=1, xp_bonus=1.0, money=100, time=360)
                starter_items = Items.select().where(Items.price == 0)

                for item in starter_items:
                    Inventory.create(
                        player_id=new_player, 
                        item_id=item, 
                        quantity=1, 
                        is_equipped=True
                    )
                Relations.create(player_id=new_player, npc_id=1, relations=-30)
                Relations.create(player_id=new_player, npc_id=2, relations=25)
                
                session["is_auth"] = True
                session["login"] = login
                session["location"] = 1

                return redirect("/trailer")
        else:
            return "Ошибка"
    
    return render_template('register.html')

#Авторизация
@app.route('/auth', methods=["GET","POST"])
def auth():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password1"]
        
        
        if not all([login,password]):
            return "Пропущены поля"
        
        if Player.get_or_none(login=login,password=password):
            session["is_auth"] = True
            session["login"] = login
            session["location"] = 1
            return redirect("/trailer")
        
        else:
            return "Ошибка"
    
    return render_template('auth.html')

#Выход из профиля
@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

app.run(debug=True)
