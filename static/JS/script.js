const moodData = {
    labels: ['Happy', 'Neutral', 'Sad'],
    datasets: [{
        label: 'Mood Tracking',
        data: [0, 0, 0],
        backgroundColor: [
            'rgba(75, 192, 192, 0.6)', // Happy
            'rgba(255, 159, 64, 0.6)', // Neutral
            'rgba(255, 99, 132, 0.6)'  // Sad
        ],
        borderColor: [
            'rgba(75, 192, 192, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(255, 99, 132, 1)'
        ],
        borderWidth: 1
    }]
};

const sleepData = [];
const waterData = [];
const exerciseData = [];

const moodCtx = document.getElementById('moodChart').getContext('2d');
const sleepCtx = document.getElementById('sleepChart').getContext('2d');
const waterCtx = document.getElementById('waterChart').getContext('2d');
const exerciseCtx = document.getElementById('exerciseChart').getContext('2d');

const moodChart = new Chart(moodCtx, {
    type: 'pie',
    data: moodData
});

const sleepChart = new Chart(sleepCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Sleep Hours',
            data: sleepData,
            fill: false,
            borderColor: '#4CAF50',
            tension: 0.1
        }]
    }
});

const waterChart = new Chart(waterCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Water Intake (liters)',
            data: waterData,
            fill: false,
            borderColor: '#3b8cc7',
            tension: 0.1
        }]
    }
});

const exerciseChart = new Chart(exerciseCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Exercise Duration (minutes)',
            data: exerciseData,
            fill: false,
            borderColor: '#ff8c00',
            tension: 0.1
        }]
    }
});

document.getElementById('saveBtn').addEventListener('click', function() {
    const mood = document.getElementById('moodSelect').value;
    const sleepHours = document.getElementById('sleepHours').value;
    const waterIntake = document.getElementById('waterIntake').value;
    const exerciseDuration = document.getElementById('exerciseDuration').value;
    const mindfulness = document.getElementById('mindfulness').value;
    const nutrition = document.getElementById('nutrition').value;
    const goal = document.getElementById('goal').value;

    if (!mood || !sleepHours || !waterIntake || !exerciseDuration || !mindfulness || !nutrition || !goal) {
        document.getElementById('feedback').textContent = 'Please fill out all fields!';
        document.getElementById('feedback').style.color = 'red';
        return;
    }

    // Update mood chart
    if (mood === 'happy') moodData.datasets[0].data[0]++;
    else if (mood === 'neutral') moodData.datasets[0].data[1]++;
    else if (mood === 'sad') moodData.datasets[0].data[2]++;
    moodChart.update();

    // Add data to sleep, water and exercise charts
    sleepData.push(sleepHours);
    waterData.push(waterIntake);
    exerciseData.push(exerciseDuration);

    // Update charts
    sleepChart.data.labels.push(new Date().toLocaleTimeString());
    waterChart.data.labels.push(new Date().toLocaleTimeString());
    exerciseChart.data.labels.push(new Date().toLocaleTimeString());

    sleepChart.update();
    waterChart.update();
    exerciseChart.update();

    // Analytics
    displayAnalytics();

    const data = {
        mood,
        sleepHours,
        waterIntake,
        exerciseDuration,
        mindfulness,
        nutrition,
        goal
    };
    localStorage.setItem('selfCareData', JSON.stringify(data));
    document.getElementById('feedback').textContent = 'Data saved successfully!';
    document.getElementById('feedback').style.color = 'green';
});

function displayAnalytics() {
    const totalSleep = sleepData.reduce((acc, val) => acc + parseFloat(val), 0);
    const totalWater = waterData.reduce((acc, val) => acc + parseFloat(val), 0);
    const totalExercise = exerciseData.reduce((acc, val) => acc + parseFloat(val), 0);

    document.getElementById('analyticsData').innerHTML = `
        <div>
            <strong>Total Sleep</strong>
            <p>${totalSleep} hours</p>
        </div>
        <div>
            <strong>Total Water Intake</strong>
            <p>${totalWater} liters</p>
        </div>
        <div>
            <strong>Total Exercise</strong>
            <p>${totalExercise} minutes</p>
        </div>
    `;
}
