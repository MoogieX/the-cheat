document.addEventListener('DOMContentLoaded', () => {
    const gameText = document.getElementById('game-text');
    const userInput = document.getElementById('user-input');

    console.log('Game script loaded.');
    gameText.innerHTML += "<p>Welcome to your text adventure! It's dark here.</p>";

    userInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            const command = userInput.value;
            handleCommand(command);
            userInput.value = '';
        }
    });

    function handleCommand(command) {
        gameText.innerHTML += `<p class=\"user-command\">> ${command}</p>`;
        // TODO: Add game logic here
        gameText.innerHTML += `<p>You typed '${command}', but nothing happens yet.</p>`;
        
        // Auto-scroll to the bottom
        gameText.scrollTop = gameText.scrollHeight;
    }
});
