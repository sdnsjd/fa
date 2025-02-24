document.addEventListener("DOMContentLoaded", function () {
    const products = document.querySelectorAll('.product');
    products.forEach(product => {
        const category = product.getAttribute('data-category');
        console.log(`Product Name: ${product.getAttribute('data-product-name')}, Category: ${category}`);
    });
});


        let currentProductId = null;
        let currentImageIndex = 0;
        let images = [];

        function openModal(productId) {
            currentProductId = productId;
            fetchProductImages(productId);
            document.getElementById('imageModal').style.display = 'flex';

            // Добавляем обработчик события для нажатия клавиши ESC
            document.addEventListener('keydown', handleKeyDown);
        }

        function closeModal() {
            document.getElementById('imageModal').style.display = 'none';
            currentImageIndex = 0;
            images = [];
            document.removeEventListener('keydown', handleKeyDown);
        }

        function handleKeyDown(event) {
            if (event.key === 'Escape') { // Проверяем, нажата ли клавиша ESC
                closeModal();
            }
        }

        function closeModalOnClickOutside(event) {
            // Закрываем модальное окно, если клик был вне его содержимого
            if (event.target === document.getElementById('imageModal')) {
                closeModal();
            }
        }


        async function fetchProductImages(productId) {
            try {
                const response = await fetch(`/product/${productId}/images`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                images = data.images;
                if (images.length > 0) {
                    showImage(0);
                }
            } catch (error) {
                console.error("Error fetching images:", error);
            }
        }

        function showImage(index) {
            if (index >= 0 && index < images.length) {
                currentImageIndex = index;
                document.getElementById('modalImage').src = images[index];
            }
        }

        function prevImage() {
            if (currentImageIndex > 0) {
                showImage(currentImageIndex - 1);
            }
        }

        function nextImage() {
            if (currentImageIndex < images.length - 1) {
                showImage(currentImageIndex + 1);
            }
        }

        function toggleDropdown() {
            var dropdownContent = document.getElementById('dropdown-content');
            if (dropdownContent.style.display === 'block') {
                dropdownContent.style.display = 'none';
            } else {
                dropdownContent.style.display = 'block';
            }
        }

        document.addEventListener('click', function(event) {
            var dropdownContent = document.getElementById('dropdown-content');
            var username = document.querySelector('.username');
            if (!username.contains(event.target) && !dropdownContent.contains(event.target)) {
                dropdownContent.style.display = 'none';
            }
        });

        let selectedSizes = {};

        function selectProductSize(element, productId, size) {
            const productElement = element.closest('.product');
            const productName = productElement.getAttribute('data-product-name');

            // Проверяем, был ли этот размер уже выбран
            if (selectedSizes[productName] && selectedSizes[productName].size === size) {
                // Если выбранный размер совпадает с текущим, отменяем выбор
                element.classList.remove('selected');
                delete selectedSizes[productName];
                console.log(`Отменен выбор размера ${size} для товара ${productName}`);
            } else {
                // Убираем выделение у всех размеров этого товара
                const sizes = productElement.querySelectorAll('.size-label');
                sizes.forEach(s => s.classList.remove('selected'));

                // Выделяем выбранный размер
                element.classList.add('selected');

                // Сохраняем выбранный размер для данного товара
                selectedSizes[productName] = { id: productId, size: size };

                console.log(`Выбран размер ${size} для товара ${productName}`);
            }
        }

        async function addToCart(productIdentifier, isSocks) {
            let productId, size;

            if (isSocks) {
                // Если это носки, используем идентификатор продукта напрямую и не проверяем размер
                productId = productIdentifier;
                size = null;
            } else {
                // Если это не носки, используем имя продукта и проверяем выбранный размер
                const productName = productIdentifier;
                if (!selectedSizes[productName]) {
                    alert("Пожалуйста, выберите размер перед добавлением в корзину.");
                    return;
                }
                const selectedProduct = selectedSizes[productName];
                productId = selectedProduct.id;
                size = selectedProduct.size;
            }

            try {
                const response = await fetch('/cart/add_to_cart', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ product_id: productId, size: size, quantity: 1 })
                });

                if (response.ok) {
                    const cart = await response.json();
                    console.log(`Товар с ID ${productId} добавлен в корзину.`);
                    console.log('Updated cart:', cart);
                    // Обновить интерфейс корзины на основе полученных данных
                } else {
                    console.error('Failed to add to cart');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }


        function goToCart() {
            window.location.href = '/cart';
        }

        function goToAdminPanel() {
            window.location.href = '/admin/panel';
        }

        function register() {
            window.location.href = '/auth/register';
        }

        function login() {
            window.location.href = '/auth/login';
        }

        async function logout() {
            try {
                const response = await fetch('/auth/logout', {
                    method: 'POST',
                    credentials: 'same-origin'
                });

                if (response.redirected) {
                    window.location.href = response.url;
                }
            } catch (error) {
                console.error('Ошибка при выполнении logout:', error);
            }
        }

