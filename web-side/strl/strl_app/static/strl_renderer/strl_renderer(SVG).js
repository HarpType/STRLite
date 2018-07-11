const STATE_STOP = 0
const STATE_RUN = 1
var canvas = SVG('canvas').size('100%', '100%') //кансвас на котором будем создавать объекты
var debug = false
var state = STATE_STOP
var cso = 0 //Current Selected Object
//var robot = canvas.image("strl_app/media/pictures/turtlebot100px.png", 50, 50)
document.getElementById('btnStop').disabled = true
function CreateCircle(sx,sy,angle, rad)
{
    var circle = {
        type: 'circle',
        x: sx,
        y: sy,
        r: rad,
        cx: rad,
        cy: rad,
        a: angle,
        img: canvas.circle(2*rad),

    }   
    circle.img.attr({
        'fill': '#fff'
    })
    circle.dir = canvas.line(circle.cx, circle.cy,  rad*2, circle.cy).stroke({width: 1})
    circle.dir.attr({
        'stroke': '#00f'
    })
    circle.img.stroke({
        width: 1,
        color: '#0f0'
    })

    return circle
}

function CreateBox(sx,sy,angle, w, h)
{
    var box = {
        type: 'box',
        x: sx,
        y: sy,
        w: w,
        h: h,
        cx: w / 2.0,
        cy: h / 2.0,
        a: angle,
        img: canvas.rect(w,h),

    }   
    box.img.attr({
        'fill': '#fff'
    })
    box.dir = canvas.line(box.cx, box.cy,  box.w, box.cy).stroke({width: 1})
    box.dir.attr({
        'stroke': '#00f'
    })
    box.img.stroke({
        width: 1,
        color: '#0f0'
    })

    return box
}


var scene = []

function btn_create_circle()
{
    CreateCircle($('#canvas').width() / 2.0, $('#canvas').height() / 2.0, )
}



//$(document).bind('keypress',pressed);
$('#btnStart').bind('click',initE)
$('#btnStop').bind('click',stopE)

function initE()
{
    document.getElementById('btnStop').disabled = false
    document.getElementById('btnStart').disabled = true
    var xhr = new XMLHttpRequest()
    xhr.open('GET', 'start', true)
    xhr.addEventListener('readystatechange', function(){
        if ((xhr.readyState==4)&&(xhr.status == 200)){
            data = JSON.parse(xhr.responseText)
            if (data.st == "ready"){
                console.log('Симуляция началась ')
                state = STATE_RUN
                setTimeout(timer, 33)
                document.getElementById('btnStop').disabled = false
                document.getElementById('btnStart').disabled = true
                
            }
            else{
                alert("Ошибка инициализации: ", data.st)
                document.getElementById('btnStop').disabled = true
                document.getElementById('btnStart').disabled = false

            }
        }
        else{
            console.log(xhr.readyState)
            state = STATE_STOP
        }

    })
    xhr.send()
        
}

function stopE()
{
    state = STATE_STOP
    var xhr = new XMLHttpRequest()
    xhr.open('GET', 'stop', true)
    document.getElementById('btnStop').disabled = true
    document.getElementById('btnStart').disabled = false
    xhr.addEventListener('readystatechange', function(){
        if ((xhr.readyState==4)&&(xhr.status == 200)){

            console.log('Симуляция становлена ')
            
            document.getElementById('btnStop').disabled = true
            document.getElementById('btnStart').disabled = false
            
        }
        else{
            console.log(xhr.readyState)
            
        }

    })
    xhr.send()
        
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
            if (debug)
                console.log('Данные получены')
            
            data = JSON.parse(xhr.responseText)
            //console.log(data)
            scene_recreate()
            
        }   
        else
        {

           // console.log(xhr.readyState)
            if (xhr.readyState==2){
                if (debug)
                    console.log("Запрос отправлен")

            }
            if (xhr.readyState==3){
                if (debug)
                    console.log("Обработка на сервере")                
            }
            
        }

    })
    xhr.send()
}

function timer()
{
    if (state == STATE_RUN){
        coordrequest()
        setTimeout(timer, 33)
    }

}

