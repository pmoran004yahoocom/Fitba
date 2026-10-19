<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Soccer Predictions</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 10px; }
        .card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .match-header { font-weight: bold; font-size: 1.1em; margin-bottom: 8px; color: #333; }
        .odds-container { display: flex; justify-content: space-between; margin-bottom: 10px; }
        .odd-box { text-align: center; flex: 1; padding: 8px; background: #eef2f7; border-radius: 8px; margin: 0 2px; }
        .odd-label { font-size: 0.8em; color: #666; text-transform: uppercase; }
        .odd-value { font-weight: bold; font-size: 1.1em; color: #007bff; }
        .score-predict { font-size: 0.9em; text-align: center; color: #444; border-top: 1px solid #eee; padding-top: 8px; }
        .timestamp { font-size: 0.8em; color: #888; text-align: center; margin-bottom: 10px; }
    </style>
</head>
<body>

    <h2 style="text-align: center; color: #333;">Match Predictions</h2>
    <div id="timestamp" class="timestamp">Loading latest data...</div>
    <div id="predictions-container"></div>

    <script>
        // URL to your autonomously updated JSON file (e.g., raw GitHub content URL)
        const DATA_URL = 'https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/predictions.json';

        async function loadPredictions() {
            try {
                const response = await fetch(DATA_URL);
                if (!response.ok) throw new Error('Network response was not ok');
                const data = await response.json();
                
                document.getElementById('timestamp').innerText = `Last updated: ${data.last_updated}`;
                
                const container = document.getElementById('predictions-container');
                container.innerHTML = '';
                
                data.matches.forEach(match => {
                    const card = document.createElement('div');
                    card.className = 'card';
                    card.innerHTML = `
                        <div class="match-header">${match.home_team} vs ${match.away_team}</div>
                        <div class="odds-container">
                            <div class="odd-box"><div class="odd-label">Home</div><div class="odd-value">${(match.home_win * 100).toFixed(0)}%</div></div>
                            <div class="odd-box"><div class="odd-label">Draw</div><div class="odd-value">${(match.draw * 100).toFixed(0)}%</div></div>
                            <div class="odd-box"><div class="odd-label">Away</div><div class="odd-value">${(match.away_win * 100).toFixed(0)}%</div></div>
                        </div>
                        <div class="score-predict">Most Likely Score: <strong>${match.score}</strong></div>
                    `;
                    container.appendChild(card);
                });
            } catch (error) {
                console.error('Error loading predictions:', error);
                document.getElementById('timestamp').innerText = 'Failed to load predictions. Check connection or pipeline.';
            }
        }

        loadPredictions();
    </script>
</body>
</html>
