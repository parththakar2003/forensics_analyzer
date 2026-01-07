const inputSection = document.getElementById('inputSection');
const progressSection = document.getElementById('progressSection');
const resultsSection = document.getElementById('resultsSection');
const startBtn = document.getElementById('startBtn');
const resetBtn = document.getElementById('resetBtn');
const inputPath = document.getElementById('inputPath');
const outputDir = document.getElementById('outputDir');

const progressBar = document.getElementById('progressBar');
const progressPercent = document.getElementById('progressPercent');
const filesFound = document.getElementById('filesFound');
const statusText = document.getElementById('statusText');
const activityLog = document.getElementById('activityLog');

let pollInterval;

startBtn.addEventListener('click', async () => {
    const path = inputPath.value.trim();
    const out = outputDir.value.trim();

    if (!path) {
        alert('Please enter an input file path.');
        return;
    }

    try {
        const response = await fetch('/api/carve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input_path: path, output_dir: out })
        });

        if (response.ok) {
            showSection(progressSection);
            startPolling();
        } else {
            const data = await response.json();
            alert('Error: ' + (data.error || 'Failed to start'));
        }
    } catch (e) {
        alert('Connection error: ' + e.message);
    }
});

resetBtn.addEventListener('click', () => {
    showSection(inputSection);
    // Reset UI
    progressBar.style.width = '0%';
    progressPercent.textContent = '0%';
    filesFound.textContent = '0';
    activityLog.innerHTML = '';
});

function showSection(section) {
    [inputSection, progressSection, resultsSection].forEach(s => s.classList.add('hidden'));
    section.classList.remove('hidden');
}

function startPolling() {
    pollInterval = setInterval(async () => {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();

            updateProgress(data);

            if (!data.running && data.progress >= 100) {
                clearInterval(pollInterval);
                setTimeout(() => {
                    showSection(resultsSection);
                }, 1000);
            }
        } catch (e) {
            console.error('Polling error:', e);
        }
    }, 1000);
}

function updateProgress(data) {
    const percent = Math.round(data.progress) + '%';
    progressBar.style.width = percent;
    progressPercent.textContent = percent;
    filesFound.textContent = data.files_found;
    statusText.textContent = data.status;

    // Update log with recent files
    if (data.recent_files && data.recent_files.length > 0) {
        // Clear and rebuild log for simplicity in this demo
        // In a real app, we'd append only new ones
        activityLog.innerHTML = '';
        data.recent_files.reverse().forEach(file => {
            const li = document.createElement('li');
            li.innerHTML = `Found <span class="highlight">${file.type.toUpperCase()}</span>: ${file.name} (${formatBytes(file.size)})`;
            activityLog.appendChild(li);
        });
    }
}

function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}
