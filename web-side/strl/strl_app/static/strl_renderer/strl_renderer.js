const STATE_STOP = 0
const STATE_RUN = 1

var debug = false
var state = STATE_STOP
//var robot = canvas.image("strl_app/media/pictures/turtlebot100px.png", 50, 50)
document.getElementById('btnStop').disabled = true


var scene = []

function setup(){
	var canvas = createCanvas(document.getElementById('canvas-container').clientWidth-5,
								document.getElementById('canvas-container').clientHeight-5)
	canvas.parent('canvas-container')
	noLoop()
}
function draw(){
	background(color(255, 255, 255))
	translate(0,0)
	for (var i = 0; i < scene.length; i++){
		var obj = scene[i]
		obj.a = - obj.a // to ?
		
		//transform apply
		translate(obj.x, 600-obj.y)
		rotate(obj.a)
		if (obj.id == 1){
			fill(color(255,255,255,100))
			stroke(color(0,255,0,255))
			ellipse(0, 0, obj.r*2, obj.r*2)
			stroke(color(0,0,255,255))
			line(0, 0, obj.r, 0)
		}
		if (obj.id == 2){
			fill(color(255,255,255,100))
			stroke(color(0,255,0,255))
			obj.h = obj.h * 2
			rect(-obj.w / 2.0, -obj.h / 2.0, obj.w , obj.h )
			stroke(color(0,0,255,255))
			line(0, 0, obj.w / 2.0, 0)
		}
		//transform reset
		rotate(-obj.a)
		translate(-obj.x, -(600-obj.y))
	}

}

function clean_out(){
	background(color(255, 255, 255))
}

var ros
var world_properties


//$(document).bind('keypress',pressed);
$('#btnStart').bind('click',initE)
$('#btnStop').bind('click',stopE)

function initE()
{
	document.getElementById('btnStop').disabled = false
	document.getElementById('btnStart').disabled = true

	// Creating a ros connection
	ros = new ROSLIB.Ros({
			url: 'ws://localhost:9090'
	});


	ros.on('connection', function() {
			console.log('Connected to websocket server.');
	});

	ros.on('error', function(error) {
		console.log('Error connecting to websocket server: ', error);
	});

	ros.on('close', function() {
		console.log('Closed ros server')
	});


	// Publishing the topic 
	var create_world = new ROSLIB.Topic({
		ros: ros,
		name: '/create_world',
		messageType: 'std_msgs/String'
	});
	var world_id_message = new ROSLIB.Message({data: '{"id": "1","world": {"gravity": -900,"objects": {"robots": [{"env": {"x": 10,"y": 10,"r": 15,"a": 0.9}}]}}}'
	});

	create_world.publish(world_id_message)

	// Subscribing to the Topic
	world_properties = new ROSLIB.Topic({
		ros: ros,
		name: '/world/1/env/world_properties',
		messageType: 'std_msgs/String'
	});

	world_properties.subscribe(function(msg) {
		scene = JSON.parse(msg.data).properties
		redraw()
	});
	 state = STATE_RUN
}

function stopE()
{
	var destroy_world = new ROSLIB.Topic({
		ros: ros,
		name: '/destroy_world',
		messageType: 'std_msgs/String'
	});

	var world_id_message = new ROSLIB.Message({data: '1'});

	destroy_world.publish(world_id_message)

	world_properties.unsubscribe()

	// disconnection
	ros.close()

	// clean_out()

	document.getElementById('btnStop').disabled = true
	document.getElementById('btnStart').disabled = false
}

