
//gets latest message from whatsapp
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "getMessage") {

        //collects all selectable messages from whatsapp
        const messages = document.querySelectorAll('[data-testid="selectable-text"]');

        //selects most recent message in the selected chat
        if (messages.length > 0) 
        {
            const recentMessage = messages[messages.length - 1].innerText;
            sendResponse({ message: recentMessage });
        } 

        //if no messages found, return empty variable, which is detected in index.js to show error
        else 
        {
            sendResponse({ message: "" });
        }
        return true;
    }
});