/*function button_shake(){
    var button=document.getElementById("signup-button");
        const id = null;
        clearInterval(id);
        id = setInterval(frame, 5);
        function frame() {
          button.style.transform="rotate(45deg)";
        }
}*/
/*
document.addEventListener("click", function (event) {
    const button=document.getElementById("signup-button");

    // Check if the clicked element is NOT the button
    if (!button.contains(event.target)) {
        let angle = 0;
        let direction = 1;
        let shakeDuration = 250; // Total duration
        let intervalTime = 75;  // Speed of shake
        let elapsed = 0;

        const shakeInterval = setInterval(() => {
            angle = direction * 10;  // Toggle between -10deg and 10deg
            button.style.transform = "rotate("+angle+"deg)";
            direction *= -1; // Change direction
            elapsed += intervalTime;

            if (elapsed >= shakeDuration) {
                clearInterval(shakeInterval);
                button.style.transform = "rotate(0deg)"; // Reset position
            }
        }, intervalTime);
    }
});
*/