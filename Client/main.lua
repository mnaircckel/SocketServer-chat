local socket = require "socket"
local address, port = "54.69.253.54", 3000
local utf8 = require "utf8"
local background, messages, font, text, data, msg, sent, chatroom_connection, awaiting_response, ping_timer

 function love.load()
 	love.window.setMode(639,379)
 	love.window.setTitle("LuaChat Client")
 	love.keyboard.setKeyRepeat(true)
	background = love.graphics.newImage('background.png')
	
	udp = socket.udp()
	udp:settimeout(0)
	udp:setpeername(address, port)
	udp:send("!n")
	udp:send("?u")

	font = love.graphics.newFont(18)
	text = ""
	messages = {}
	ping_timer = love.timer.getTime()
	chatroom_connection = true
	awaiting_response = false
end

function love.update(dt)
	data, msg = udp:receive()
	-- If there is data, add it to the messages client side, remove awaiting response, reset ping timer
	if data then
		awaiting_response = false
		chatroom_connection = true
		ping_timer = love.timer.getTime()
		if data ~= "?p" then
			if table.getn(messages) > 7 then
				table.remove(messages,1)
			end
			table.insert(messages,data)
		end
	end
	-- Ping server every 2 seconds to check if there is a connection
	if (love.timer.getTime()-ping_timer) > 2 then
		udp:send("?p")
		ping_timer = love.timer.getTime()
		if awaiting_response then
			chatroom_connection = false
			--> Attempt to reconnect to chat room
			udp = socket.udp()
			udp:settimeout(0)
			udp:setpeername(address, port)
			udp:send("!n")
			udp:send("?u")
		end
		awaiting_response = true
	end
end

function love.draw(dt)
	love.graphics.draw(background, 0, 0)
	love.graphics.setFont(font)
	love.graphics.setBackgroundColor( 100, 55, 200)
	love.graphics.print("LuaChat Client",8,5)
	local message_number = 0
	love.graphics.setColor(102, 255, 51)
	for key,message in pairs(messages) do
		message_number = message_number + 1
		love.graphics.print(message,8,message_number*30)
	end
	if chatroom_connection == false then
		love.graphics.setColor(255, 50, 50)
		love.graphics.print("Unable to establish connection...",8, 270)
	end
	love.graphics.setColor(102, 255, 51, 210)
	love.graphics.print(text,8,300)
	love.graphics.setColor(255,255,255)
end

function love.textinput(t)
    text = text .. t
end
 
function love.keypressed(key)
    if key == "backspace" then
        -- get the byte offset to the last UTF-8 character in the string.
        local byteoffset = utf8.offset(text, -1)
 
        if byteoffset then
            -- remove the last UTF-8 character.
            -- string.sub operates on bytes rather than UTF-8 characters, so we couldn't do string.sub(text, 1, -2).
            text = string.sub(text, 1, byteoffset - 1)
        end
    end
    if key == "return" then
    	udp:send("!m:" .. text)
    	text = ""
    end
end


function love.quit()
	udp:send("!q")
end