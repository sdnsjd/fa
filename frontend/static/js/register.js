    //функция скрытия видимости пароля
document.addEventListener('DOMContentLoaded', function () {
    const togglePassword = document.getElementById('toggle-password');
    const passwordField = document.getElementById('password');

    togglePassword.addEventListener('click', function () {
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);

        this.classList.toggle('fa-eye');
        this.classList.toggle('fa-eye-slash');
    });
});

    //функция скрытия окна ошибок
function hideErrorMessages() {
    const errorMessage = document.getElementById('error-message');
    if (errorMessage) {
        setTimeout(() => {
            errorMessage.style.display = 'none';
        }, 5000);
    }
}

    //post запрос для отправки данных на сервер
document.getElementById('register-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const data = {
        username: formData.get('username'),
        password: formData.get('password')
    };

        // валидация данных со стороны клиента
    const errorMessage = document.getElementById('error-message');

    if (!/^[a-zA-Z]/.test(data.username)) {
        errorMessage.textContent = 'Логин должен начинаться с латинской буквы';
        errorMessage.style.color = 'red';
        errorMessage.style.display = 'block';
        hideErrorMessages();
        return;
    }
    if (!/^[a-zA-Z0-9]+$/.test(data.username)) {
        errorMessage.textContent = 'Логин должен содержать только латинские буквы и цифры';
        errorMessage.style.color = 'red';
        errorMessage.style.display = 'block';
        hideErrorMessages();
        return;
    }
    if (data.username.length < 4 || data.username.length > 12) {
        errorMessage.textContent = 'Логин должен быть от 4 до 12 символов';
        errorMessage.style.color = 'red';
        errorMessage.style.display = 'block';
        hideErrorMessages();
        return;
    }
    if (data.password.length < 4 || data.password.length > 12) {
        errorMessage.textContent = 'Пароль должен быть от 4 до 12 символов';
        errorMessage.style.color = 'red';
        errorMessage.style.display = 'block';
        hideErrorMessages();
        return;
    }

    const response = await fetch('/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    if (response.ok) {
        errorMessage.textContent = result.detail;
        errorMessage.style.color = 'green';
        errorMessage.style.display = 'block';

        setTimeout(() => {
            errorMessage.style.display = 'none';
            window.location.href = '/auth/login';
        }, 3000);

    } else {
        errorMessage.textContent = result.detail;
        errorMessage.style.color = 'red';
        errorMessage.style.display = 'block';
        hideErrorMessages();
    }
});

