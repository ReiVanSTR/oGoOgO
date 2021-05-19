local ApiCommunicator = {}
ApiCommunicator['version'] = "1.0"

local json = require('json')

local config = {}
	config.url = {}
	url['addUser'] = 'http://ivangooder.pythonanywhere.com/addUser?user=%s',
	url['getUser'] = 'http://ivangooder.pythonanywhere.com/getUser?user=%s',
	url['updateStatus'] = 'http://ivangooder.pythonanywhere.com/updateStatus?user=%s',
	url['removeUser'] = 'http://ivangooder.pythonanywhere.com/removeUser?user=%s&reason=%s'

	config.injectionWords = {'SELECT','FROM','WHERE','OR','AND','DROP','TABLE'}
	config.injectionChars = {'(',')','=',';'}

function ApiCommunicator:init(config)
	objects = {}
	objects.config = config

	function objects:checkOnInjection(str)
		
	end

	setmetatable(self, objects)
	self.__init = self
	return objects
end

function ApiCommunicator:version()
	return self.version()
end

return ApiCommunicator