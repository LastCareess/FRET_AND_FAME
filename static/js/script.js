// Используем addEventListener вместо onload для надежности
document.addEventListener("DOMContentLoaded", function () {
  // 1. Элементы интерфейса
  const phoneBtn = document.querySelector(".PhoneDiv");
  const modal = document.getElementById("phone-modal");
  const closeBtn = document.getElementById("close-phone");
  const click = document.getElementById("click");
  const hourElem = document.querySelector(".HourDiv");
  const minElem = document.querySelector(".MinuteDiv");

  // Экраны (меню)
  const mainMenu = document.getElementById("main-phone-menu");
  const invMenu = document.getElementById("inventory-menu");
  const shopMenu = document.getElementById("shop-menu");
  const jobMenu = document.getElementById("job-menu"); // Добавили экран работы

  // Кнопки открытия
  const openInvBtn = document.getElementById("open-inventory");
  const openShopBtn = document.getElementById("open-shop");
  const openJobBtn = document.getElementById("open-job"); // Добавили кнопку работы
  

  // Кнопки возврата
  const backInvBtn = document.getElementById("back-to-menu");
  const backShopBtn = document.getElementById("back-from-shop");
  const backJobBtn = document.getElementById("back-from-job"); // Добавили кнопку назад

  // 2. Инициализация (запуск функций ПРИ ЗАГРУЗКЕ)
  const startHP = parseInt(document.querySelector(".hp span").innerText);
  const startEn = parseInt(document.querySelector(".energy span").innerText);
  const startWt = parseInt(document.querySelector(".hydration span").innerText);
  const startFd = parseInt(document.querySelector(".satiety span").innerText);
  
  updateStat("hp-fill", startHP, 100);
  updateStat("energy-fill", startEn, 100);
  updateStat("water-fill", startWt, 100);
  updateStat("food-fill", startFd, 100);
  updateXP();
  checkUnlocks();


    window.loadInventory = async function() { 
    const container = document.getElementById("items-container");
    if (!container) return; // Страховка, если элемента нет на странице

    container.innerHTML = "Загрузка..."; // Показываем текст, пока ждем ответ

    try {
      const response = await fetch('/get_inventory');
      const items = await response.json();

      container.innerHTML = ""; // Очищаем текст загрузки

      if (items.length === 0) {
        container.innerHTML = "<p style='text-align:center; padding:10px;'>В инвентаре пусто</p>";
        return;
      }

      items.forEach(item => {
          const itemDiv = document.createElement("div");
          itemDiv.className = "inventory-item";
          
          // 1. Проверяем статус экипировки (из JSON, который прислал Flask)
          const isEquipped = item.is_equipped; 
          const btnText = isEquipped ? "Снять" : "Использовать";
          const btnColor = isEquipped ? "#e74c3c" : "#2ecc71"; // Красный для снятия, зеленый для использования

          itemDiv.innerHTML = `
              <div class="item-info" style="border-bottom: 1px solid #444; padding: 10px; margin-bottom: 5px;">
                  <strong>${item.name}</strong> ${isEquipped ? '<span style="color:#f1c40f;">[Надето]</span>' : `(x${item.quantity})`}
                  <p style="font-size: 0.8em; color: #ccc; margin: 5px 0;">${item.description}</p>
                  <button onclick="useItem(${item.id})" class="btn-use" 
                          style="background: ${btnColor}; color: white; border: none; padding: 5px 10px; cursor: pointer; border-radius: 3px;">
                      ${btnText}
                  </button>
              </div>
          `;
          container.appendChild(itemDiv);
      });
    } catch (error) {
      console.error("Ошибка загрузки инвентаря:", error);
      container.innerHTML = "Ошибка связи с сервером";
    }
  }
// КНОПКИ ПЕРЕКЛЮЧЕНИЯ
if (openInvBtn) {
    openInvBtn.onclick = () => {
        console.log("Инвентарь открывается...");
        switchScreen(invMenu); 
        loadInventory();
    };
}
  if (openShopBtn) {
    openShopBtn.onclick = () => {
      console.log("Открываем магазин...");
      switchScreen(shopMenu);
      // Если хочешь сразу загружать товары:
      // loadShopItems(); 
    };
  }

  // Открытие работы
  if (openJobBtn) {
    openJobBtn.onclick = () => {
      console.log("Открываем работу...");
      switchScreen(jobMenu);
      // loadJobs();
    };
  }

  if (click) {
    click.onclick = async (e) => {
      e.preventDefault();
      const response = await fetch('/click', { method: 'POST' });
      
      if (response.ok) {
        const data = await response.json();

        // ПРОВЕРКА: Если сервер вернул активную ситуацию
        if (data.status === "active") {
          showEventModal(data);
        } else {
          // Если просто клик — обновляем всё как обычно
          updateUI(data);
        }
      }
    };
  }
  window.updateUI = function(data) {
    console.log("Обновление интерфейса данными:", data);
  
    const hpVal = parseInt(document.querySelector(".hp span").innerText);
  const enVal = parseInt(document.querySelector(".energy span").innerText);
  updateStat("hp-fill", data.hp, 100);
  updateStat("energy-fill", data.energy, 100);
  updateStat("water-fill", data.water, 100); // Добавь это
  updateStat("food-fill", data.food, 100);  // Добавь это

    if (hourElem && minElem) {
      let hours = Math.floor(data.time / 60);
      let minutes = data.time % 60;
      hourElem.innerText = String(hours).padStart(2, '0');
      minElem.innerText = String(minutes).padStart(2, '0');
    }

    document.querySelector(".hp span").innerText = `${data.hp}HP/100HP`;
    document.querySelector(".energy span").innerText = `${data.energy}/100 ENERGY`;
    document.querySelector(".hydration span").innerText = `${data.water}/100 WATER`;
    document.querySelector(".satiety span").innerText = `${data.food}/100 FOOD`;
    document.querySelector(".wallet-img").innerText = `💰 $${data.money}`;
    
    const xpElem = document.getElementById("current-xp");
    if (xpElem) xpElem.innerText = data.xp;
    
    updateXP();
    checkUnlocks();
  }

  // Показ окна ситуации
  function showEventModal(data) {
    const eventModal = document.getElementById("event-modal");
    document.getElementById("event-name").innerText = data.name;
    document.getElementById("event-desc").innerText = data.description;
    
    const container = document.getElementById("event-choices");
    container.innerHTML = ""; // Очистка старых кнопок

    data.choice.forEach((text, index) => {
      if (text && text.trim() !== "") {
        const btn = document.createElement("button");
        btn.className = "choice-btn"; 
        btn.innerText = text;
        // Отправляем ID ситуации и номер выбора (index + 1)
        btn.onclick = () => makeChoice(data.situation_id, index + 1);
        container.appendChild(btn);
      }
    });
    eventModal.style.display = "flex";
  }

  // Отправка выбора игрока на сервер
  async function makeChoice(sitId, choiceNum) {
  const response = await fetch('/choice', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ situation_id: sitId, choice_num: choiceNum })
  });

  if (response.ok) {
    const data = await response.json();
    
    // Обновляем статы в фоне
    updateUI(data); 

    // 1. Меняем описание события на текст результата (data.result из Python)
    document.getElementById("event-desc").innerText = data.result;
    
    // 2. Очищаем кнопки выбора
    const container = document.getElementById("event-choices");
    container.innerHTML = ""; 

    // 3. Создаем одну кнопку "Закрыть" или "Понятно"
    const closeBtn = document.createElement("button");
    closeBtn.className = "choice-btn"; 
    closeBtn.innerText = "Понятно";
    closeBtn.onclick = () => {
      document.getElementById("event-modal").style.display = "none";
    };
    container.appendChild(closeBtn);
  }
}

  // 3. Функция переключения экранов внутри телефона
  function switchScreen(toShow) {
    // Прячем все возможные меню
    [mainMenu, invMenu, shopMenu, jobMenu].forEach((m) => {
      if (m) m.style.display = "none";
    });
    // Показываем нужное
    if (toShow) toShow.style.display = "block";
  }

  // 4. События кликов
  if (phoneBtn && modal) {
    phoneBtn.onclick = () => {
      modal.style.display = "flex";
      switchScreen(mainMenu);
    };
  }

  // Переходы в подразделы
  

  // Кнопки "Назад"
  if (backInvBtn) backInvBtn.onclick = () => switchScreen(mainMenu);
  if (backShopBtn) {
  backShopBtn.onclick = () => {
    const categoriesGrid = document.getElementById("shop-categories-grid");
    const itemsContainer = document.getElementById("shop-items-container");

    // Проверяем: если сейчас на экране блок с товарами (он виден) 
    if (itemsContainer && itemsContainer.style.display === "block") {
      itemsContainer.style.display = "none";  // Скрываем витрину товаров
      itemsContainer.innerHTML = "";         // Очищаем контейнер от старых карточек
      categoriesGrid.style.display = "grid"; // Возвращаем на экран сетку категорий
    } else {
      // Если блок товаров и так скрыт (игрок видит категории) — полностью выходим в меню телефона
      switchScreen(mainMenu);
    }
  };
  }
  if (backJobBtn) backJobBtn.onclick = () => switchScreen(mainMenu);

  // Закрытие модального окна
  if (closeBtn) {
    closeBtn.onclick = () => {
      modal.style.display = "none";
    };
  }

  window.onclick = (e) => {
    if (e.target === modal) modal.style.display = "none";
  };


  window.useItem = async function(invId) {
    try {
        const response = await fetch('/use_item', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ inv_id: invId })
        });

        if (response.ok) {
            const data = await response.json();

            if (data.status === "success" || data.status === "unequipped") {
                // Обновляем полоски статов
                window.updateUI(data); 
                // Сразу перерисовываем список, чтобы сменился текст кнопок (Надето/Снять)
                window.loadInventory(); 
            } else {
                alert(data.message || "Ошибка");
            }
        }
    } catch (error) {
        console.error("Критическая ошибка:", error);
    }
  };
  window.useItem = useItem;
});

