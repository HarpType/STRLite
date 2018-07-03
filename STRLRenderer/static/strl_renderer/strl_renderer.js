var canvas = SVG('canvas').size('100%', '100%')
var robot = canvas.image('static/pictures/turtlebot100px.png', 50, 50)
//var robot = canvas.rect(50,50)
var robot_angle = 0.0
var robot_coord_x = 10.0
var robot_coord_y = 10.0
var center_x = 0
var center_y = 0


$(document).bind('keypress',pressed);
$('#btnStart').bind('click',coordrequest)

function coordrequest()
{
    var xhr = new XMLHttpRequest()
    xhr.open('GET', 'properties', false)
    xhr.send()
    if (xhr.status != 200){
        alert(xhr.status + ': ' + xhr.statusText )
        
    }
    else{
        var data = JSON.parse(xhr.responseText)
        console.log(data)
        
    }
}

function robot_update()
{    
    console.log(robot.x(), " ", robot.y())
    robot.rotate(robot_angle, robot.cx(), robot.cy())
    robot.x(robot_coord_x)
    robot.y(robot_coord_y)
}

function pressed(e)
{
    var dx = 0
    var dy = 0
    console.log("keypressed: ", e.keyCode)
    if(e.keyCode == 100)
    {
        dx = 5  
    }
    if(e.keyCode == 97)
    {
        dx = -5
    }
    if(e.keyCode == 115)  
    {
        dy = 5   
    }
    if(e.keyCode == 119)
    {
        dy = -5
    }
    robot_coord_x += dx
    robot_coord_y += dy
    
    if(e.keyCode == 101)
    {
        robot_angle += 5  
    }
    if(e.keyCode == 113)
    {
        robot_angle -= 5  
    }
    robot_update()
    
    
    
    
}
robot_update()