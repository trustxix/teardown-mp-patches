#version 2

function server.init()
    RegisterTool("mptool", "MP Tool", "MOD/vox/tool.vox")
end

function client.draw()
    UiText("MP Ready!")
end
