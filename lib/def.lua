-- @lint-ok-file MISSING-VERSION2
-- @lint-ok-file PLAYERS-NO-INCLUDE
-- @lint-ok-file VARIABLE-KEY-PLAYER
-- @lint-ok-file HANDLE-GT-ZERO
----------------------------------------------------------------
-- Desync Exterminator Framework (DEF) v1.2
-- One #include. Zero desync. Every tool mod, done right.
--
-- ARCHITECTURE: All server/client callbacks are at the TOP LEVEL
-- of this file (not inside functions) so the v2 preprocessor
-- safely extracts them. DEF.Tool() only stores config — callbacks
-- iterate over DEF._tools at runtime via globals.
--
-- Usage:
--   #include "lib/def.lua"
--   tool = DEF.Tool("my-gun", {
--       displayName = "My Gun",
--       prefab = "MOD/vox/gun.vox",
--       group = 6,
--       ammoPickup = 30,
--       ammo = 100,
--   })
--   tool:PlayerData(function()
--       return { shootCooldown = 0, magazine = 10 }
--   end)
--   tool:ServerTick(function(p, data, dt)
--       -- game logic here
--   end)
--   tool:ClientTick(function(p, data, dt)
--       -- visuals here
--   end)
--   tool:Draw(function(p, data)
--       -- HUD here
--   end)
----------------------------------------------------------------

DEF = DEF or {}
DEF._VERSION = "1.2.0"
DEF._tools = {}
DEF._toolOrder = {}

----------------------------------------------------------------
-- TOOL: Registration + config (NO callback definitions here)
----------------------------------------------------------------

