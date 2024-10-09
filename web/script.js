    // Function to update clock
    function updateClock() {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        const seconds = now.getSeconds().toString().padStart(2, '0');
        const timeString = `${hours}:${minutes}:${seconds}`;
        const clockElement = document.getElementById('clock');
        if (clockElement) {
            clockElement.textContent = timeString;
        }

        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        const dateString = now.toLocaleDateString('en-US', options);
        const dateElement = document.getElementById('date');
        if (dateElement) {
            dateElement.textContent = dateString;
        }
    }

    // Function to update weather information
    function updateWeather() {
        eel.get_weather()().then(function(weatherData) {
            if (weatherData.error) {
                console.error(weatherData.error);
                return;
            }
            const cityElement = document.getElementById('city');
            const temperatureElement = document.getElementById('temperature');
            const descriptionElement = document.getElementById('weather-description');
            const humidityElement = document.getElementById('humidity');
            const iconElement = document.getElementById('weather-icon');

            if (cityElement) cityElement.textContent = weatherData.city;
            if (temperatureElement) temperatureElement.textContent = weatherData.temperature + '°C';
            if (descriptionElement) descriptionElement.textContent = weatherData.description;
            if (humidityElement) humidityElement.textContent = 'Humidity: ' + weatherData.humidity + '%';
    
            // Set weather icon
            if (iconElement) {
                iconElement.src = weatherData.icon_url;
                iconElement.alt = weatherData.description;
            }
        });
    }

    // Function to update calendar information
    function updateCalendar() {
        eel.calendar()().then(function(result) {
            const calendarContainer = document.getElementById('calendar-container');
            if (calendarContainer) {
                if (typeof result === 'object') {
                    calendarContainer.innerHTML = `Next event: <a href="${result.link}" target="_blank">${result.summary}</a> at ${result.start}`;
                } else {
                    calendarContainer.textContent = result;
                }
            }
        });
    }

    // Function to update user message
    function updateUserMessage() {
        eel.display_user_message()().then(function(message) {
            const userMessageElement = document.getElementById('user-message');
            if (userMessageElement) {
                userMessageElement.textContent = message;
            }
        });
    }

    // Function to update all information
    function updateAll() {
        updateClock();
        updateWeather();
        updateCalendar();
        updateUserMessage();
    }

    // Call updateAll immediately and then every second for clock, every 10 minutes for weather and calendar
    updateAll();
    setInterval(updateClock, 10);
    setInterval(updateWeather, 60000);
    setInterval(updateCalendar, 10);
    setInterval(updateUserMessage, 10);
