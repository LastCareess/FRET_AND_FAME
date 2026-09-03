from models import *


def fill_db():
    items_data = [
        # --- НАПИТКИ ---
        {'name': 'Кофе', 'item_type': 'drink', 'price': 10, 'restore_hydration': 10, 'energy_change': 30, 
         'description': 'Горькая жижа из автомата. Единственное, что держит тебя на ногах после ночной репетиции.'},
        {'name': 'Энергетик', 'item_type': 'drink', 'price': 5, 'restore_hydration': 10, 'energy_change': 15, 
         'description': 'Дешевый шипучий напиток. Сердце стучит быстрее, но руки почему-то трясутся.'},
        {'name': 'Пиво', 'item_type': 'drink', 'price': 1, 'restore_hydration': 15, 'energy_change': 20, 'influence_on_hp': -5, 
         'description': 'Теплая банка сомнительного пойла. Ты чувствуешь себя рок-звездой, но печень не согласна.'},
        {'name': 'Вода', 'item_type': 'drink', 'price': 1, 'restore_hydration': 30, 
         'description': 'Обычная вода из-под крана в пластиковой бутылке. Жизненно необходима для связок.'},

        # --- ЕДА ---
        {'name': 'Дешевый обед', 'item_type': 'food', 'price': 3, 'restore_satiety': 10, "energy_change":1,
         'description': 'Подгоревший хот-дог с заправки. Желудок ворчит, но выбора нет.'},
        {'name': 'Средний обед', 'item_type': 'food', 'price': 10, 'restore_satiety': 40,  "energy_change":5,
         'description': 'Бизнес-ланч в местной забегаловке. Почти как настоящая домашняя еда.'},
        {'name': 'Большой обед', 'item_type': 'food', 'price': 20, 'restore_satiety': 100, "energy_change":10,
         'description': 'Настоящий пир из стейка и картошки. Ты готов свернуть горы (или хотя бы перетащить усилитель).'},

        # --- ЛЕКАРСТВА ---
        {'name': 'Курс таблеток', 'item_type': 'meds', 'price': 100, 'influence_on_hp': 50, 
         'description': 'Сильные антибиотики. Помогают выжить после самого жесткого слэма.'},
        {'name': 'Бинт', 'item_type': 'meds', 'price': 60, 'influence_on_hp': 30, 
         'description': 'Стерильный бинт. Полезен, когда струна рвется прямо во время соло и режет пальцы.'},
        {'name': 'Пластырь', 'item_type': 'meds', 'price': 20, 'influence_on_hp': 5, 
         'description': 'Маленький пластырь с забавным рисунком. Чисто символическая помощь.'},
        {"name":"Непонятная таблетка", 'item_type':'meds', 'price':10, 'influence_on_hp':10, 'restore_hydration':-10,
         'description': 'Таблетка из переулка, кто знает что она делает'},
        {"name":"Сигаретка", 'item_type':'meds', 'price':5, 'influence_on_hp':-10, 'restore_hydration':-10, 'energy_change':30,
         'description': 'Сигаретка'},

        # --- ГИТАРЫ ---
        {'name': 'Старый страт', 'item_type': 'guitar', 'price': 0, 'charismabonus': 0, 'xpbonus': 1.0, 
         'description': 'Поцарапанная гитара из комиссионки. Фонит, не держит строй, но это твоё первое оружие.'},
        {'name': 'Дешевый суперстрат', 'item_type': 'guitar', 'price': 100, 'charismabonus': 2, 'xpbonus': 1.4, 
         'description': 'Выглядит агрессивно, звучит плоско. Но для первых риффов пойдет.'},
        {'name': 'Дешевая стрела', 'item_type': 'guitar', 'price': 200, 'charismabonus': 5, 'xpbonus': 1.3, 
         'description': 'Острые углы и дешевый лак. Все сразу видят — ты пришел играть метал.'},
        {'name': 'Эксплорер', 'item_type': 'guitar', 'price': 350, 'charismabonus': 7, 'xpbonus': 1.5, 
         'description': 'Классическая форма для тяжелого рока. Увесистая штука с хорошим сустейном.'},
        {'name': 'Стрела', 'item_type': 'guitar', 'price': 400, 'charismabonus': 9, 'xpbonus': 1.6, 
         'description': 'Инструмент для тех, кто хочет выделяться на сцене. Только не сиди с ней.'},
        {'name': 'The dean from hell', 'item_type': 'guitar', 'price': 1000, 'charismabonus': 15, 'xpbonus': 2.0, 
         'description': 'Молнии на корпусе и яростный звук. Соседи вызовут полицию через пять минут после включения.'},
        {'name': 'Авангардная гитара', 'item_type': 'guitar', 'price': 5000, 'charismabonus': 30, 'xpbonus': 3.0, 
         'description': 'Шедевр гитарного искусства. Звучит так, будто ангелы поют хором в аду.'},

        # --- ОБОРУДОВАНИЕ ---
        {'name': 'Крутые медиаторы', 'item_type': 'eqp', 'price': 40, 'xpbonus': 1.2, 
         'description': 'Они не теряются в карманах. По крайней мере, первые пять минут.'},
        {'name': 'Дешевый комбик', 'item_type': 'eqp', 'price': 90, 'charismabonus': 2, 
         'description': '10 ватт чистого разочарования. Но громче, чем акустика.'},
        {'name': 'Средний комбик', 'item_type': 'eqp', 'price': 190, 'charismabonus': 4, 
         'description': 'Уже можно репетировать с барабанщиком, если он не слишком злой.'},
        {'name': 'Дорогой комбик', 'item_type': 'eqp', 'price': 500, 'charismabonus': 10, 
         'description': 'Ламповый звук, который заставляет стены дрожать.'},
        {'name': 'Дорогие струны', 'item_type': 'eqp', 'price': 100, 'xpbonus': 1.3, 
         'description': 'Блестящие, звонкие и не режут пальцы. Одно удовольствие.'},
        {'name': 'Педаль Overdrive', 'item_type': 'eqp', 'price': 100, 'charismabonus': 2, 
         'description': 'Добавляет классического "песочка" в твой звук.'},
        {'name': 'Педаль Distortion', 'item_type': 'eqp', 'price': 150, 'charismabonus': 3, 
         'description': 'Плотный перегруз. Идеально для хэви-метала.'},
        {'name': 'Педаль Reverb', 'item_type': 'eqp', 'price': 100, 'charismabonus': 2, 
         'description': 'Теперь твое соло звучит так, будто ты на стадионе, а не в трейлере.'},
        {'name': 'Педаль Wah-Wah', 'item_type': 'eqp', 'price': 750, 'charismabonus': 10, 
         'description': 'Квакушка. Заставляет гитару разговаривать.'},

        # --- ОДЕЖДА ---
        {'name': 'Старая джинсовка', 'item_type': 'jacket', 'price': 0, 'charismabonus': 0, 
         'description': 'Протертая на локтях куртка. Пахнет пылью и гаражом.'},
        {'name': 'Старые джинсы', 'item_type': 'pants', 'price': 0, 'charismabonus': 0, 
         'description': 'Джинсы, которые видели лучшие времена.'},
        {'name': 'Заляпанная футболка', 'item_type': 't-shirt', 'price': 0, 'charismabonus': 0, 
         'description': 'Пятна от кетчупа или кофе? Уже никто не помнит.'},
        {'name': 'Старые кроссовки', 'item_type': 'boots', 'price': 0, 'charismabonus': 0, 
         'description': 'Подошва держится на честном слове и скотче.'},
        {'name': 'Рваная кожанка', 'item_type': 'jacket', 'price': 200, 'charismabonus': 3, 
         'description': 'Настоящая кожа, хоть и местами облезлая. Добавляет брутальности.'},
        {'name': 'Рваные джинсы', 'item_type': 'pants', 'price': 75, 'charismabonus': 2, 
         'description': 'Дырки на коленях сделаны специально. Ну, ты так всем говоришь.'},
        {'name': 'Мерч футболка', 'item_type': 't-shirt', 'price': 50, 'charismabonus': 1, 
         'description': 'Футболка известной группы. Показывает, что у тебя есть вкус.'},
        {'name': 'Конверсы', 'item_type': 'boots', 'price': 150, 'charismabonus': 3, 
         'description': 'Классические кеды. В них ноги почти не устают на сцене.'},
        {'name': 'Дорогая кожанка', 'item_type': 'jacket', 'price': 1000, 'charismabonus': 10, 
         'description': 'Тяжелая, качественная кожа. Ты выглядишь как бог рок-н-ролла.'},
        {'name': 'Кожанные штаны', 'item_type': 'pants', 'price': 750, 'charismabonus': 8, 
         'description': 'Жарко? Да. Неудобно? Да. Но выглядит чертовски круто.'},
        {'name': 'Берцы', 'item_type': 'boots', 'price': 400, 'charismabonus': 5, 
         'description': 'Массивные ботинки. Идеально для того, чтобы прыгать со сцены в толпу.'},
        {'name': 'Футболка своей группы', 'item_type': 't-shirt', 'price': 200, 'charismabonus': 3, 
         'description': 'Собственный мерч. Первый шаг к мировой славе.'},
    ]

    for data in items_data:
        Items.get_or_create(name=data['name'], defaults=data)
    print("БАЗА ЗАПОЛНЕНА ПРЕДМЕТАМИ!")
    #===================ЛОКАЦИИ=======================
    #===================ЛОКАЦИИ=======================
    #===================ЛОКАЦИИ=======================
    #===================ЛОКАЦИИ=======================
    #===================ЛОКАЦИИ=======================

    locations_data = [
        {"name":"Трейлер","access":True,"needxp":0,"needcharisma":0,"open_from":0,"open_to":1440, "base_xp":10},
        {"name":"Переход","access":False,"needxp":1500,"needcharisma":20,"open_from":0,"open_to":1440, "base_xp":15},
        {"name":"Парк","access":False,"needxp":3000,"needcharisma":40,"open_from":600,"open_to":1320, "base_xp":20}
    ]
    for data in locations_data:
        Locations.get_or_create(name=data['name'], defaults=data)
    print("ЛОКАЦИИ ЗАПОЛНЕНЫ!")

    #===========НПС=================
    #===========НПС=================
    #===========НПС=================
    #===========НПС=================
    #===========НПС=================

    npc_data = [
        {"name":"Саманта",
         "age":27,
         "xpbonus":1,
         "charismabonus":1,
         "relations":-30,
         "location":1
        },

        {"name":"Джейк",
         "age":23,
         "xpbonus":1.5,
         "charismabonus":1,
         "relations":25,
         "location":1
        },

        {"name":"Джон Дикон",
         "age":44,
         "xpbonus":2,
         "charismabonus":5,
         "relations":0,
         "location":2
        },

        {"name":"Иззи Стредлин",
         "age":54,
         "xpbonus":3.3,
         "charismabonus":5,
         "relations":0,
         "location":3
        }
    ]

    for data in npc_data:
        Npc.get_or_create(name=data['name'], defaults=data)
    print("База ожила благодаря НПС!")

    #====================РАБОТА==============================
    #====================РАБОТА==============================
    #====================РАБОТА==============================
    #====================РАБОТА==============================
    #====================РАБОТА==============================

    jobs_data = [
        {"name":"Собирать бутылки",
         "salary":0.7,
         "need_xp":0,
         "need_charisma":0,
         "energy_cost":2,
         "time_cost":10,
         "open_from":0,
         "open_to":1440,
         "access":True
        },
        {"name":"Играть попсу",
         "salary":3,
         "need_xp":1500,
         "need_charisma":20,
         "energy_cost":5,
         "time_cost":30,
         "open_from":480,
         "open_to":1320,
         "access":False
        },
        {"name":"Выступить в местной забегаловке",
         "salary":20,
         "need_xp":3000,
         "need_charisma":40,
         "energy_cost":15,
         "time_cost":60,
         "open_from":480,
         "open_to":1320,
         "access":False
        }
    ]
    for data in jobs_data:
        Jobs.get_or_create(name=data['name'], defaults=data)
    print("Можно работать!")
    #====================СИТУАЦИИ============================
    #====================СИТУАЦИИ============================
    #====================СИТУАЦИИ============================
    #====================СИТУАЦИИ============================
    #====================СИТУАЦИИ============================

    random_situations = [
    #===========================БЛОК ПЕРВОЙ ЛОКАЦИИ============================================
        {"name":"Приходит ваша бывшая, которая требует с вас алименты на ребенка!",
         "description":"Пришла ваша бывшая девушка, с которой у вас был ребенок. Она требует чтобы ты уже наконец заплатил ей 100$!!!",
         "chance":10,
         "location_id":1,
         "choice_name1":"Ударить",
         "choice_name2":"Заплатить",
         "choice_name3":"Сказать что денег нет и ты все еще любишь ее",
         "is_available":True},

        {"name":"Приходит ваш друг и предлагает вам выпить пива как обычно",
         "description":"Хэй чувак! Я холодненького принес как обычно)",
         "chance":10,
         "location_id":1,
         "choice_name1":"Отказать",
         "choice_name2":"Согласиться",
         "choice_name3":"Позвать в группу",
         "is_available":True},
        
        {"name":"Ваша крыша протекает",
         "description":"Крыша вашего трейлера протекает! Нужно срочно решать что делать!",
         "chance": 2,
         "location_id":1,
         "choice_name1":"Игнорировать",
         "choice_name2":"Починить самому",
         "choice_name3":"Вызвать мастера",
         "is_available":True},

        {"name":"Вам пришло письмо из профсоюза!",
         "description":"Это пособие по безработице!!! Скорее откройте его",
         "chance": 4,
         "location_id":1,
         "choice_name1":"Скорее принять!!!",
         "is_available":True},
    #===========================БЛОК ПЕРВОЙ ЛОКАЦИИ============================================
                                    #ПЕРЕХОД
    #===========================БЛОК ВТОРОЙ ЛОКАЦИИ============================================
        {"name":"Вам предложили Запрещенные вещества",
         "description":"Мутный тип предложил вам закурить вместе с ним, как поступите?",
         "chance":20,
         "location_id":2,
         "choice_name1":"Согласиться",
         "choice_name2":"Отказаться",
         "choice_name3":"Напасть",
         "is_available":True},

        {"name":"Вы встретили своего кумира",
         "description":"Ваш кумир проходит буквально в двух шагах от вас, как поступите?",
         "chance":5,
         "location_id":2,
         "choice_name1":"Познакомиться",
         "choice_name2":"Не обращать внимания",
         "choice_name3":"Сыграть его песню",
         "is_available":True},

        {"name":"Разгильдяи",
         "description":"Местные хулиганы решили что вы легкая мишень и требуют денег, как поступите?",
         "chance":10,
         "location_id":2,
         "choice_name1":"Драться",
         "choice_name2":"Заплатить",
         "choice_name3":"Позвать на помощь",
         "is_available":True},
    #===========================БЛОК ВТОРОЙ ЛОКАЦИИ============================================
                                    #ПЕРЕХОД
    #===========================БЛОК ТРЕТЬЕЙ ЛОКАЦИИ============================================
        {"name":"Хот-дог",
         "description":"Ребенок просит вас добавить ему на хот-дог.",
         "chance":20,
         "location_id":3,
         "choice_name1":"Добавить",
         "choice_name2":"Послать",
         "choice_name3":"Дать ему самому на сцене заработать на хот-дог",
         "is_available":True},

        {"name":"Вас хотят арестовать за громкий звук",
         "description":"Органы местной власти вышли на вас по наводке от местных жителей и просят вас пройти с ними в участок",
         "chance":10,
         "location_id":2,
         "choice_name1":"Дать взятку",
         "choice_name2":"Сдаться",
         "choice_name3":"Убежать",
         "is_available":True},

        {"name":"Бомж попросил вас сыграть его любимую песню",
         "description":"Бомж просит у вас разрешения взять вашу гитару и сыграть песню так, как он делал в молодости",
         "chance":10,
         "location_id":2,
         "choice_name1":"Дать гитару",
         "choice_name2":"Прогнать",
         "choice_name3":"Сыграть самому его песню",
         "is_available":True}
    ]
    for data in random_situations:
        Random_situation.get_or_create(name=data['name'], defaults=data)
    print("База заполнена ситуациями!")

    #РЕЗУЛЬТАТЫ======================================================РЕЗУЛЬТАТЫ======================================================
    #РЕЗУЛЬТАТЫ======================================================РЕЗУЛЬТАТЫ======================================================
    #РЕЗУЛЬТАТЫ======================================================РЕЗУЛЬТАТЫ======================================================
    #РЕЗУЛЬТАТЫ======================================================РЕЗУЛЬТАТЫ======================================================
    #РЕЗУЛЬТАТЫ======================================================РЕЗУЛЬТАТЫ======================================================

    situation_results_data = [
    #===========================БЛОК ПЕРВОЙ ЛОКАЦИИ============================================
        #Женщина
        {"hp_change":-50,
         "money_change":-50,
         "charisma_change":3,
         "choice_num":1,
         "result_text":"Оказалась сильнее и вы потеряли половину здоровья, 50$ потерянo Харизма +3",
         "situation_id":1,
         "target_npc":1,
         "relations_change":-30},
        {"money_change":-30,
         "choice_num":2,
         "result_text":"Вы заплатили 30$, Она улыбнулась вам)",
         "situation_id":1,
         "target_npc":1,
         "relations_change":+10},
        {"hp_change":-15,
         "charisma_change":-2,
         "choice_num":3,
         "result_text":"Она дала вам пощечину и ушла.",
         "situation_id":1,
         "target_npc":1},
        #Друг и пиво
        {"choice_num":1,
         "result_text":"Ваш друг разочарован, отношения ухудшены",
         "situation_id":2,
         "target_npc":2,
         "relations_change":-10},
        
        {"hp_change":-15,
         "charisma_change":-2,
         "glory_change":-1,
         "choice_num":2,
         "result_text":"Вы выпили пива, и попытались перелезть к соседям. Половина вашей задницы не покинула их участок. Получен респект от друга",
         "situation_id":2,
         "target_npc":2,
         "relations_change":20},
        
        {"charisma_change":2,
         "choice_num":3,
         "result_text":"Ваш друг подумает",
         "situation_id":2,
         "target_npc":2,
         "relations_change":5},
        #Крыша
        {"money_change":-100,
         "hp_change":-90,
         "choice_num":1,
         "result_text":"Ваш трейлер обрушился, потребовался капитальный ремонт",
         "situation_id":3},
         
        {"money_change":-20,
         "hp_change":-10,
         "choice_num":2,
         "result_text":"Вы пошли в магазин и купили материалы, крыша починена, но ваш палец пострадал от встречи с молотком",
         "situation_id":3},

        {"money_change":-40,
         "choice_num":3,
         "result_text":"Вы вызвали мастера и он починил вам крышу",
         "situation_id":3},
        #Пособие
        {"money_change":100,
         "choice_num":1,
         "result_text":"Вы приняли его",
         "situation_id":4},
    #===========================БЛОК ПЕРВОЙ ЛОКАЦИИ============================================
                                    #ПЕРЕХОД
    #===========================БЛОК ВТОРОЙ ЛОКАЦИИ============================================
        #Барыга
        {"hp_change":-99,
         "money_change":-100,
         "charisma_change":-3,
         "choice_num":1,
         "result_text":"Вас сильно избили и забрали 100$",
         "situation_id":5
        },
        {"charisma_change":3,
         "choice_num":2,
         "result_text":"Барыга ушел, оставив за собой множество загадок",
         "situation_id":5
        },
        {"hp_change":-70,
         "charisma_change":4,
         "choice_num":3,
         "result_text":"Вы напали на него, но к несчастью, у него был нож. Вы тоже не промах, многочисленные драки дали плоды",
         "situation_id":5
        },
        #Кумир
        {"xp_change":100,
         "charisma_change":3,
         "choice_num":1,
         "result_text":"Он оказался таким как вы его себе и представляли, он научил вас искуственным флажолетам",
         "situation_id":6,
         "target_npc":3,
         "relations_change":10
        },
        {"choice_num":2,
         "result_text":"Он прошел мимо",
         "situation_id":6
        },
        {"money_change":50,
         "charisma_change":4,
         "glory_change":2,
         "choice_num":3,
         "result_text":"Он заценил! За прекрасное исполнение он кинул вам 50$",
         "situation_id":6,
         "target_npc":3,
         "relations_change":30
        },
        #Разгильдяи

        {"hp_change":-50,
         "charisma_change":3,
         "choice_num":1,
         "result_text":"Ваш опыт в драке позволил их отметелить без особых потерь",
         "situation_id":7
        },

        {"choice_num":2,
         "money_change":-40,
         "result_text":"Вы отдали деньги",
         "situation_id":7
        },

        {"charisma_change":-5,
         "glory_change":-1,
         "choice_num":3,
         "result_text":"Вам помогли правоохранители",
         "situation_id":7
        },
    #===========================БЛОК ВТОРОЙ ЛОКАЦИИ============================================
                                    #ПЕРЕХОД
    #===========================БЛОК ТРЕТЬЕЙ ЛОКАЦИИ============================================
        #Мальчик и хот-дог

        {"charisma_change":3,
         "money_change":-5,
         "choice_num":1,
         "result_text":"Мальчик поблагодарил вас! Ваше самочувствие улучшилось",
         "situation_id":8
        },

        {"choice_num":2,
         "charisma_change":-5,
         "result_text":"Мальчик расстроился, вы почувствовали себя козлом",
         "situation_id":8
        },

        {"charisma_change":5,
         "glory_change":2,
         "choice_num":3,
         "result_text":"На этот трогательный жест собралась большая толпа. Вы стали популярнее, и почувствовали себя лучше",
         "situation_id":8
        },
        #Арест

        {"money_change":-100,
         "choice_num":1,
         "result_text":"Правоохранитель усмехнулся и с довольной ухмылкой взял ваши деньги",
         "situation_id":9
        },

        {"choice_num":2,
         "charisma_change":-5,
         "glory_change":-2,
         "hp_change":-10,
         "result_text":"Вас заломали. Харизма и слава снижены",
         "situation_id":9
        },
        
        {"hp_change":-30,
         "choice_num":3,
         "energy_change":-10,
         "result_text":"Вы зацепились за кусты, но убежали",
         "situation_id":9
        },

        #Бомж-легенда

        {"money_change":100,
         "glory_change":1,
         "choice_num":1,
         "result_text":"За 'Аренду' гитары бомж дал вам сотню. Получена слава",
         "situation_id":10,
         "target_npc":4,
         "relations_change":10
        },

        {"choice_num":2,
         "charisma_change":-5,
         "glory_change":-2,
         "result_text":"Бомж оказался забытой легендой рока, вы почувствовали себя посмешищем",
         "situation_id":10,
         "target_npc":4,
         "relations_change":-10
        },
        
        {"choice_num":3,
         "situation_id":10,
         "charisma_change":5,
         "result_text":"Бомж оказался легендой рока и заценил ваш навык, также толпа ликует. Иззи Стрэдлин приглашает",
         "money_change":20,
         "glory_change":3
        }
    ]
    for data in situation_results_data:
        Situation_results.get_or_create(
            situation_id=data['situation_id'],
            choice_num=data['choice_num'],
            defaults=data
        )
    print("База заполнена результатами!")

    

fill_db()




