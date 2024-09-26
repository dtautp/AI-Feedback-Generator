function copyFeedbackText(key) {
    // Selecciona el contenido del div
    var contenido = document.getElementById('feedbackText_' + key);
    contador_copy(key);
    // Verifica si el div tiene contenido
    if (contenido.innerText.trim() === '') {
        // Si no hay contenido, muestra un mensaje de alerta
        alert('No hay valores para copiar.');
        return;
    }

    // Crea un rango de selección
    var range = document.createRange();
    range.selectNodeContents(contenido);

    // Selecciona el contenido del div
    var selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);

    // Ejecuta el comando de copiar
    document.execCommand('copy');

    // Seselecciona el texto
    selection.removeAllRanges();

    // Notifica al usuario que se ha copiado el contenido
    // alert('¡Contenido copiado al portapapeles!');
    showBootstrapAlert('¡Contenido copiado al portapapeles!', 'success');
}

function showBootstrapAlert(message, alertType) {
    var alertContainer = document.getElementById('alertContainer');
    var alertId = 'alert-' + new Date().getTime();

    // Crea el div de alerta
    var alertDiv = document.createElement('div');
    alertDiv.id = alertId;
    alertDiv.className = 'alert alert-' + alertType + ' alert-dismissible fade show';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = message;

    // Añade la alerta al contenedor
    alertContainer.appendChild(alertDiv);

    // Auto cierra la alerta después de 3 segundos
    setTimeout(function() {
        var alertElement = document.getElementById(alertId);
        if (alertElement) {
            alertElement.classList.remove('show');
            alertElement.classList.add('fade');
            alertElement.addEventListener('transitionend', function() {
                alertElement.remove();
            });
        }
    }, 1000);
}

// Configurar el contador de selección al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    const totalSelections = document.querySelectorAll('.file_name').length;
    document.getElementById('selectionCounter').textContent = `1 de ${totalSelections}`;
});


