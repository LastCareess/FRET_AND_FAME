import random
from models import *
from flask import Flask,render_template,redirect,request,session,jsonify

app = Flask("myapp")
app.secret_key = 'Poawlh9aw1982;lawfi'
#==============================================================================
#МАРШРУТЫ
@app.route("/buy_item", methods=["POST"])
def buy_item():
    try_to_buy_item = request.get_json()
    item = Items.get_or_none(id=try_to_buy_item.get("item_id"))
    player = Player.get_or_none(login=session.get("login"))

    if item and player:
        
        if player.money >= item.price:
            player.money -= item.price
            player.save()


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


    

@app.route("/shop", methods=["POST"])
def shop():
    data = request.get_json()   
    

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
    sorted_items = []
    for item in items:
        sorted_items.append({"id":item.id,"name":item.name,"price":item.price,"description":item.description,"item_type":item.item_type})
    return jsonify(sorted_items)

@app.route("/use_item", methods=["POST"])
def use_item():
    player = Player.get_or_none(login=session.get("login"))
    data = request.get_json()
    item = Inventory.get_or_none(id=data.get("inv_id"), player_id=player.id)

    if not item or item.quantity <= 0:
        return jsonify({"status": "error", "message": "Предмет не найден"})
    

    else:
        item_stats = item.item_id

        # Логика по типам
        if item_stats.item_type in ["food", "drink", "meds"]:
            # Удаление/уменьшение количества
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete_instance()

            print(f"Используем предмет: {item_stats.name}, Тип: {item_stats.item_type}, Восстанавливает жажды: {item_stats.restore_hydration}")
            player.satiety = min(player.max_satiety, player.satiety + item_stats.restore_satiety)
            player.hydration = min(player.max_hydration, player.hydration + item_stats.restore_hydration)
            player.hp = min(player.max_hp, player.hp + item_stats.influence_on_hp)
            player.energy = min(player.max_energy, player.energy + item_stats.energy_change)

        elif item_stats.item_type in ["guitar", "eqp", "jacket", "t-shirt", "pants", "boots"]:
            if item.is_equipped:
                player.charisma_bonus -= item_stats.charismabonus 
                player.xp_bonus -= item_stats.xpbonus - 1
                item.is_equipped = False
                item.save()
                return jsonify({
                    "status": "unequipped",
                    "hp": player.hp,
                    "energy": player.energy,
                    "food": player.satiety,
                    "water": player.hydration,
                    "money": player.money,
                    "xp": player.xp,
                    "time": player.time
                })
                
            already_equipped = (Inventory.select().join(Items).where(Inventory.player_id == player.id, Inventory.is_equipped == True, Items.item_type == item_stats.item_type).first())
            if already_equipped:
                return jsonify({"status": "item_type_is_equipped", "message": "Слот уже занят!"})
            
            else:
                player.charisma_bonus += item_stats.charismabonus 
                player.xp_bonus += item_stats.xpbonus - 1
                item.is_equipped = True
                item.save()
        player.save()

    # Возвращаем ВСЕ статы, чтобы JS обновил полоски
    return jsonify({
        "status": "success",
        "hp": player.hp,
        "energy": player.energy,
        "food": player.satiety,
        "water": player.hydration,
        "money": player.money,
        "xp": player.xp,
        "time": player.time,
        "is_equipped":item.is_equipped
    })


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

@app.route("/choice", methods=["POST"])
def choice():
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

    return jsonify({"status":"success",
                    "result":text,
                    "hp":player.hp,
                    "energy":player.energy,
                    "food":player.satiety,
                    "water":player.hydration,
                    "time":player.time,
                    "xp":player.xp,
                    "money":player.money,
                    })


#Обработка кликера
@app.route('/click', methods=['POST'])
def click():
    
    player = Player.get_or_none(login=session.get("login"))
    Cooldowns.update(available_at=Cooldowns.available_at - 10).where((Cooldowns.player_id == player.id)&(Cooldowns.available_at >= 10)).execute()

    print("КЛИК")
    if player.hp <= 0 and player.money >= 50:
        player.hp = 30           
        player.energy = 50       
        player.satiety = 50
        player.hydration = 50
        player.money -= 50       
        player.time += 360  

    if player.hp <= 0:
        Player.delete().where(id=player.id).execute()
        session.clear()
        
        return jsonify({
            "status":"death"
        })
    
    if player.hp > 0:
        player.satiety = max(0,player.satiety -2)
        player.hydration = max(0,player.hydration -3)
        if player.satiety <= 0 or player.hydration <= 0:
            player.energy = max(0,player.energy -10)
        if player.energy <= 0:
            player.hp = max(0,player.hp -10)
        
        if not player.job: 
            player.time += 10
            player.energy = max(0,player.energy -1 )
            if player.location_id == 1:
                player.xp += int(10 * player.xp_bonus)
            if player.location_id == 2:
                player.xp += int(15 * player.xp_bonus)
            if player.location_id == 3:
                player.xp += int(20 * player.xp_bonus)
        

            for situation in Random_situation.select().where(Random_situation.location_id==player.location_id):
                cooldown = Cooldowns.get_or_none(player_id=player.id, situation_id=situation.id)
                random_num = random.randint(0,100)
                if random_num <= situation.chance:
                    if cooldown and cooldown.available_at <= 0:
                        results = Situation_results.get_or_none(situation_id = situation.id)
                        Cooldowns.update(available_at = random.randrange(1440, 2881, 10), situation_id=situation.id,player_id=player.id).where(player_id=player.id,situation_id=situation.id).execute()
                        player.save()
                        return jsonify({
                            "status":"active",
                            "situation_id":situation.id,
                            "name":situation.name,
                            "description":situation.description,
                            "choice":[situation.choice_name1,situation.choice_name2,situation.choice_name3,]
                        })
                    elif not cooldown:
                        results = Situation_results.get_or_none(situation_id = situation.id)
                        Cooldowns.create(available_at=random.randrange(1440, 2881, 10), situation_id=situation.id,player_id=player.id)
                        player.save()
                        return jsonify({
                            "status":"active",
                            "situation_id":situation.id,
                            "name":situation.name,
                            "description":situation.description,
                            "choice":[situation.choice_name1,situation.choice_name2,situation.choice_name3,]
                        })
        elif player.job:
            job = player.job
            player.money += job.salary
            player.xp += int(1 * player.xp_bonus)
            player.energy = max(0, player.energy - job.energy_cost)
            player.time += job.time_cost

    if player.time >= 1440:
        player.time = player.time - 1440
        player.days += 1
    player.save()   
    return jsonify({ 
        "hp":player.hp,
        "energy":player.energy,
        "food":player.satiety,
        "water":player.hydration,
        "time":player.time,
        "xp":player.xp,
        "money":player.money
    })
    

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
