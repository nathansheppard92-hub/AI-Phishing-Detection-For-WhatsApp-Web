
//confirmation the page has loaded
console.log("Application loaded successfully")

document.addEventListener("DOMContentLoaded", () => {

    //detect phishing button
    const detectButton = document.getElementById("detectButton");
    detectButton.addEventListener("click", detectFunction);

    //scan message from WhatsApp button
    const scanButton = document.getElementById("scanButton");
    scanButton.addEventListener("click", scanFunction);

    //paste button
    const pasteButton = document.getElementById("pasteButton");
    pasteButton.addEventListener("click", pasteFunction);

    //show options dropdown
    const optionsButton = document.getElementById("optionsButton");
    optionsButton.addEventListener("click", optionsFunction);

    //user input box
    const inputBox = document.getElementById("inputBox");
    
    //title text will show either red or green
    const predictionText = document.getElementById("predictionText");

    //decision explanation
    const explanationText = document.getElementById("explanationText");

    const breakLine = document.getElementById("breakLine");
})

    let i = 0;
    let j = 0;

    //speed of prediction/explanation fade in
    let typeSpeed = 30;
    let explanation = "";
    let prediction = "";
    
    //animation for text fade in
    function explanationAnimation() 
    {
        if (i < explanation.length) {
        explanationText.innerHTML += explanation.charAt(i);
        i++;
        setTimeout(explanationAnimation, typeSpeed);
    }
}
    //animation for text fade in
    function predictionAnimation() 
    {
        if (j < prediction.length) {
        predictionText.innerHTML += prediction.charAt(j);
        j++;
        setTimeout(predictionAnimation, typeSpeed);
    }
}

//detect phishing function
async function detectFunction() 
{
    //takes inputted message
    const message = inputBox.value;

    //break line animation
    breakLine.classList.add("fade-in");

    //wipes all text
    j = 0;
    predictionText.innerHTML = "";
    i = 0;
    explanationText.innerHTML = "";

    //flask api fetch request
    try {
        const response = await fetch("http://127.0.0.1:5000/detect", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        //returns whether message is spam or safe
        
        if (data.prediction === "spam") 
        {
            predictionText.style.color = "red";
            prediction = "This message is likely spam";
        } 

        else 
        {
            predictionText.style.color = "green";
            prediction = "This message seems safe";
        }

        //returns explanation
        explanation = data.explanation;

        //plays text fade in animations
        predictionAnimation();
        explanationAnimation();

    //if error
    } catch (err) {
        prediction = "";
        explanation = "There was an error";

        //plays text fade in animations
        predictionAnimation();
        explanationAnimation();
    }
}

function scanFunction() 
{
    inputBox.value = "Scan button pressed";
}

async function pasteFunction()
{
    const text = await navigator.clipboard.readText()
    inputBox.value = text;
}


