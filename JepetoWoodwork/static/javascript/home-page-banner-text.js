// Another animation for the home page

const nameLetters = document.querySelectorAll(".banner div p span");

const changeColorsAnimation = () => {
  const caramelColor = "#B18857";
  const lightColor = "#E9E4D0";
  const animationSpeed = 200;
  let currentTimeoutTime = animationSpeed;
  const finishedAnimationTime = currentTimeoutTime * nameLetters.length;

  const loopAnimation = () => {
    nameLetters.forEach((letter) => {
      setTimeout(() => {
        letter.style.color = caramelColor;
      }, currentTimeoutTime);
      currentTimeoutTime += animationSpeed;
    });

    setTimeout(() => {
      currentTimeoutTime = animationSpeed;
      for (let i = nameLetters.length - 1; i >= 0; i--) {
        const currentLetter = nameLetters[i];
        setTimeout(() => {
          currentLetter.style.color = lightColor;
        }, currentTimeoutTime + animationSpeed);
        currentTimeoutTime += animationSpeed;
      }
      currentTimeoutTime = animationSpeed;
    }, finishedAnimationTime);

    setTimeout(loopAnimation, finishedAnimationTime * 2 + animationSpeed);
  };
  loopAnimation();
};

changeColorsAnimation();
