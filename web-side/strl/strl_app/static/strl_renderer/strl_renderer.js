var canvas = SVG('canvas').size('100%', '100%')
//var robot = canvas.image("strl_app/media/pictures/turtlebot100px.png", 50, 50)
function CreateRobot(sx,sy,angle, rad)
{
    var robot = {
        x: sx,
        y: sy,
        r: rad,
        cx: rad / 2.0,
        cy: rad / 2.0,
        a: angle,
        img: canvas.circle(rad),
    }

    return robot
}


var robots = []





//$(document).bind('keypress',pressed);
$('#btnStart').bind('click',initE)

function initE()
{
    console.log("initE")
    var xhr = new XMLHttpRequest()
    xhr.open('GET', 'start', true)

    xhr.addEventListener('readystatechange', function(){
        if ((xhr.readyState==4)&&(xhr.status == 200)){
            console.log('Симуляция началась а ярослав пидр')
            setTimeout(timer, 33)
        }
        else{
            console.log(xhr.readyState)
        }

    })
    xhr.send() // !!!!!!!!!!!!!!!!!!!!!!!!!!!!

}
var data


function coordrequest()
{
    /*var xhr = new XMLHttpRequest()
    xhr.open('GET', 'properties', false)
    xhr.send()
    if (xhr.status != 200){
        alert(xhr.status + ': ' + xhr.statusText )

    }
    else{
        var data = JSON.parse(xhr.responseText)
        console.log(data)

    }*/
    var xhr = new XMLHttpRequest()
    xhr.open('GET', 'properties', true)
    xhr.addEventListener('readystatechange', function(){
        if ((xhr.readyState==4)&&(xhr.status == 200)){
            console.log('Данные получены')

            data = JSON.parse(xhr.responseText)
            console.log(data)
            //console.log(data)
            robots_recreate()

        }
        else
        {

           // console.log(xhr.readyState)
            if (xhr.readyState==2){
                console.log("Запрос отправлен")

            }
            if (xhr.readyState==3){
                console.log("Обработка на сервере")
            }
        }

    })
    xhr.send()
}

function timer()
{
    coordrequest()
    setTimeout(timer, 33)
}

function robots_clear()
{
    for(var i = 0; i < robots.length; i++){
        robots[i].img.remove()
        delete robots[i]
    }
    robots = []
}

function robots_create(data)
{
     for (var i = 0; i < data.length; i++){
        var robot_ns = data[i]
        robots[i] = CreateRobot(robot_ns.x, robot_ns.y, robot_ns.a, robot_ns.r)

        console.log(robots[i])
        robot_update(i)
    }
}

function robots_update()
{
    for (var i = 0; i < robots.length; i++){
        robot_update(i)
    }
}

function robots_recreate()
{
    robots_clear()
    robots_create(data)
    robots_update()

}

function robot_update(index)
{
    //console.log(robot.x(), " ", robot.y())
    robots[index].img.rotate(robots[index].a, robots[index].img.cx(), robots[index].img.cy())
    robots[index].img.x(robots[index].x - robots[index].cx)
    robots[index].img.y(robots[index].y - robots[index].cy)
}

/*function pressed(e)
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
    robot.x += dx
    robot.y += dy

    if(e.keyCode == 101)
    {
        robot.a += 5
    }
    if(e.keyCode == 113)
    {
        robot.a -= 5
    }
    robot_update()

}*/