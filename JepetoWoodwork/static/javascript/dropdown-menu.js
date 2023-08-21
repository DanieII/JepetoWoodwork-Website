const hamburger= document.querySelector('.hamburger');
const navigation = document.querySelector('.navigation-menu');
hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navigation.classList.toggle('active');
})