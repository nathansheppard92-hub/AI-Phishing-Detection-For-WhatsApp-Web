
//gets latest message from whatsapp
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "getMessage") {

        //selects all content from most recent message going in or out
        const messages = document.querySelectorAll('div.message-in, div.message-out');

        //error checking
        if (messages.length > 0) 
        {
            //detects all elements of a message
            //WhatsApp breaks down a message if containing hyperlinks or phone numbers
            const lastMessage = messages[messages.length - 1];
            const textElement = lastMessage.querySelector('[data-testid="selectable-text"]');
            let text = textElement ? textElement.innerText : "";

            //returns detected message
            sendResponse({ message: text });
        } 
        else 
        {
            //returns empty if nothing found
            sendResponse({ message: "" });
        }

        return true;
    }
});