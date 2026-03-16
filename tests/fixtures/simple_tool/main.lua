local toolActive = false
local charge = 0

function init()
    RegisterTool("lasercutter", "Laser Cutter", "MOD/vox/laser.vox")
    SetBool("game.tool.lasercutter.enabled", true)
end

function tick(dt)
    if InputPressed("lmb") then
        toolActive = true
    end
    if InputReleased("lmb") then
        toolActive = false
        charge = 0
    end
    if toolActive then
        charge = charge + dt
        if charge > 1.0 then
            local t = GetPlayerTransform()
            local dir = TransformToParentVec(t, Vec(0, 0, -1))
            local hit, dist = QueryRaycast(t.pos, dir, 50)
            if hit then
                MakeHole(VecAdd(t.pos, VecScale(dir, dist)), 0.5, 0.5, 0.5)
                PlaySound(laserSound)
            end
        end
    end
end

function update(dt)
    if toolActive then
        SpawnParticle(GetPlayerTransform().pos, Vec(0, 0.5, 0), 0.3)
    end
end

function draw(dt)
    UiPush()
    UiAlign("center middle")
    UiTranslate(UiCenter(), UiMiddle())
    if toolActive then
        UiText("Charge: " .. math.floor(charge * 100) .. "%")
    end
    UiPop()
end
