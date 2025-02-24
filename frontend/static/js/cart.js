async function increaseQuantity(productId) {
    try {
        const response = await fetch(`/cart/increase`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ product_id: productId })
        });
        const data = await response.json();
        if (data.status === "success") {
            const productItem = document.querySelector(`.product-item[data-product-id="${productId}"]`);
            const input = productItem.querySelector('.quantity-control input');
            const currentQuantity = parseInt(input.value);
            const newQuantity = currentQuantity + 1;
            input.value = newQuantity;

            // Обновить общую цену за товар
            const productTotalPriceElement = productItem.querySelector('.product-item-total');
            const currentTotalPrice = parseFloat(productTotalPriceElement.textContent.split('$')[1]);

            // Рассчитать цену за единицу товара
            const unitPrice = currentTotalPrice / currentQuantity;

            // Рассчитать новую общую цену за товар
            const newTotalPrice = unitPrice * newQuantity;
            productTotalPriceElement.textContent = `Общая цена: $${newTotalPrice.toFixed(2)}`;

            // Обновить общую сумму всех товаров
            updateTotalPrice();
        } else {
            alert('Ошибка при увеличении количества товара.');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function decreaseQuantity(productId) {
    try {
        const response = await fetch(`/cart/decrease`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ product_id: productId })
        });
        const data = await response.json();
        if (data.status === "success") {
            const productItem = document.querySelector(`.product-item[data-product-id="${productId}"]`);
            const input = productItem.querySelector('.quantity-control input');
            const currentQuantity = parseInt(input.value);
            const newQuantity = currentQuantity - 1;

            if (newQuantity === 0) {
                productItem.remove();
            } else {
                input.value = newQuantity;

                // Обновить общую цену за товар
                const productTotalPriceElement = productItem.querySelector('.product-item-total');
                const currentTotalPrice = parseFloat(productTotalPriceElement.textContent.split('$')[1]);

                // Рассчитать цену за единицу товара
                const unitPrice = currentTotalPrice / currentQuantity;

                // Рассчитать новую общую цену за товар
                const newTotalPrice = unitPrice * newQuantity;
                productTotalPriceElement.textContent = `Общая цена: $${newTotalPrice.toFixed(2)}`;
            }

            // Обновить общую сумму всех товаров
            updateTotalPrice();
        } else {
            alert('Ошибка при уменьшении количества товара.');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function removeProduct(productId) {
    try {
        const response = await fetch(`/cart/remove`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ product_id: productId })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.status === "success") {
            const productItem = document.querySelector(`.product-item[data-product-id="${productId}"]`);
            if (productItem) {
                productItem.remove();
                updateTotalPrice();
            } else {
                console.error('Product item element not found.');
            }
        } else {
            alert('Ошибка при удалении товара.');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function updateTotalPrice() {
    let totalPrice = 0;
    document.querySelectorAll('.product-item').forEach(item => {
        const itemTotalPrice = parseFloat(item.querySelector('.product-item-total').textContent.split('$')[1]);
        totalPrice += itemTotalPrice;
    });
    document.querySelector('.summary').textContent = `Общая сумма: $${totalPrice.toFixed(2)}`;
}