document.addEventListener("DOMContentLoaded", function () {
    selectCategory('tshirts'); // Выбираем категорию "Футболки" по умолчанию
    filterProducts(); // Применяем фильтры при загрузке страницы
});

let selectedCategory = 'tshirts'; // Переменная для хранения выбранной категории

function selectCategory(category) {
    // Убираем активный класс у всех категорий
    document.querySelectorAll('.category').forEach(cat => cat.classList.remove('active'));

    // Добавляем активный класс выбранной категории
    const selectedCategoryElement = document.querySelector(`.category[onclick="selectCategory('${category}')"]`);
    if (selectedCategoryElement) {
        selectedCategoryElement.classList.add('active');
    }

    // Обновляем выбранную категорию
    selectedCategory = category;

    // Управляем видимостью панели фильтров
    const filterPanel = document.getElementById('tshirts-filter-panel');
    if (filterPanel) {
        if (category === 'tshirts') {
            filterPanel.classList.add('active');
        } else {
            filterPanel.classList.remove('active');
        }
    }

    // Применяем фильтрацию товаров
    filterProducts();
}

function filterProducts() {
    const minPrice = parseFloat(document.getElementById('min-price').value) || 0;
    const maxPrice = parseFloat(document.getElementById('max-price').value) || Infinity;
    const selectedSizes = Array.from(document.querySelectorAll('.size.active')).map(s => s.textContent);

    const products = document.querySelectorAll('.product');

    products.forEach(product => {
        const productCategory = product.getAttribute('data-category');
        const productPrice = parseFloat(product.querySelector('.price').textContent.replace('$', ''));
        const productSizes = Array.from(product.querySelectorAll('.size-label')).map(s => s.textContent);

        const categoryMatches = productCategory === selectedCategory;
        const priceInRange = productPrice >= minPrice && productPrice <= maxPrice;
        const sizeMatches = selectedSizes.length === 0 || productSizes.some(size => selectedSizes.includes(size));

        if (categoryMatches && priceInRange && sizeMatches) {
            product.style.display = 'block';
        } else {
            product.style.display = 'none';
        }
    });
}

function resetFilters() {
    document.querySelectorAll('.size').forEach(size => size.classList.remove('active'));
    document.getElementById('min-price').value = 0;
    document.getElementById('max-price').value = 100;
    updatePrice('min');
    updatePrice('max');
    filterProducts();
}

function updatePrice(type) {
    const priceElement = document.getElementById(`${type}-price`);
    if (priceElement) {
        const price = parseFloat(priceElement.value);
        if (!isNaN(price)) {
            priceElement.value = price.toFixed(2);
        }
    }
}



function selectSize(size) {
    const sizeElement = document.querySelector(`.size[onclick="selectSize('${size}')"]`);
    sizeElement.classList.toggle('active');
    filterProducts();
}


function updatePrice(type) {
    const minPriceInput = document.getElementById('min-price');
    const maxPriceInput = document.getElementById('max-price');
    const minThumb = document.getElementById('min-thumb');
    const maxThumb = document.getElementById('max-thumb');
    const sliderWidth = document.querySelector('.slider').offsetWidth;

    if (type === 'min') {
        const minValue = parseInt(minPriceInput.value);
        const maxValue = parseInt(maxPriceInput.value);
        if (minValue > maxValue) {
            minPriceInput.value = maxValue;
        }
        const position = ((minPriceInput.value - 0) / (100 - 0)) * sliderWidth;
        minThumb.style.left = `${position}px`;
    } else {
        const minValue = parseInt(minPriceInput.value);
        const maxValue = parseInt(maxPriceInput.value);
        if (maxValue < minValue) {
            maxPriceInput.value = minValue;
        }
        const position = ((maxPriceInput.value - 0) / (100 - 0)) * sliderWidth;
        maxThumb.style.left = `${position}px`;
    }

    filterProducts();
}







        let isDragging = false;
        let currentThumb = null;

        function startDrag(type) {
            isDragging = true;
            currentThumb = type;
            document.addEventListener('mousemove', drag);
            document.addEventListener('mouseup', stopDrag);
        }

        function drag(event) {
            if (!isDragging) return;

            const slider = document.querySelector('.slider');
            const sliderRect = slider.getBoundingClientRect();
            const minThumb = document.getElementById('min-thumb');
            const maxThumb = document.getElementById('max-thumb');
            const minPriceInput = document.getElementById('min-price');
            const maxPriceInput = document.getElementById('max-price');

            let position = event.clientX - sliderRect.left;
            position = Math.max(0, Math.min(position, sliderRect.width));

            if (currentThumb === 'min') {
                const minValue = Math.round((position / sliderRect.width) * 100);
                minPriceInput.value = minValue;
                minThumb.style.left = `${position}px`;
            } else {
                const maxValue = Math.round((position / sliderRect.width) * 100);
                maxPriceInput.value = maxValue;
                maxThumb.style.left = `${position}px`;
            }

            updatePrice(currentThumb);
        }

        function stopDrag() {
            isDragging = false;
            currentThumb = null;
            document.removeEventListener('mousemove', drag);
            document.removeEventListener('mouseup', stopDrag);
        }