function scene_clear()
{
    for(var i = 0; i < scene.length; i++){
        scene[i].img.remove()
        scene[i].dir.remove()
        delete scene[i]
    }
    scene = []
}

function scene_create(data)
{
     for (var i = 0; i < data.length; i++){
        var info = data[i]
        if (info.id == 1){
            scene[i] = CreateCircle(info.x, info.y, info.a, info.r) 
        }
        if (info.id == 2){
            scene[i] = CreateBox(info.x, info.y, info.a, info.w, info.h) 
            
        }

        
        //console.log(robots[i])              
        scene_update(i)
    }
}

function scene_update()
{
    for (var i = 0; i < scene.length; i++){
        object_update(i)
    }
}

function scene_recreate()
{
    scene_clear()
    scene_create(data)
    scene_update()

}

function object_update(index)
{
    //console.log(robot.x(), " ", robot.y())
    //scene[index].img.rotate(scene[index].a, scene[index].img.cx(), scene[index].img.cy())
    scene[index].img.x(scene[index].x - scene[index].cx)
    scene[index].img.y(scene[index].y - scene[index].cy)
    scene[index].img.rotate(scene[index].a, scene[index].img.cx(), scene[index].img.cy())


    scene[index].dir.x(scene[index].x )
    scene[index].dir.y(scene[index].y )
    scene[index].dir.rotate(scene[index].a, scene[index].img.cx(), scene[index].img.cy())
}

function unselect()
{
    if (!(cso === 0)){
        cso.img.selectize(false)
        cso = 0
    }
}
$("#tools").bind("click", unselect)


var c = CreateCircle($('#canvas').innerWidth() / 2.0, $('#canvas').innerHeight() / 2.0, 0.0, 100)

c.img.selectize().resize({ snapToGrid: 5}).draggable()
c.img.on('click', function() {
    c.img.selectize(true)
    cso = c
})
c.img.on('dragmove', function(){
    console.log(c.img.x(), c.img.y())
    console.log(c.img.transform('x'), c.img.transform('y') )
    console.log(c.img.transform('cx'), c.img.transform('cy') )

   // c.x = c.img.attr('x')
    //c.y = c.img.attr('y')
    console.log('dragmove')
    //console.log(c.x, c.y, c.a)
  //  console.log(c.img.attr('cx'), c.img.attr('cy'), c.img.attr('rotation'))

  //  var x_t = c.img.transform().x
   // var y_t = c.img.transform().y
   // var a_t = c.img.transform().rotation

    var r = c.img.attr('r')
    var x = c.img.x() //+ x_t
    var y = c.img.y() //+ y_t
    var angle = c.img.transform('rotation')
   // console.log(x, y, angle)
   // console.log(x_t, y_t, a_t)
   // console.log("CX,CY:",c.img.attr('cx'), c.img.attr('cy'))
    c.a = angle
    //console.log(c.img.transform('rotation'))
    c.cx = r;
    c.cy = r;
    c.x = x + r
    c.y = y + r

    /*var r = c.img.attr('r')
    c.x = c.img.x() + r
    c.y = c.img.y() + r
    console.log("CXY DRAG:", c.x, c.y)*/

    scene_update()
})


c.img.on("resizing", function ()
{
    var x_t = c.img.transform().x
    var y_t = c.img.transform().y
    var a_t = c.img.transform().rotation
    var r = c.img.attr('r')
    var x = c.img.x()
    var y = c.img.y()
    var angle = c.img.transform('rotation')
    c.a = angle

    console.log('resizing')
    console.log(x, y, angle)
    console.log(x_t, y_t, a_t)

    c.cx = r;
    c.cy = r;
    c.x = x + r
    c.y = y + r

    var old_dir_x = c.dir.x()
    var old_dir_y = c.dir.y()
    var old_t = c.dir.transform()
    c.dir.remove()
    c.dir = canvas.line(r, r, r*2,r).stroke({width: 1})
    //c.dir.x(old_dir_x)
   // c.dir.y(old_dir_y)
   c.dir.transform(old_t)

   c.dir.attr({
       'stroke': '#00f'
   })
    scene_update()
})
scene.push(c)
scene_update()