local vehicleBody = nil
local speed = 0

function init()
    vehicleBody = FindBody("monstertruck", true)
end

function tick(dt)
    local vehicle = GetPlayerVehicle()
    if vehicle ~= 0 then
        if InputDown("up") then
            speed = math.min(speed + dt * 10, 100)
        else
            speed = speed * 0.95
        end
        local t = GetVehicleTransform(vehicle)
        local fwd = TransformToParentVec(t, Vec(0, 0, -1))
        SetBodyVelocity(GetVehicleBody(vehicle), VecScale(fwd, speed))
    end
end

function update(dt)
    if speed > 50 then
        local t = GetPlayerTransform()
        SpawnParticle(t.pos, Vec(0, 0.2, 0), 0.5)
    end
end

function draw(dt)
    UiPush()
    UiAlign("left top")
    UiTranslate(20, 20)
    UiText("Speed: " .. math.floor(speed) .. " km/h")
    UiPop()
end
