function scrollToAdvantages() {
   // Найти элемент по id
    var advantages = document.getElementById("advantages");
    // Прокрутить страницу к элементу
    advantages.scrollIntoView();
}


var button = document.getElementById("learn");
// добавляем обработчик события, который будет вызывать функцию scrollToBelow() при клике на кнопку
button.addEventListener("click", scrollToAdvantages);

