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

    //post запрос для отправки данных на сервер
document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const response = await fetch('/auth/login', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    const errorMessage = document.getElementById('error-message');

    if (response.ok) {
        errorMessage.textContent = 'Вход выполнен';
        errorMessage.style.color = 'green';
        errorMessage.style.display = 'block';

        setTimeout(() => {
            errorMessage.style.display = 'none';
            window.location.href = '/';
        }, 3000);
    } else {
        errorMessage.textContent = result.error;
        errorMessage.style.color = 'red';
        errorMessage.style.display = 'block';

        setTimeout(() => {
            errorMessage.style.display = 'none';
        }, 5000);
    }
});

