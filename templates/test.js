

// Function to draw Inicio de ciclo
function draw_inicio_ciclo(canvas,ctx,x, y, size_x,size_y, radius, color) {
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.arcTo(x + size_x, y, x + size_x, y + size_y, 0);
    ctx.arcTo(x + size_x+size_x/4, y + size_y/2, x + size_x, y + size_y, 0);
    ctx.arcTo(x + size_x, y + size_y, x, y + size_y, 0);

    ctx.arcTo(x, y + size_y, x, y, radius);
    ctx.arcTo(x, y, x + size_x, y, radius);
    ctx.strokeStyle = "black";
    ctx.lineWidth = 1;
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.fill();
    ctx.closePath();
    ctx.stroke();
}

function draw_fin_ciclo(canvas,ctx,x, y, size_x,size_y, radius, color) {
    ctx.beginPath();
    ctx.moveTo(x , y);
    ctx.arcTo(x + size_x, y, x + size_x, y + size_y, radius);
    ctx.arcTo(x + size_x, y + size_y, x, y + size_y, radius);
    ctx.arcTo(x, y + size_y, x, y, 0);
    ctx.arcTo(x -size_x/4, y + size_y/2, x - size_x, y + size_y, 0);
    ctx.arcTo(x, y, x + size_x, y, 0);
    
    ctx.strokeStyle = "black";
    ctx.lineWidth = 1;
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.fill();
    ctx.closePath();
    ctx.stroke();
}

function draw_linea(canvas,ctx,x, y, size_x,size_y, color, grosor) {
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(size_x, size_y);
    ctx.lineWidth = grosor;
    ctx.strokeStyle = color;
    ctx.stroke();
}

// Circulos base
function draw_circulo(canvas,ctx,x,y,radio,color){
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.arc(x, y, radio, 0, 2 * Math.PI);
    ctx.lineWidth = 1;
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.fill();
    ctx.stroke();
}

function draw_circulos_en_linea(canvas,ctx,x, y, size_x,size_y,radio,color,cantidad_semanas, numero_semanas){
    for(let i=1;i<=numero_semanas;i++){
        let c = (size_x-x)/cantidad_semanas;
        draw_circulo(canvas,ctx,c * i + x - c/2, y+size_y*i/cantidad_semanas ,radio ,color);
    }
}

function draw_line_progreso(canvas,ctx,x, y, size_x,size_y,cantidad_semanas,numero_semanas,color){
    let c = (size_x - x)/cantidad_semanas;
    draw_linea(canvas,ctx,0, y, x + c*numero_semanas - c/2,size_y, color, 8) ;
}






function draw_cartel_porcentaje(canvas,ctx,x, y, size_x,size_y, radius, color) {
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.arcTo(x + size_x, y, x + size_x, y + size_y, radius);
    ctx.arcTo(x + size_x, y + size_y, x , y + size_y, radius);
    ctx.arcTo(x + size_x*4/6, y + size_y, x + size_x *4/6, y + size_y, radius);
    ctx.arcTo(x + size_x*3/6, y + size_y*5/4, x + size_x *3/6, y + size_y*5/4, 0);
    ctx.arcTo(x + size_x*2/6, y + size_y, x + size_x *2/6, y + size_y, 0);
    ctx.arcTo(x, y + size_y, x , y, radius);
    ctx.arcTo(x, y, x + size_x, y, radius);
    ctx.strokeStyle = "black";
    ctx.lineWidth = 1;
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.fill();
    ctx.closePath();
    ctx.stroke();
}

function number_format(number) {
    // Check if the number is less than 10
    if (number < 10) {
        // Add a leading zero and convert the number to a string
        return '0' + number.toString();
    } else {
        // Convert the number to a string
        return number.toString();
    }
}

