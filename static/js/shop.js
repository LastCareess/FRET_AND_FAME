const locationShopData = {
    categories: [
        { id: "weapons", label: "Оружие" },
        { id: "services", label: " Услуги" },
        { id: "business", label: " Бизнес" }
    ],
    items: {
        weapons: [
            { id: "w_1", label: "Купить Кастет", price: 150 },
            { id: "w_2", label: "Купить Револьвер", price: 600 }
        ],
        services: [
            { id: "s_1", label: "Подкупить шерифа", price: 300 },
            { id: "s_2", label: "Нанять охрану", price: 800 }
        ],
        business: [
            { id: "b_1", label: "Купить бензоколонку", price: 2500 },
            { id: "b_2", label: "Открыть Закусочную", price: 4000 }
        ]
    }
};

function showCategories() {
    const container = document.getElementById('menu-buttons-container');
    const title = document.getElementById('menu-title');
    const backBtn = document.getElementById('back-btn');

    if (!container || !title || !backBtn) return;

    title.innerText = "Выберите категорию";
    backBtn.classList.add('hidden'); 
    container.innerHTML = ''; 

    locationShopData.categories.forEach(cat => {
        const btn = document.createElement('button');
        btn.className = 'action-location-btn';
        btn.innerText = cat.label;
        btn.onclick = () => showItems(cat.id, cat.label);
        container.appendChild(btn);
    });
}

function showItems(categoryId, categoryLabel) {
    const container = document.getElementById('menu-buttons-container');
    const title = document.getElementById('menu-title');
    const backBtn = document.getElementById('back-btn');

    title.innerText = categoryLabel;
    backBtn.classList.remove('hidden'); 
    container.innerHTML = ''; 

    const currentItems = locationShopData.items[categoryId] || [];

    currentItems.forEach(item => {
        const btn = document.createElement('button');
        btn.className = 'action-location-btn';
        btn.innerHTML = `
            <span>${item.label}</span>
            <span class="btn-price">${item.price} $</span>
        `;
        btn.onclick = () => buyAction(item.id, item.price, item.label);
        container.appendChild(btn);
    });
}

function buyAction(itemId, price, label) {
    console.log(`Клик по кнопке: ${itemId}, Цена: ${price}$`);
    alert(`Вы купили: "${label}" за ${price}$!`);
}

document.addEventListener("DOMContentLoaded", () => {
    showCategories();
});