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
        obj.a = obj.a * (1.0/180.0 * 3.14159 ) // to radian
        obj.a = - obj.a // to ?
        //transform apply
        translate(obj.x, obj.y)
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
            rect(-obj.w / 2.0, -obj.h / 2.0, obj.w , obj.h )
            stroke(color(0,0,255,255))
            line(0, 0, obj.w / 2.0, 0)
        }
        //transform reset
        rotate(-obj.a)
        translate(-obj.x, -obj.y)
    }

}


var debug = false
document.getElementById('btnStop').disabled = true
const STATE_STOP = 0
const STATE_RUN = 1
var state = STATE_RUN



var scene = []



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

function coordrequest()
{
    var xhr = new XMLHttpRequest()
    xhr.open('GET', 'properties', true)
    xhr.addEventListener('readystatechange', function(){
        if ((xhr.readyState==4)&&(xhr.status == 200)){
            if (debug)
                console.log('Данные получены')
            
            scene = JSON.parse(xhr.responseText)
            console.log(scene)
            redraw()

            
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

$('#btnStart').bind('click',timer)
$('#btnStop').bind('click',stopE)
