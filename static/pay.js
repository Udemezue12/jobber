document.addEventListener('DOMContentLoaded', function() {
    function fetchCountries() {
        fetch('https://country-api-1.onrender.com/country/countries')
            .then(response => response.json())
            .then(data => {
                const countrySelect = document.getElementById('country');
                countrySelect.innerHTML = '';  // Clear existing options
                data.forEach(country => {
                    const option = document.createElement('option');
                    option.value = country[0];  // country code
                    option.textContent = country[1];  // country name
                    countrySelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching countries:', error));
    }

    const countrySelect = document.getElementById('country');
    const stateSelect = document.getElementById('state');

    countrySelect.addEventListener('change', function() {
        const selectedCountry = countrySelect.value;
        if (selectedCountry) {
            fetch(`https://country-api-1.onrender.com/states/states/${selectedCountry}`)
                .then(response => response.json())
                .then(data => {
                    stateSelect.innerHTML = '';  // Clear previous options
                    data.forEach(state => {
                        const option = document.createElement('option');
                        option.value = state;
                        option.textContent = state;
                        stateSelect.appendChild(option);
                    });
                })
                .catch(error => console.error('Error fetching states:', error));
        } else {
            stateSelect.innerHTML = '';
        }
    });

    fetchCountries();
});