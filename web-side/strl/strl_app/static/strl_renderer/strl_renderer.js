//For getting CSRF token
function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
           var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
         }
      }
  }
 return cookieValue
}

var world_id = -1
const STATE_STOP = 0
const STATE_RUN = 1

var debug = false
var state = STATE_STOP
//var robot = canvas.image("strl_app/media/pictures/turtlebot100px.png", 50, 50)
document.getElementById('btnStop').disabled = true
var co_name = ""
var co = "none"


var scene = []

function setup(){
	var height = document.getElementById('canvas_container').clientHeight
	var width = document.getElementById('canvas_container').clientWidth+11
	var canvas = createCanvas(document.getElementById('canvas_container').clientWidth+11,
								document.getElementById('canvas_container').clientHeight)
	canvas.parent('canvas_container')
	loop()
}
function draw(){
	
	background(color(255, 255, 255))
	const xy_step_inc = 20
	stroke(color(150,150,150,50))
	for (var x = -100; x <= width + 100; x += xy_step_inc){
		line(x,0,x,height-1)
	}
	for (var y = -100; y <= height + 100; y += xy_step_inc){
		line(0,y,width-1,y)
	}


	for (var i = 0; i < scene.length; i++){
		var obj = scene[i]
		SceneObject_Render(obj)
	}
	if (keyIsDown ( 87)){
		co.y += move_speed		
	}
	if (keyIsDown ( 83)){
		co.y -= move_speed		
	}
	if (keyIsDown ( 65)){
		co.x -= move_speed		
	}
	if (keyIsDown ( 68)){
		co.x += move_speed		
	}
	if (keyIsDown ( 81)){
		co.a += -rotate_speed		
	}
	if (keyIsDown ( 69)){
		co.a -= -rotate_speed		
	}
		
	

}

function SceneObject_Render(obj)
{
    
    resetMatrix()    	
    //transform apply
    translate(obj.x, 600-obj.y)
    rotate(obj.a)
    if (obj.id == 1){
        fill(color(0,0,0,15))
        if (co_name == obj.name){
	        stroke(color(0,255,0,255))	        
        }
	    else
	    	stroke(color(50,50,50,255))
        ellipse(0, 0, obj.r*2, obj.r*2)
        stroke(color(0,0,255,255))
        line(0, 0, obj.r, 0)
    }
    if (obj.id == 2){
        fill(color(0,0,0,15))
        if (co_name == obj.name){
	        stroke(color(0,255,0,255))	        
        }
	    else
	    	stroke(color(50,50,50,255))
        
        rect(-obj.w / 2.0, -obj.h / 2.0, obj.w , obj.h )
        stroke(color(0,0,255,255))
        line(0, 0, obj.w / 2.0, 0)
    }
    //transform reset
  //  rotate(-obj.a)
  //  translate(-obj.x, -(600-obj.y))
}

function clean_out(){
	background(color(255, 255, 255))
}

var ros
var world_properties

function correct_angle(){
	for (var i = 0; i < scene.length; i++){
		var obj = scene[i]
		obj.a = - obj.a
		if (obj.id == 2)
			obj.h = obj.h * 2
	}
}

//$(document).bind('keypress',pressed);
$('#btnStart').bind('click',initE)
$('#btnStop').bind('click',stopE)


