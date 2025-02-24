
function openAddProductModal() {
    document.getElementById('addProductModal').style.display = 'block';
}

function closeAddProductModal() {
    document.getElementById('addProductModal').style.display = 'none';
}


async function addProduct() {
// Получаем форму
const form = document.getElementById('addProductForm');

// Создаем объект FormData из формы
const formData = new FormData(form);

// Логируем все ключи и значения из formData
for (let [key, value] of formData.entries()) {
    console.log(`${key}: ${value}`);
}

try {
    // Отправляем данные на сервер
    const response = await fetch('/admin/panel/add_product', {
        method: 'POST',
        body: formData
    });

    // Проверяем успешность ответа
    if (response.ok) {
        // Если успешно, выводим сообщение и перезагружаем страницу
        const result = await response.json();
        alert(result.message);
        location.reload(); // Перезагружаем страницу
    } else {
        // Если произошла ошибка, выводим сообщение об ошибке
        const errorData = await response.json();
        console.error('Ошибка:', errorData);
        alert('Ошибка при добавлении товара: ' + JSON.stringify(errorData));
    }
} catch (error) {
    // Обработка ошибок, например, если не удается подключиться к серверу
    console.error('Error:', error);
    alert('Ошибка при добавлении товара.');
}
}





async function deleteProduct(productId) {
    try {

        console.log(`Тип данных productId: ${typeof productId}`);
        const response = await fetch(`/admin/panel/delete_product/${productId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            // Успешное удаление товара
            alert('Товар успешно удален');
            // Обновите таблицу или удалите строку товара из DOM
            const row = document.querySelector(`tr[data-product-id="${productId}"]`);
            if (row) {
                row.remove();
            }
        } else {
            // Обработка ошибки
            const errorData = await response.json();
            alert(`Ошибка при удалении товара: ${errorData.message}`);
        }
    } catch (error) {
        // Обработка сетевых ошибок
        alert(`Ошибка сети: ${error.message}`);
    }
}


function editProduct(productId) {
// Получите данные товара из строки таблицы
const row = document.querySelector(`tr[data-product-id="${productId}"]`);
const name = row.querySelector('td:nth-child(2)').textContent;
const price = row.querySelector('td:nth-child(3)').textContent;
const size = row.querySelector('td:nth-child(4)').textContent;
const quantity = row.querySelector('td:nth-child(5)').textContent;
const category = row.querySelector('td:nth-child(6)').textContent;
const mainImage = row.querySelector('td:nth-child(7) img').src;

// Заполните форму данными товара
document.getElementById('editProductId').value = productId;
document.getElementById('editProductName').value = name;
document.getElementById('editProductPrice').value = price;
document.getElementById('editProductSize').value = size;
document.getElementById('editProductQuantity').value = quantity;
document.getElementById('editProductCategory').value = category;
document.getElementById('editProductMainImage').value = mainImage;

// Покажите форму редактирования
document.getElementById('editProductModal').style.display = 'block';
}

function closeEditProductModal() {
    document.getElementById('editProductModal').style.display = 'none';
}

async function saveProduct() {
const productId = document.getElementById('editProductId').value;
const name = document.getElementById('editProductName').value;
const price = document.getElementById('editProductPrice').value;
const size = document.getElementById('editProductSize').value;
const quantity = document.getElementById('editProductQuantity').value;
const category = document.getElementById('editProductCategory').value;
const mainImage = document.getElementById('editProductMainImage').value;

const productData = {
    id: productId,
    name: name,
    price: parseFloat(price),
    size: size,
    quantity: parseInt(quantity),
    category: category,
    main_image: mainImage
};

try {
    const response = await fetch(`/admin/panel/update_product/${productId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(productData)
    });

    if (response.ok) {
        // Успешное обновление товара
        alert('Товар успешно обновлен');
        // Обновите данные товара в таблице
        const row = document.querySelector(`tr[data-product-id="${productId}"]`);
        row.querySelector('td:nth-child(2)').textContent = name;
        row.querySelector('td:nth-child(3)').textContent = price;
        row.querySelector('td:nth-child(4)').textContent = size;
        row.querySelector('td:nth-child(5)').textContent = quantity;
        row.querySelector('td:nth-child(6)').textContent = category;
        row.querySelector('td:nth-child(7) img').src = mainImage;

        // Скрыть форму редактирования
        document.getElementById('editProductModal').style.display = 'none';
    } else {
        // Обработка ошибки
        const errorData = await response.json();
        alert(`Ошибка при обновлении товара: ${errorData.message}`);
    }
} catch (error) {
    // Обработка сетевых ошибок
    alert(`Ошибка сети: ${error.message}`);
}
}