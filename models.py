from peewee import SqliteDatabase, Model, CharField, IntegerField,BooleanField, FloatField
from peewee import ForeignKeyField
from flask import jsonify

db_path = 'database.db'
db = SqliteDatabase(db_path)

"""
TODO: КРИТИЧЕСКИЕ АРХИТЕКТУРНЫЕ ПРАВКИ БАЗЫ ДАННЫХ (ВЕРНУТЬСЯ ПОЗЖЕ)

1. ГЛОБАЛЬНЫЙ ДОСТУП (Jobs.access и Locations.access):
   Поля 'access' общие для всех. Если один игрок открывает работу/локацию, 
   она открывается для всего сервера. Проверять доступ нужно динамически в коде по статам.

2. МУСОР ПРИ СМЕРТИ (Нет каскадного удаления):
   on_delete="CASCADE" есть только в Inventory. При смерти Player.delete() 
   его кулдауны, группа и отношения с NPC остаются "сиротами" и забивают базу мусором.

3. ДУБЛИРОВАНИЕ СТРОК (Нет уникальных индексов):
   В Cooldowns и Relations база позволяет создавать по 10 одинаковых строк 
   на одного игрока. Нужно добавить составные индексы в class Meta: indexes = ...

4. ПУТАНИЦА С ИМЕНАМИ (Суффиксы _id):
   Поля названы item_id, player_id. Из-за этого Peewee путает типы, и в коде 
   приходится писать уродливое item.item_id.item_type. Переименовать просто в 'item', 'player'.

5. ХАРДКОД КВЕСТОВ (Ограничение на 3 выбора):
   Поля choice_name1, 2, 3 зашиты в Random_situation. Это ограничивает квесты строго 
   тремя кнопками. Правильнее привязывать варианты ответов к Situation_results.

6. СЛОТЫ ОДЕЖДЫ ( jacket и t-shirt):
   Сейчас проверка идет по точному совпадению item_type. Игрок может надеть куртку 
   и футболку одновременно. Нужно ввести общее поле 'category' = 'cloth'.
"""



class BaseModel(Model):
    class Meta:
        database = db


class Locations(BaseModel):
    name = CharField()
    access = BooleanField(default=False)
    needxp = IntegerField()
    needcharisma = IntegerField()
    open_from = IntegerField()
    open_to = IntegerField()
    base_xp = IntegerField()

class Jobs(BaseModel):
    name = CharField()
    salary = FloatField()
    need_xp = IntegerField()
    need_charisma = IntegerField()
    time_cost = IntegerField()
    energy_cost = IntegerField()
    open_from = IntegerField()
    open_to = IntegerField()
    access = BooleanField(default=False)
    
class Player(BaseModel):
    login = CharField(unique=True)
    password = CharField()
    hp = IntegerField(default=100)
    energy = IntegerField(default=100)
    max_hp = IntegerField(default=100)
    max_energy = IntegerField(default=100)
    charisma = IntegerField(default=0)
    charisma_bonus = IntegerField(default=0)
    money = FloatField(default=0)
    glory = IntegerField(default=0)
    xp = IntegerField(default=0)
    xp_bonus = FloatField(default=1)
    age = IntegerField()
    name = CharField()
    location = ForeignKeyField(Locations, backref="players")
    job = ForeignKeyField(Jobs, backref="players", null=True)
    satiety = IntegerField(default=100)
    max_satiety = IntegerField(default=100)
    hydration = IntegerField(default=100)
    max_hydration = IntegerField(default=100)
    time = IntegerField(default=0)
    days = IntegerField(default=0)

class Npc(BaseModel):
    name = CharField()
    age = IntegerField()
    xpbonus = FloatField()
    charismabonus = IntegerField()
    location = ForeignKeyField(Locations,backref="npcs")

class Band(BaseModel):
    name = CharField()
    popularity = IntegerField()
    player_id = ForeignKeyField(Player)
     
class Bandmember(BaseModel):
    band_id = ForeignKeyField(Band)
    npc_id = ForeignKeyField(Npc,backref="npcs_on_band",null=True)
    player_id = ForeignKeyField(Player,null=True)
     

     
class Random_situation(BaseModel):
    name = CharField()
    description = CharField()
    chance = IntegerField()
    location = ForeignKeyField(Locations, backref='situations')
    choice_name1 = CharField()
    choice_name2 = CharField(null=True)
    choice_name3 = CharField(null=True)
    is_available = BooleanField(default=True)

class Situation_results(BaseModel):
    relations_change = IntegerField(default=0)
    target_npc = ForeignKeyField(Npc, backref="situation_impacts",null=True)
    hp_change = IntegerField(default=0)
    xp_change = IntegerField(default=0)
    energy_change = IntegerField(default=0)
    money_change = IntegerField(default=0)
    charisma_change = IntegerField(default=0)
    glory_change = IntegerField(default=0)
    situation_id = ForeignKeyField(Random_situation, backref="results")
    choice_num = IntegerField()
    result_text = CharField()

    
     
class Cooldowns(BaseModel):
    player_id = ForeignKeyField(Player, backref="cooldowns")
    situation_id = ForeignKeyField(Random_situation)
    available_at = IntegerField()

class Relations(BaseModel):
    player_id = ForeignKeyField(Player,backref="relations")
    npc_id = ForeignKeyField(Npc)
    relations = IntegerField(default=0)      
class Items(BaseModel):
    name = CharField()
    description = CharField()
    xpbonus = FloatField(default=1)
    charismabonus = FloatField(default=0)
    price = IntegerField()
    item_type = CharField()
    restore_satiety = IntegerField(default=0)
    restore_hydration = IntegerField(default=0)
    energy_change = IntegerField(default=0)
    influence_on_hp = IntegerField(default=0)
    

class Inventory(BaseModel):
	player_id = ForeignKeyField(Player,on_delete="CASCADE",backref="inventory")
	is_equipped = BooleanField(default=False)
	quantity = IntegerField(default=1)
	item_id = ForeignKeyField(Items)




      



db.create_tables([Locations,Player,Npc,Band,Bandmember,Jobs,Random_situation,Situation_results,Cooldowns,Items,Inventory,Relations])

 