function create_init_data(){
	var data = {}
	data.id = world_id.toString()
	data.world = {}
	var world = data.world
	world.space_options = {
		'gravity': -900
	}
	world.objects = {}
	var objects = world.objects
	objects.robots = []
	objects.walls = []
	for (var i = 0; i < scene.length; i++){
		if (scene[i].id == 1){
			objects.robots.push({
				'x': scene[i].x,
				'y': scene[i].y,
				'r': scene[i].r,
				'a': scene[i].a,
			})
		}
		if (scene[i].id == 2){
			objects.walls.push({
				'x': scene[i].x,
				'y': scene[i].y,
				'w': scene[i].w,
				'h': scene[i].h,
				'a': scene[i].a,
			})
		}
	}
	return data
}

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

	var world_id_message = new ROSLIB.Message({data: JSON.stringify(create_init_data())});

	create_world.publish(world_id_message)

	// Subscribing to the Topic
	world_properties = new ROSLIB.Topic({
		ros: ros,
		name: '/world/1/env/world_properties',
		messageType: 'std_msgs/String'
	});

	world_properties.subscribe(function(msg) {
		var data = JSON.parse(msg.data).world
		console.log(data)
		scene = []
		for (var i = 0; i < data.objects.robots.length; i++){
			data.objects.robots[i].id = 1
			scene.push(data.objects.robots[i])
		}
		for (var i = 0; i < data.objects.walls.length; i++){
			data.objects.walls[i].id = 2
			scene.push(data.objects.walls[i])
		}
		correct_angle()
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


////////////////////////////////////////////////////
var scene_list = document.getElementById('scene_list')
function add_to_scene_list(s){
	scene_list.options[scene_list.options.length] = new Option(s, s)
}


function SceneObject_Create(x, y, w, h, a){ // создание базового объекта
    var so = {}
    so.x = x
    so.y = y
    so.w = w
    so.h = h
    so.a = a

    return so
}


function Circle_Create(x,y,r){ // создание круга
    var c = SceneObject_Create(x,y,r*2,r*2,0.0)
    c.r = r
   c.id = 1

    return c
}

function Box_Create(x,y,w,h){ // создание прямоугольника
    var c = SceneObject_Create(x,y,w,h,0.0)
    c.w = w
    c.h = h
    c.id = 2
    return c
}

function select_so(){ // выбор объекта
	for (var i = 0; i < scene.length; i++){
		var obj = scene[i]
		if (obj.name == co_name){
			co = obj
			console.log('selected!')
		}
	}
}

function btnCreateCircle_click() // обработчик кнопки создания круга
{
	var circle_name = prompt('Введите название круга: ')
	if (circle_name == null)
		return;
	var circle_radius = parseInt(prompt('Введите радиус круга: ', '5'))
	add_to_scene_list(circle_name)
	var circle = Circle_Create(300,300,circle_radius)
	circle.name = circle_name 
    scene.push(circle)
    redraw()
    console.log(scene.length)

}

function btnCreateBox_click()// обработчик кнопки создания прямоугольника
{
	var box_name = prompt('Введите название прямоугольника: ')
	if (box_name == null)
		return;
	var box_w = parseInt(prompt('Введите ширину прямоугольника: ', '5'))
	if (box_w == null)
		return;
	var box_h = parseInt(prompt('Введите высоту прямоугольника: ', '5'))
	if (box_h == null)
		return;
	add_to_scene_list(box_name)
	var box = Box_Create(300,300,box_w, box_h)
	box.name = box_name 
    scene.push(box)
    redraw()
    console.log(scene.length)

}


$('#btnCreateCircle').bind('click', btnCreateCircle_click)
$('#btnCreateBox').bind('click', btnCreateBox_click)
$('#scene_list').on('change', function (){
	co_name = this.value
	console.log('Selected: ', co_name)
	select_so()

})
const move_speed = 2.0
const rotate_speed = 2.0 * (1.0 / 180.0) * 3.14159

function keyPressed(){
	var ki = key.charCodeAt(0) // ki - key index
	console.log('Code: ', ki)
	if (ki == 46){
		if (co_name != ""){
			for (var i = 0; i < scene.length; i++){
				if (scene[i] == co){
					scene.splice(i,1)
					delete co;
					var x = document.getElementById("scene_list");
					x.remove(x.selectedIndex);
					redraw()	
					break
				}
			}
			


		}
	}
	

}

function btnSave_click(){ // сохранение
	/*var xhr = new XMLHttpRequest();
	xhr.open('POST', 'create', true);
	xhr.onreadystatechange = function() { // (3)
	  if (xhr.readyState != 4) return; 

	  if (xhr.status != 200) {
	    alert(xhr.status + ': ' + xhr.statusText);
	  }
	  else{
	  	console.log('Успешно сохранено')
	  }

	}


	xhr.send("Hello"); // (1)*/
	var d = create_init_data()
	console.log(d)

	document.getElementById('loading').style.visibility="visible";
	console.log(scene)
    var csrftoken = getCookie('csrftoken');
	$.ajax({
           url : "/editor/save/", // the endpoint,commonly same url
           type : "POST", // http method
           data : { csrfmiddlewaretoken : csrftoken,
                    scene : JSON.stringify(scene),
         }, // data sent with the post request

         // handle a successful response
         success : function(json) {
            console.log('response ok')
            document.getElementById('loading').style.visibility="hidden";
         },

         // handle a non-successful response
         error : function(xhr,errmsg,err) {
         console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
         document.getElementById('loading').style.visibility="hidden";
         }
     });
}
$('#btnSave').bind('click',btnSave_click)

/*
function mousePressed(){
	if (co != 'none'){
		co.x = mouseX
		co.y = 600-mouseY
	}
}
*/
///////////////////SCENE-TREE

function loadWorld() // загрузка мира из БД после загрузки страницы редактора
{
	
    var csrftoken = getCookie('csrftoken');
	$.ajax({
           url : "/editor/", // the endpoint,commonly same url
           type : "POST", // http method
           data : { csrfmiddlewaretoken : csrftoken
                    
         }, // data sent with the post request

         // handle a successful response
         success : function(json) {
         	//console.log(json)
         	var data = JSON.parse(json)
         	world_id = data.id
         	console.log("World id: ", world_id)
         	scene = data.scene
         	for (var i = 0; i < scene.length; i++){
         		add_to_scene_list(scene[i].name)

         	}
           // console.log('Worlds json: ', data)
            document.getElementById('loading').style.visibility="hidden";
            /*setTimeout(function(){
		         
		         document.getElementById('loading').style.visibility="hidden";
		      },1000);*/

         },

         // handle a non-successful response
         error : function(xhr,errmsg,err) {
         	console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
         	document.getElementById('loading').style.visibility="hidden";
         }
     });
}

/*document.onreadystatechange = function () {
  var state = document.readyState
  if (state == 'complete') {
      setTimeout(function(){
         
         document.getElementById('loading').style.visibility="hidden";
      },1000);
  }
}*/

loadWorld()