// --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---

function updateStat(id, current, max) {
  const fill = document.getElementById(id);
  if (fill) {
    let percentage = (current / max) * 100;
    fill.style.width = Math.max(0, Math.min(100, percentage)) + "%";
  }
}

function updateXP() {
  const currentElem = document.getElementById("current-xp");
  const maxElem = document.getElementById("max-xp");
  const xpFill = document.getElementById("xp-fill");
  if (currentElem && maxElem && xpFill) {
    const currentXP = parseInt(currentElem.innerText.replace(/\D/g, ""));
    const maxXP = parseInt(maxElem.innerText.replace(/\D/g, ""));
    let percentage = (currentXP / maxXP) * 100;
    xpFill.style.width = Math.min(percentage, 100) + "%";
  }
}

function checkUnlocks() {
  const currentXPNode = document.getElementById("current-xp");
  if (!currentXPNode) return;
  const currentXP = parseInt(currentXPNode.innerText.replace(/\D/g, ""));
  const tunnel = document.getElementById("loc-tunnel");
  const park = document.getElementById("loc-park");
  const job2 = document.getElementById("job2")
  const job3 = document.getElementById("job3")

  if (tunnel && currentXP >= 1500) tunnel.style.display = "flex";
  if (park && currentXP >= 3000) park.style.display = "flex";
  if (job2 && currentXP >= 1500) job2.style.display = "flex";
  if (job3 && currentXP >= 3000) job3.style.display = "flex";
}