function DEF.Tool(toolId, config)
    assert(type(toolId) == "string", "DEF.Tool: toolId must be a string")
    assert(type(config) == "table", "DEF.Tool: config must be a table")

    local tool = {
        id = toolId,
        displayName = config.displayName or toolId,
        prefab = config.prefab or "",
        group = config.group or 6,
        ammoPickup = config.ammoPickup or 0,
        ammo = config.ammo or 100,

        _serverPlayers = {},
        _clientPlayers = {},
        _createPlayerData = nil,
        _serverInitFn = nil,
        _clientInitFn = nil,
        _serverTickFn = nil,
        _clientTickFn = nil,
        _drawFn = nil,
        _sounds = {},
        _animators = {},
    }

    DEF._tools[toolId] = tool
    DEF._toolOrder[#DEF._toolOrder + 1] = toolId

    function tool:PlayerData(factory) self._createPlayerData = factory end
    function tool:ServerInit(fn) self._serverInitFn = fn end
    function tool:ClientInit(fn) self._clientInitFn = fn end
    function tool:ServerTick(fn) self._serverTickFn = fn end
    function tool:ClientTick(fn) self._clientTickFn = fn end
    function tool:Draw(fn) self._drawFn = fn end

    function tool:InputPressed(action, p)
        if action == "usetool" then return InputPressed("usetool", p) end
        if p and IsPlayerLocal(p) then return InputPressed(action) end
        return false
    end

    function tool:InputDown(action, p)
        if action == "usetool" then return InputDown("usetool", p) end
        if p and IsPlayerLocal(p) then return InputDown(action) end
        return false
    end

    function tool:InputValue(action, p)
        if p and IsPlayerLocal(p) then return InputValue(action) end
        return 0
    end

    function tool:GetAim(p, muzzleOffset)
        local eye = GetPlayerEyeTransform(p)
        local offset = muzzleOffset or Vec(0.3, -0.2, -0.5)
        return {
            pos = TransformToParentPoint(eye, offset),
            dir = TransformToParentVec(eye, Vec(0, 0, -1)),
            eye = eye,
        }
    end

    function tool:Fire(pos, dir, config, p)
        Shoot(pos, dir,
            (config and config.bulletType) or "regular",
            (config and config.damage) or 10,
            (config and config.range) or 100,
            p, self.id)
    end

    function tool:LoadSound(path)
        local snd = LoadSound(path)
        self._sounds[path] = snd
        return snd
    end

    function tool:PlaySound(pathOrHandle, pos)
        local snd = pathOrHandle
        if type(pathOrHandle) == "string" then
            snd = self._sounds[pathOrHandle]
            if not snd then
                snd = LoadSound(pathOrHandle)
                self._sounds[pathOrHandle] = snd
            end
        end
        if snd and pos then PlaySound(snd, pos) end
    end

    function tool:TickTimer(data, field, dt)
        if data[field] and data[field] > 0 then
            data[field] = math.max(0, data[field] - dt)
        end
    end

    function tool:SyncToClient(key, value, p)
        local regKey = "def." .. self.id .. "." .. key .. "." .. tostring(p)
        if type(value) == "number" then
            if math.floor(value) == value then SetInt(regKey, value, true)
            else SetFloat(regKey, value, true) end
        elseif type(value) == "boolean" then SetBool(regKey, value, true)
        elseif type(value) == "string" then SetString(regKey, value, true) end
    end

    function tool:ReadSync(key, p, default)
        local regKey = "def." .. self.id .. "." .. key .. "." .. tostring(p)
        if HasKey(regKey) then
            if type(default) == "number" then
                if math.floor(default) == default then return GetInt(regKey)
                else return GetFloat(regKey) end
            elseif type(default) == "boolean" then return GetBool(regKey)
            elseif type(default) == "string" then return GetString(regKey) end
            return GetInt(regKey)
        end
        return default
    end

    function tool:IsEquipped(p) return GetPlayerTool(p) == self.id end

    return tool
end

function DEF.GetTool(id) return DEF._tools[id] end

----------------------------------------------------------------
-- TOP-LEVEL CALLBACKS — preprocessor-safe, no closures
-- Player iterators called ONCE per tick, results shared across tools
----------------------------------------------------------------

function server.init()
    for i = 1, #DEF._toolOrder do
        local tool = DEF._tools[DEF._toolOrder[i]]
        RegisterTool(tool.id, tool.displayName, tool.prefab, tool.group)
        if tool.ammoPickup ~= 0 then
            SetToolAmmoPickupAmount(tool.id, tool.ammoPickup)
        end
        SetString("game.tool." .. tool.id .. ".ammo.display", "")
        if tool._serverInitFn then tool._serverInitFn() end
    end
end

function server.tick(dt)
    -- Collect player events ONCE (iterators are consumed after one pass)
    local added = {}
    for p in PlayersAdded() do added[#added + 1] = p end
    local removed = {}
    for p in PlayersRemoved() do removed[#removed + 1] = p end
    local current = {}
    for p in Players() do current[#current + 1] = p end

    for i = 1, #DEF._toolOrder do
        local tool = DEF._tools[DEF._toolOrder[i]]

        for j = 1, #added do
            local p = added[j]
            local data = tool._createPlayerData and tool._createPlayerData() or {}
            tool._serverPlayers[p] = data
            SetToolEnabled(tool.id, true, p)
            SetToolAmmo(tool.id, tool.ammo, p)
        end

        for j = 1, #removed do
            tool._serverPlayers[removed[j]] = nil
        end

        for j = 1, #current do
            local p = current[j]
            local data = tool._serverPlayers[p]
            if data and tool._serverTickFn then
                tool._serverTickFn(p, data, dt)
            end
        end
    end
end

function client.init()
    for i = 1, #DEF._toolOrder do
        local tool = DEF._tools[DEF._toolOrder[i]]
        for path, _ in pairs(tool._sounds) do
            LoadSound(path)
        end
        if tool._clientInitFn then tool._clientInitFn() end
    end
end

function client.tick(dt)
    local added = {}
    for p in PlayersAdded() do added[#added + 1] = p end
    local removed = {}
    for p in PlayersRemoved() do removed[#removed + 1] = p end
    local current = {}
    for p in Players() do current[#current + 1] = p end

    for i = 1, #DEF._toolOrder do
        local tool = DEF._tools[DEF._toolOrder[i]]

        for j = 1, #added do
            local p = added[j]
            local data = tool._createPlayerData and tool._createPlayerData() or {}
            tool._clientPlayers[p] = data
            tool._animators[p] = ToolAnimator()
        end

        for j = 1, #removed do
            local p = removed[j]
            tool._clientPlayers[p] = nil
            tool._animators[p] = nil
        end

        -- ToolAnimator for ALL players (not just local)
        for j = 1, #current do
            local p = current[j]
            if tool:IsEquipped(p) and tool._animators[p] then
                tickToolAnimator(tool._animators[p], dt, nil, p)
            end
        end

        -- User client tick
        for j = 1, #current do
            local p = current[j]
            local data = tool._clientPlayers[p]
            if data and tool._clientTickFn then
                tool._clientTickFn(p, data, dt)
            end
        end
    end
end

function client.draw()
    local p = GetLocalPlayer()
    if not p then return end
    for i = 1, #DEF._toolOrder do
        local tool = DEF._tools[DEF._toolOrder[i]]
        if tool:IsEquipped(p) and tool._drawFn then
            local data = tool._clientPlayers[p]
            if data then
                tool._drawFn(p, data)
            end
        end
    end
end