function contador_copy(key){
    // console.log(key)
    const newData = {
        request_id: key,
    };

    // Options for the fetch request
    const options = {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newData)
    };

    // Make the API request
    fetch('contador_copiar', options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Display the updated response data
            // console.log(JSON.stringify(data));
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

const fileSelector = {
    currentSelectionIndex: 1,
    totalSelections: document.querySelectorAll('.file_name').length,
    updateSelection() {
        // Actualizar el contador de selección
        selectionCounter.textContent = `${this.currentSelectionIndex} de ${this.totalSelections}`;
        // Encuentra el botón correspondiente a la selección actual y simula su clic
        const currentButton = document.querySelector(`.file_name:nth-child(${this.currentSelectionIndex})`);
        currentButton.click();
        // Habilitar o deshabilitar el botón previo según sea necesario
        if (this.currentSelectionIndex === 1) {
            prevButton.disabled = true;
            prevButton.classList.add('disabled');
            prevButton.querySelector('img').src = '/static/img/back.svg'; // Cambiar la imagen
        } else {
            prevButton.disabled = false;
            prevButton.classList.remove('disabled');
            prevButton.querySelector('img').src = '/static/img/back-blue.svg'; // Restaurar la imagen original
        }
        // Habilitar o deshabilitar el botón siguiente según sea necesario
        if (this.currentSelectionIndex === this.totalSelections) {
            nextButton.disabled = true;
            nextButton.classList.add('disabled');
            nextButton.querySelector('img').src = '/static/img/back.svg';
        } else {
            nextButton.disabled = false;
            nextButton.classList.remove('disabled');
            nextButton.querySelector('img').src = '/static/img/back-blue.svg';
        }
    }
};

// Función para manejar el clic en el botón del archivo
function handleClick(event) {
    const button = event.currentTarget;
    
    // Quita la clase 'selected' de todos los botones
    document.querySelectorAll('.file_name').forEach(btn => {
        btn.classList.remove('selected');
    });

    // Agrega la clase 'selected' al botón seleccionado
    button.classList.add('selected');
    
    const buttonRect = button.getBoundingClientRect();
    const containerRect = scrollContainer.getBoundingClientRect();

    // Calcular el desplazamiento necesario para centrar el botón
    const scrollLeft = buttonRect.left - containerRect.left - (containerRect.width - buttonRect.width) / 2;
    // console.log(scrollLeft)
    
    // Desplazar el contenedor
    scrollContainer.scrollLeft += scrollLeft;
    
    // Actualizar el contador de selección
    fileSelector.currentSelectionIndex = Array.from(button.parentNode.children).indexOf(button) + 1;
    fileSelector.updateSelection();

    // Agregar la clase 'active' al contenido correspondiente
    // Agregar la clase 'active' solo al contenido correspondiente
    const contentId = button.getAttribute('id');
    document.querySelectorAll('.preview-content').forEach(elem => {
        elem.classList.remove('active');
        if (elem.id === contentId) {
            elem.classList.add('active');
        }
    });
}

const fileButtons = document.querySelectorAll('.file_name');
fileButtons.forEach(button => {
    button.addEventListener('click', handleClick);
});

const scrollContainer = document.getElementById('scrollContainer');

scrollContainer.addEventListener('wheel', (event) => {
    scrollContainer.scrollLeft += event.deltaY;
});

scrollContainer.addEventListener('scroll', () => {
    const buttons = document.querySelectorAll('.file_name');
    const lastButton = buttons[buttons.length - 1];
    const firstButton = buttons[0];
    const containerRect = scrollContainer.getBoundingClientRect();
    const lastButtonRect = lastButton.getBoundingClientRect();
    const firstButtonRect = firstButton.getBoundingClientRect();

    if (lastButtonRect.right < containerRect.right) {
        scrollContainer.insertBefore(lastButton, firstButton);
        scrollContainer.scrollLeft -= firstButtonRect.width;
    } else if (firstButtonRect.left > containerRect.left) {
        scrollContainer.appendChild(firstButton);
        scrollContainer.scrollLeft += firstButtonRect.width;
    }
});

const prevButton = document.getElementById('prevButton');
const nextButton = document.getElementById('nextButton');
const selectionCounter = document.getElementById('selectionCounter');

// Funciones de flecha para manejar el clic en los botones de selección anterior y siguiente
prevButton.addEventListener('click', () => {
    if (fileSelector.currentSelectionIndex > 1) {
        fileSelector.currentSelectionIndex--;
        fileSelector.updateSelection();
    }
});

nextButton.addEventListener('click', () => {
    if (fileSelector.currentSelectionIndex < fileSelector.totalSelections) {
        fileSelector.currentSelectionIndex++;
        fileSelector.updateSelection();
    }
});

// Deshabilitar el botón previo inicialmente si el primer archivo está seleccionado
prevButton.disabled = true;
prevButton.classList.add('disabled');
// Habilitar o deshabilitar el botón siguiente inicialmente según si el último archivo está seleccionado o no
nextButton.disabled = fileSelector.currentSelectionIndex === fileSelector.totalSelections;
if (nextButton.disabled) {
    nextButton.classList.add('disabled');
}

// poner puntos suspensivos al nombre del archivo
document.addEventListener("DOMContentLoaded", function() {
    var fileTitles = document.getElementsByClassName("file-title");
    for (var i = 0; i < fileTitles.length; i++) {
        var fileTitle = fileTitles[i];
        var filename = fileTitle.querySelector("p");
        var filenameFull = fileTitle.querySelector(".filename-full");
        var containerWidth = fileTitle.offsetWidth; // Ancho del contenedor
        var text = filename.textContent;
        var textWidth = getTextWidth(text, getComputedStyle(filename).font); // Ancho del texto
        
        // Calcular la longitud máxima del texto que cabe en el contenedor sin salto de línea
        var maxLength = Math.floor((containerWidth / textWidth) * text.length);
        
        // Truncar el texto si es necesario
        // if (text.length > maxLength) {
        //     filename.textContent = text.substring(0, maxLength) + "...";
        //     filenameFull.textContent = text;
        //     console.log(filenameFull.textContent)
        // }
    }
});

function getTextWidth(text, font) {
    // Crear un elemento span para medir el ancho del texto
    var span = document.createElement("span");
    span.textContent = text;
    span.style.font = font;
    span.style.visibility = "hidden"; // Ocultar el span
    document.body.appendChild(span);
    var width = span.offsetWidth; // Obtener el ancho del span
    document.body.removeChild(span); // Eliminar el span
    return width;
}

// Genera alerta cuando cuando se encuentra la variable err_code
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const errCode = urlParams.get('err_code');
if (errCode=='timeout') {
  alert("Ups! Parece que ha pasado un poco más de tiempo del esperado, no se pudieron procesar todos los documentos.");
}

// Funciones para dar like y dislike
function sendReaction(key, reaction) {
    fetch('/update-feedback-reaction', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ key: key, reaction: reaction })
    })
    .then(response => response.json())
    .then(data => {
        // Aquí actualizas la interfaz de usuario
        updateReactionUI(key, reaction);
    })
    .catch(error => console.error('Error:', error));
}

function updateReactionUI(key, reaction) {
    const likeButton = document.querySelector(`.button-like[data-key="${key}"]`);
    const dislikeButton = document.querySelector(`.button-dislike[data-key="${key}"]`);

    // Actualiza el estado de los botones
    if (reaction === 1) {
        likeButton.classList.add('seleted');
        dislikeButton.classList.remove('seleted');
        showBootstrapAlert('¡Gracias!', 'success');
    } else {
        dislikeButton.classList.add('seleted');
        likeButton.classList.remove('seleted');
        showBootstrapAlert('¡Gracias, seguiremos mejorando!', 'secondary');
    }
}