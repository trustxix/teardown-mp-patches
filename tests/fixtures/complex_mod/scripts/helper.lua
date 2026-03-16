function calculateScore(kills, survivalTime)
    return kills * 100 + survivalTime * 10
end

function formatTime(seconds)
    local mins = math.floor(seconds / 60)
    local secs = math.floor(seconds % 60)
    return string.format("%02d:%02d", mins, secs)
end
