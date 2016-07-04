var ENTER_KEYCODE = 13;

var serverModule = function() {
	var module = {
		ip: '192.168.1.7',
		port: '8888'
	}
	module.init = function() {
		module.ws = new WebSocket('ws://' + module.ip + ':' + module.port + '/websocket');
	}
	module.send = function(o) {
		module.ws.send(o);
	}
	return module;
}

var textareaModule = function() {
	var module = {}
	var el = document.getElementById('area');
	module.write = function(val) {
		el.innerHTML = el.innerHTML + val + '\n';
	}
	module.error = function(val) {
		module.write("ERROR: " + val);
	}
	return module
}

window.addEventListener('load', function() {
	var server = serverModule();
	var textarea = textareaModule();
	textarea.write("Connecting to web socket.");
	// loaded the DOM, let's set up the websocket
	server.init();
	var ws = server.ws;
	ws.onerror = function(msg) {
		textarea.error("An error occurred.")
	}
	ws.onopen = function() {
		ws.send("Hello, world");
	}
	ws.onmessage = function(msg){
		textarea.write(msg.data)
	}
	// bind the submit / enter key
	var textField = document.getElementById('userinput');
	textField.onkeypress = function(e) {
		if (e.keyCode == ENTER_KEYCODE) {
			server.send(textField.value);
			textField.value = "";
		}
	}
}, false);