// Функция загрузки товаров по выбранной категории
async function loadShop(categoryType) {
// Шаг 1: Находим нужные элементы в HTML-документе
const categoriesGrid = document.getElementById("shop-categories-grid");
const itemsContainer = document.getElementById("shop-items-container");

// Страховка: если элементов нет на странице, прерываем выполнение кода
if (!categoriesGrid || !itemsContainer) return;

// Шаг 2: Меняем видимость (прячем сетку категорий, показываем блок товаров)
categoriesGrid.style.display = "none";
itemsContainer.style.display = "block";

// Шаг 3: Выводим текст ожидания, пока идет запрос к серверу
itemsContainer.innerHTML = "<div class='loading'>Загрузка товаров...</div>";

try {
  // Шаг 4: Делаем асинхронный POST-запрос к Flask на роут /shop
  const response = await fetch('/shop', {
    method: 'POST', // Указываем метод отправки данных
    headers: { 'Content-Type': 'application/json' }, // Говорим серверу, что отправляем JSON
    body: JSON.stringify({ category_type: categoryType }) // Пакуем имя категории в строку
  });

  // Шаг 5: Переводим полученный от Flask ответ из JSON в обычный JS-массив
  const items = await response.json();

  // Шаг 6: Полностью очищаем контейнер от текста загрузки
  itemsContainer.innerHTML = "";

  // Если сервер вернул пустой массив (в этой категории нет товаров в БД)
  if (items.length === 0) {
    itemsContainer.innerHTML = "<p style='text-align:center; padding:15px;'>Товаров пока нет</p>";
    return;
  }

  // Шаг 7: Запускаем цикл по всем полученным предметам
  items.forEach(item => {
    // Создаем новый пустой тег <div> для карточки товара
    const itemDiv = document.createElement("div");
    itemDiv.className = "inventory-item"; // Назначаем ему CSS-класс стиля

    // Формируем внутренний HTML-код карточки товара с помощью шаблонных строк ``
    itemDiv.innerHTML = `
        <div class="item-info" style="border-bottom: 1px solid #444; padding: 10px; margin-bottom: 5px;">
            <strong>${item.name}</strong> — <span style="color: #2ecc71;">$${item.price}</span>
            <p style="font-size: 0.85em; color: #ccc; margin: 5px 0;">${item.description}</p>
            <!-- При клике на кнопку вызываем функцию buyItem и передаем ей ID товара из базы -->
            <button onclick="buyItem(${item.id})" class="btn-use" 
                    style="background: #e67e22; color: white; border: none; padding: 6px 12px; cursor: pointer; border-radius: 3px; width: 100%;">
                Купить
            </button>
        </div>
    `;
    // Добавляем готовую карточку товара на экран телефона
    itemsContainer.appendChild(itemDiv);
  });

} catch (error) {
  // Если сервер выключен или упал с ошибкой 500 — выводим ошибку
  console.error("Ошибка магазина:", error);
  itemsContainer.innerHTML = "<p style='text-align:center; color:red;'>Ошибка загрузки</p>";
}
}

