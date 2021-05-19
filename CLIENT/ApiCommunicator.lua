local ApiCommunicator = {}
ApiCommunicator['version'] = "1.0"

local json = require('json')
local text = require('text')
local internet = require('internet')

local config = {}
	config.url = {}
	config.url['addUser'] = 'http://ivangooder.pythonanywhere.com/addUser?user=%s'
	config.url['getUser'] = 'http://ivangooder.pythonanywhere.com/getUser?user=%s'
	config.url['updateStatus'] = 'http://ivangooder.pythonanywhere.com/updateStatus?user=%s'
	config.url['removeUser'] = 'http://ivangooder.pythonanywhere.com/removeUser?user=%s&reason=%s'

	config.injectionWords = {'SELECT','FROM','WHERE','OR','AND','DROP','TABLE'}
	config.injectionChars = {'=',';'}

function ApiCommunicator:init()
	objects = {}

	function isInjected(str)
		if type(str) == 'string' then
			for _, word in pairs(config.injectionWords) do
				if string.find(string.upper(str), word) then return true end
			end
			for _, char in pairs(config.injectionChars) do
				if string.find(string.upper(str), char) then return true end
			end
			return false
		end
	end

	function objects:checkOnInjection(str)
		local parts = text.tokenize(str)
		for _, pair in pairs(parts) do
			if isInjected(pair) then return true end
		end
		return false
	end

	function objects:getUser(user)
		if not self:checkOnInjection(user) then
			for response in internet.request(string.format(config.url['getUser'], user)) do
				if response then
					return json.decode(response[1])
				end
			end
			return false
		else
			return "Tryed to inject!"
		end
	end


	setmetatable(self, objects)
	self.__init = self
	return objects
end

function ApiCommunicator:version()
	return self.version()
end

return ApiCommunicator