function cartel_letras(canvas,ctx,size_x,size_y,cantidad_semanas,sememana,porcentaje,color){
    let a = 0 +size_x*5/4;
    let b = canvas.width-size_x*5/4;
    let c = (b-a)/cantidad_semanas;
    let cordenada_x = a + c*sememana - c/2;
    draw_cartel_porcentaje(canvas,ctx,cordenada_x - 65/2, canvas.height/10, 65,40, 5, color)
    draw_circulo(canvas,ctx,cordenada_x,canvas.height/2,13,color)
    
    // Letras cartel
    let font = new FontFace('Lato', 'url(https://fonts.gstatic.com/s/lato/v24/S6uyw4BMUTPHjxAwXjeu.woff2)');
    font.load().then(function(loadedFont) {
        // Use the loaded font
        document.fonts.add(loadedFont);
        ctx.fillStyle = "White";
        ctx.font = '24px Lato'; // Set the font size and family

        // Colocar Porcentaje
        let espaciado = 0;
        if(porcentaje/10<1){
            espaciado = 15;
        }else if(porcentaje/10<10){
            espaciado = 24;
        }else{
            espaciado = 31;
        }
        ctx.fillText(porcentaje.toString()+'%', cordenada_x - espaciado, canvas.height/10+28); // Draw the text

        // Colocar Semana
        ctx.fillStyle = "Black";
        ctx.fillText('Semana '+number_format(sememana), cordenada_x - 54, canvas.height*8/10); // Draw the text
        ctx.fillStyle = "White";
        ctx.fillText('Inicio de ciclo ', size_x/6-14, canvas.height/2+size_y/4-2); // Draw the text
        ctx.fillStyle = "Black";
        ctx.fillText('Fin de ciclo ', canvas.width-size_x, canvas.height/2+size_y/4-2); // Draw the text
        
        
    }).catch(function(error) {
        console.log('Font loading failed: ' + error);
    });

    ctx.font = '30px Lato'; // Set the font size and family
    ctx.fillStyle = "White";
    ctx.fillText(".", 0, 0);

}

function crea_graf(cantidad_semanas,sem,por,canvas_id){
    let canvas = document.getElementById(canvas_id);
    let ctx = canvas.getContext("2d");
    // Define the properties of the rounded square
    let squareSize_x = 150; // Size of the square
    let squareSize_y = 40; // Size of the square
    let cornerRadius = 5; // Radius of the corners
    let squareX_inicio = 0; // X coordinate of the square
    let squareY_inicio = (canvas.height/2 - squareSize_y/2); // Y coordinate of the square
    let squareX_fin = (canvas.width - squareSize_x); // X coordinate of the square
    let squareY_fin = (canvas.height/2 - squareSize_y/2); // Y coordinate of the square
    // Colores
    let color_inicio = "#00b491";
    let color_fin = "#b0cdff";
    // Draw the rounded square
    draw_linea(canvas,ctx,0, canvas.height/2, canvas.width,canvas.height/2, color_fin, 8)
    draw_inicio_ciclo(canvas,ctx,squareX_inicio, squareY_inicio, squareSize_x, squareSize_y, cornerRadius, color_inicio);
    draw_fin_ciclo(canvas,ctx,squareX_fin, squareY_fin, squareSize_x, squareSize_y, cornerRadius, color_fin);
    draw_circulos_en_linea(canvas,ctx,0+squareSize_x*5/4, canvas.height/2, canvas.width-squareSize_x*5/4,0,9,color_fin,cantidad_semanas,cantidad_semanas)
    draw_line_progreso(canvas,ctx,squareSize_x*5/4, canvas.height/2, canvas.width - squareSize_x*5/4,canvas.height/2,cantidad_semanas,sem,color_inicio)
    draw_circulos_en_linea(canvas,ctx,0+squareSize_x*5/4, canvas.height/2, canvas.width-squareSize_x*5/4,0,9,"#6fcf97",cantidad_semanas,sem)
    draw_circulos_en_linea(canvas,ctx,0+squareSize_x*5/4, canvas.height/2, canvas.width-squareSize_x*5/4,0,4,"white",cantidad_semanas,sem)
    cartel_letras(canvas,ctx,squareSize_x,squareSize_y,cantidad_semanas,sem,por,color_inicio)
}

function crea_canvas(div_id,sems,act){
    let canvas_tag = document.createElement('canvas');
    canvas_tag.width = 1200;
    canvas_tag.height = 200;
    canvas_tag.style = 'width: 100%; height: 100%;';
    canvas_tag.id = 'mi_barra_de_progreso';
    // Get the div element where you want to append the canvas
    let mi_div = document.getElementById(div_id);
    mi_div.innerHTML = "";
    mi_div.appendChild(canvas_tag);
    crea_graf(sems,act, Math.round(sem_por[1]/sem_por[0]*100),canvas_tag.id)
}