// Делаем функцию глобальной, чтобы onclick="loadShop(...)" из HTML её увидел
window.loadShop = loadShop;




// 



// Асинхронная функция для покупки предмета
async function buyItem(itemId) {
  // На всякий случай выводим в консоль ID товара, чтобы видеть, что кнопка нажалась
  console.log("Пытаемся купить предмет с ID:", itemId);

  try {
    // 1. Отправляем запрос на сервер во Flask и ждем, пока он обработает данные
    const response = await fetch('/buy_item', {
      method: 'POST', // Указываем метод POST, так как мы передаем данные на сервер
      headers: { 
        'Content-Type': 'application/json' // Объясняем Фласку, что отправляем данные в формате JSON
      },
      // Превращаем обычный объект JavaScript в текстовую строку JSON, понятную Python
      body: JSON.stringify({ item_id: itemId }) 
    });

    // 2. Ждем, пока сервер пришлет текстовый ответ, и переводим его обратно в объект JavaScript
    const data = await response.json();

    // 3. Проверяем, что ответил твой Python-роут в переменной "status"
    if (data.status === "success") {
      // Если покупка прошла успешно — выводим сообщение от сервера (например: "Куплено: Конверсы")
      alert(data.message);

      // Находим элемент кошелька на экране и моментально меняем в нем сумму денег
      const wallet = document.querySelector(".wallet-img");
      if (wallet) {
        wallet.innerText = `💰 $${data.money}`;
      }
    } else {
      // Если в Python сработала ошибка (например, "Недостаточно денег") — показываем текст ошибки
      alert(data.message);
    }

  } catch (error) {
    // Страховка на случай, если Flask-сервер выключен или упал с ошибкой
    console.error("Критическая ошибка при покупке:", error);
    alert("Ошибка связи с сервером. Попробуйте позже.");
  }
}
