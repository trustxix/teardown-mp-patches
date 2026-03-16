local gameState = "waiting"
local players = {}
local timer = 0
local zoneRadius = 500
local scores = {}

function init()
    SetInt("game_round", 0)
    SetString("game_state", "waiting")
end

function tick(dt)
    if gameState == "waiting" then
        if InputPressed("interact") then
            gameState = "countdown"
            timer = 10
        end
    elseif gameState == "countdown" then
        timer = timer - dt
        if timer <= 0 then
            gameState = "active"
            SetInt("game_round", GetInt("game_round") + 1)
        end
    elseif gameState == "active" then
        zoneRadius = zoneRadius - dt * 2
        local health = GetPlayerHealth()
        if health <= 0 then
            gameState = "dead"
            SetString("game_state", "dead")
        end
        local t = GetPlayerTransform()
        local dist = VecLength(t.pos)
        if dist > zoneRadius then
            SetPlayerHealth(GetPlayerHealth() - dt * 0.1)
        end
    end
end

function update(dt)
    if gameState == "active" then
        SpawnParticle(Vec(0, 10, 0), Vec(0, -1, 0), zoneRadius * 0.01)
    end
end

function draw(dt)
    UiPush()
    UiAlign("center top")
    UiTranslate(UiCenter(), 40)
    if gameState == "waiting" then
        UiText("Press E to start")
    elseif gameState == "countdown" then
        UiFont("bold.ttf", 48)
        UiText(tostring(math.ceil(timer)))
    elseif gameState == "active" then
        UiText("Zone: " .. math.floor(zoneRadius) .. "m")
        UiTranslate(0, 30)
        UiText("Health: " .. math.floor(GetPlayerHealth() * 100) .. "%")
    elseif gameState == "dead" then
        UiFont("bold.ttf", 36)
        UiText("ELIMINATED")
    end
    UiPop()
end
