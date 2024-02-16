function myFunction() {
  let x = document.getElementById("myText").value;
  console.log(x)
  chartCountryLifeExpectancy(x, "userCountry")
}


fetch('./JSON/maleFemale.json')
  .then(response => response.json())
  .then(data => {
    const ctx = document.getElementById('maleFemale').getContext('2d');
    const years = Object.keys(data);
    const male = [];
    const female = [];

    for (let i = 0; i < years.length; i++) {
      female.push(data[years[i]][0]); 
      male.push(data[years[i]][1]); 
    }

    new Chart(ctx, {
      type: 'line',
      data: {
        labels: years,
        datasets: [
          {
            label: 'Male',
            data: male,
            borderColor: 'blue',
            backgroundColor: 'rgba(0, 0, 255, 0.1)', 
          },
          {
            label: 'Female',
            data: female,
            borderColor: 'pink',
            backgroundColor: 'rgba(255, 192, 203, 0.1)', 
          }
        ]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true 
          }
        }
      }
    });
  })
  .catch(error => console.error('Error fetching JSON:', error));


fetch('./JSON/change.json')
.then(response => response.json())
.then(data => {
  const ctx = document.getElementById('lifeExpectancyChart').getContext('2d');
  const countries = Object.keys(data);
  const datasets = countries.map(country => ({
    label: `${country}`,
    data: data[country],
    fill: false,
    borderColor: getRandomColor(), 
    tension: 0.1
  }));

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: Array.from({length: data[countries[0]].length}, (_, i) => 1950 + i), 
      datasets: datasets
    },
    options: {
      scales: {
        y: {
          beginAtZero: false
        }
      }
    }
  });
})
.catch(error => console.error('Error fetching JSON:', error));


fetch('./JSON/continentPerYear.json')
  .then(response => response.json())
  .then(data => {
    const ctx = document.getElementById('continentPerYear').getContext('2d');
    const continents = new Set();
    const years = new Set();
    const lifeExpectancyData = {};

    Object.keys(data).forEach(key => {
      const [continent, year] = key.replace('(', '').replace(')', '').split(', ');
      continents.add(continent);
      years.add(year);

      if (!lifeExpectancyData[continent]) {
        lifeExpectancyData[continent] = {};
      }
      lifeExpectancyData[continent][year] = data[key];
    });

    const sortedYears = Array.from(years).sort();
    const datasets = Array.from(continents).map(continent => {
      return {
        label: continent,
        data: sortedYears.map(year => lifeExpectancyData[continent][year] || null),
        fill: false, 
      };
    });

    new Chart(ctx, {
      type: 'line',
      data: {
        labels: sortedYears,
        datasets: datasets
      },
      options: {
        scales: {
          y: {
            beginAtZero: false, // Depending on your data, you may want to start at a different value
            title: {
              display: true,
              text: 'Average Life Expectancy'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Year'
            }
          }
        },
        plugins: {
          title: {
            display: true,
            text: 'Average Life Expectancy by Continent and Year'
          }
        }
      }
    });
  })
  .catch(error => console.error('Error fetching JSON:', error));

let myChart = null;

function chartCountryLifeExpectancy(country, temp) {
  fetch('./JSON/country.json')
    .then(response => response.json())
    .then(data => {
      const countryData = data[country];
      if (!countryData) {
        console.error('Country data not found');
        return;
      }

      const maleLife = countryData[1];
      const femaleLife = countryData[0];
      const years = Array.from({ length: 2019 - 1950 }, (_, i) => i + 1950);

      const ctx = document.getElementById(temp).getContext('2d');
      if (myChart) {
        myChart.destroy();
      }

      myChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: years,
          datasets: [
            {
              label: 'Male Life Expectancy',
              data: maleLife,
              borderColor: 'blue',
              backgroundColor: 'rgba(0, 0, 255, 0.1)',
            },
            {
              label: 'Female Life Expectancy',
              data: femaleLife,
              borderColor: 'pink',
              backgroundColor: 'rgba(255, 192, 203, 0.1)',
            }
          ]
        },
        options: {
          scales: {
            y: {
              beginAtZero: false,
              title: {
                display: true,
                text: 'Life Expectancy (years)'
              }
            },
            x: {
              title: {
                display: true,
                text: 'Year'
              }
            }
          },
          plugins: {
            title: {
              display: true,
              text: `Life Expectancy in ${country} (1950-2018)`
            }
          }
        }
      });
    })
    .catch(error => console.error('Error fetching country data:', error));
}

function chartCountryLifeExpectancy2(country, temp = "exampleCountry") {
  fetch('./JSON/country.json')
    .then(response => response.json())
    .then(data => {
      const countryData = data[country];
      if (!countryData) {
        console.error('Country data not found');
        return;
      }

      const maleLife = countryData[1];
      const femaleLife = countryData[0];
      const years = Array.from({ length: 2019 - 1950 }, (_, i) => i + 1950);
      
      const ctx = document.getElementById(`${temp}`).getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: years,
          datasets: [
            {
              label: 'Male Life Expectancy',
              data: maleLife,
              borderColor: 'blue',
              backgroundColor: 'rgba(0, 0, 255, 0.1)',
            },
            {
              label: 'Female Life Expectancy',
              data: femaleLife,
              borderColor: 'pink',
              backgroundColor: 'rgba(255, 192, 203, 0.1)',
            }
          ]
        },
        options: {
          scales: {
            y: {
              beginAtZero: false,
              title: {
                display: true,
                text: 'Life Expectancy (years)'
              }
            },
            x: {
              title: {
                display: true,
                text: 'Year'
              }
            }
          },
          plugins: {
            title: {
              display: true,
              text: `Life Expectancy in ${country} (1950-2018)`
            }
          }
        }
      });
    })
    .catch(error => console.error('Error fetching country data:', error));
}


chartCountryLifeExpectancy2('Norway', "exampleCountry");
chartCountryLifeExpectancy("Germany", "userCountry");

function getRandomColor() {
  const letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}
