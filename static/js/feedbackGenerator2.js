var selectedFiles = [];
const fileInput = document.getElementById('fileInput');
const uploadButtonFirst = document.getElementById('uploadButtonFirst');
const uploadDesc = document.getElementById('uploadDesc');
const filesList = document.getElementById('filesList');
const uploadButtonSecond = document.getElementById('uploadButtonSecond');
const selectFilesDesc = document.getElementById('selectFilesDesc');
const fileInputButtonFirst = document.getElementById('fileInputButtonFirst');
const fileInputButtonSecond = document.getElementById('fileInputButtonSecond');
const dropArea = document.querySelector(".upload-files");
const dropText = dropArea.querySelector(".text-drop-area");

const submitFiles = document.getElementById('submitFiles');
const imgSubmitActive = document.getElementById('imgSubmitActive');
const imgSubmitDisable = document.getElementById('imgSubmitDisable');

fileInputButtonFirst.addEventListener('click', handleFileInputButtonClick);
fileInputButtonSecond.addEventListener('click', handleFileInputButtonClick);

fileInput.addEventListener('change', handleFileInputChange);
dropArea.addEventListener("dragover", handleDragOver);
dropArea.addEventListener("dragenter", handleDragEnter);
dropArea.addEventListener("dragleave", handleDragLeave);
dropArea.addEventListener("drop", handleDrop);

function handleFileInputButtonClick() {
    fileInput.click();
}

function handleFileInputChange() {
    var files = this.files;
    handleSelectedFiles(files);
}

function handleDragOver(e) {
    e.preventDefault();
    dropText.classList.add("active");
    updateZIndex("-1");
}

function handleDragEnter(e) {
    e.preventDefault();
    dropText.classList.add("active");
}

function handleDragLeave(e) {
    e.preventDefault();
    const rect = dropArea.getBoundingClientRect();
    const x = e.clientX;
    const y = e.clientY;
    if (x < rect.left || x >= rect.right || y < rect.top || y >= rect.bottom) {
        dropText.classList.remove("active");
        updateZIndex(null);
    }
}

function handleDrop(e) {
    e.preventDefault();
    dropText.classList.remove("active");
    updateZIndex(null);

    var files = e.dataTransfer.files;
    var allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    var validFiles = [];

    for (var i = 0; i < files.length; i++) {
        if (allowedTypes.includes(files[i].type)) {
            validFiles.push(files[i]);
        }
    }

    if (validFiles.length > 0) {
        handleSelectedFiles(validFiles);
    } else {
        alert("Solo se permiten archivos de tipo Word (docx) y PDF.");
    }
}

function updateZIndex(value) {
    const elementsToUpdate = [uploadButtonFirst, uploadDesc, filesList, uploadButtonSecond, selectFilesDesc];
    elementsToUpdate.forEach(element => {
        element.style.zIndex = value;
    });
}

function addMoreFiles() {
    fileInput.click();
};

function sumSizeFiles(files) {
    var totalSize = 0;
    for (var i = 0; i < files.length; i++) {
        totalSize += files[i].size;
    }
    totalSize = (totalSize / (1024 * 1024)).toFixed(1)
    return totalSize;
};

function showSelectFiles(content, files) {
    sizeFiles = sumSizeFiles(files);
    countFiles = files.length;
    var paragraph = document.createElement('p');
    paragraph.textContent = countFiles + ' Archivos - ' + sizeFiles + ' MB';
    content.innerHTML = '';
    content.appendChild(paragraph);
};

function handleSelectedFiles(files) {
    var fileList = document.getElementById('selectedFilesList');

    for (var i = 0; i < files.length; i++) {
        var fileId = 'file_' + i;
        var listItem = document.createElement('li');
        var deleteButton = document.createElement('button');
        var deleteImage = document.createElement('img');
        deleteImage.src = '/static/img/delete.svg';
        var itemId = 'file_' + i;
        listItem.id = itemId;

        deleteButton.onclick = createDeleteHandler(listItem, fileId, fileList);

        var liContent = `
            <div>
                <img src="/static/img/file-white.svg" alt="">
                <p>${files[i].name}</p>
            </div>
        `;

        listItem.id = fileId;
        listItem.innerHTML = liContent;
        deleteButton.appendChild(deleteImage);
        listItem.appendChild(deleteButton);
        fileList.appendChild(listItem);
        selectedFiles.push(files[i]);
    }

    // console.log(selectedFiles);

    if (selectedFiles.length != 0) {
        uploadButtonFirst.style.display = 'none';
        uploadDesc.style.display = 'none';
        filesList.style.display = 'flex';
        uploadButtonSecond.style.display = 'flex';
        selectFilesDesc.style.display = 'flex';

        showSelectFiles(selectFilesDesc, selectedFiles);
    
        submitFiles.removeAttribute('disabled');
        submitFiles.classList.add('active');
        imgSubmitActive.style.display = 'block';
        imgSubmitDisable.style.display = 'none';
    }
}

function createDeleteHandler(listItem, fileId, fileList) {
    return function () {
        var index = Array.from(fileList.children).indexOf(listItem);
        selectedFiles.splice(index, 1);
        fileList.removeChild(listItem);
        showSelectFiles(selectFilesDesc, selectedFiles);

        if (selectedFiles.length == 0) {
            uploadButtonFirst.style.display = 'flex';
            uploadDesc.style.display = 'flex';
            filesList.style.display = 'none';
            uploadButtonSecond.style.display = 'none';
            selectFilesDesc.style.display = 'none';

            submitFiles.setAttribute('disabled', 'disabled');
            submitFiles.classList.remove('active');
            imgSubmitActive.style.display = 'none';
            imgSubmitDisable.style.display = 'block';
        }
    };
}

// submitFiles.addEventListener('click', function(event) {
//     event.preventDefault();

//     var form = document.getElementById('uploadForm');
//     form.submit();

// });



function extraerTextoPDF(contenido, frase) {
    return new Promise((resolve, reject) => {
        const loadingTask = pdfjsLib.getDocument(new Uint8Array(contenido));
        loadingTask.promise.then(pdf => {
            const numPages = pdf.numPages;
            let textoCompleto = '';
            const getPageText = (pageNum) => {
                if (pageNum > numPages) {
                    // Aplicar la función para extraer el texto después de la frase
                    textoCompleto = extraerTextoDespuesDeFrase(textoCompleto, "Write your answer");
                    // Remover saltos de línea
                    textoCompleto = textoCompleto.replace(/\n/g, '');
                    resolve(textoCompleto);
                    return;
                }
                pdf.getPage(pageNum).then(page => {
                    page.getTextContent().then(textContent => {
                        let textoPagina = '';
                        textContent.items.forEach(item => {
                            textoPagina += item.str + ' ';
                        });
                        textoCompleto += textoPagina;
                        getPageText(pageNum + 1);
                    }).catch(reject);
                }).catch(reject);
            };
            getPageText(1);
        }).catch(reject);
    });
}

function extraerTextoDocx(contenido) {
    return new Promise((resolve, reject) => {
        mammoth.extractRawText({arrayBuffer: contenido})
            .then(result => {
                let texto = result.value;
                // Aplicar la función para extraer el texto después de la frase
                texto = extraerTextoDespuesDeFrase(texto, "Write your answer");
                // Remover saltos de línea
                texto = texto.replace(/\n/g, '');
                resolve(texto);
            }).catch(reject);
    });
}

function extraerTextoDespuesDeFrase(texto, frase) {
    const indiceInicio = texto.indexOf(frase);
    if (indiceInicio !== -1) {
        texto = texto.substring(indiceInicio + frase.length);
    } else {
        console.log(`La frase '${frase}' no fue encontrada en el archivo.`);
    }
    return texto;
}

function enviarResultados(resultados) {
    fetch('/guardar_resultados', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(resultados)
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Error al enviar los resultados al servidor');

      }
      return response.text();
    })
    .then(data => {
      console.log('Respuesta del servidor:', data);
      window.location.href = '/loading';
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.worker.min.js'

submitFiles.addEventListener('click', function(event) {
    event.preventDefault();

    // const filesList = document.getElementById('inputFiles').files;
    const textos = [];
    var resultados = [];

    for (let i = 0; i < selectedFiles.length; i++) {
        const file = selectedFiles[i];
        const reader = new FileReader();
        reader.onload = function(event) {
            const contenido = event.target.result;
            let promise;
            if (file.type === 'application/pdf') {
                promise = extraerTextoPDF(contenido);
            } else if (file.name.endsWith('.docx')) {
                promise = extraerTextoDocx(contenido);
            }

            if (promise) {
                promise.then(texto => {
                    const resultado = {
                        nombreArchivo: file.name,
                        textoExtraido: texto
                    };
                    resultados.push(resultado);
                    if (resultados.length === selectedFiles.length) {
                        console.log("Resultados de la extracción:");
                        console.log(resultados);
                        // Enviar los resultados a Flask
                        enviarResultados(resultados);
                    }
                }).catch(error => {
                    console.error(`Error al extraer texto del archivo ${file.name}:`, error);
                });
            } else {
                console.error(`Formato de archivo no compatible: ${file.name}`);
            }
        };

        reader.readAsArrayBuffer(file);
    }
    // console.log(resultados)
    // enviarResultados(resultados);
    
    // enviarResultados(resultados);

    // var form = document.getElementById('uploadForm');
    // form.submit();

    // var form = document.createElement('form');
    // form.setAttribute('action', '/test_s');
    // form.setAttribute('method', 'POST');
    // form.setAttribute('enctype', 'multipart/form-data');
    // var input = document.createElement('input');
    // input.setAttribute('type', 'hidden');
    // input.setAttribute('name', 'total');
    // input.setAttribute('value', selectedFiles.length);
    // form.appendChild(input);


    // for (var i = 0; i < selectedFiles.length; i++) {
    //     // var input = document.createElement('input');
    //     // input.setAttribute('type', 'file');
    //     // input.setAttribute('name', i);
    //     // input.setAttribute('value', selectedFiles[i]);
    //     // form.appendChild(input);

    //     console.log(selectedFiles[i], selectedFiles[i].name, selectedFiles[i].type)

    //     var formData = new FormData();
    //     formData.append('archivo', selectedFiles[i]);
        
    //     var xhr = new XMLHttpRequest();
    //     xhr.open('POST', '/feedback-generator2', true);
    //     xhr.onload = function () {
    //         console.log('entro')
    //         if (xhr.status === 200) {
    //             console.log('Archivo enviado correctamente');
    //         } else {
    //             console.log('Error al enviar archivo');
    //         }
    //     };
    //     xhr.send(formData);
    // }

    // document.body.appendChild(form);
    // form.submit();


    // var formData = new FormData();

    // for (var i = 0; i < selectedFiles.length; i++) {
    //     console.log(selectedFiles[i])
    //     formData.append('Files[]', selectedFiles[i]);
    // }

    // console.log(JSON.stringify(formData));

    // var xhr = new XMLHttpRequest();
    // xhr.open("POST", "/read-assignments2", true);
    
    // xhr.onload = function() {
    //     if (xhr.readyState === XMLHttpRequest.DONE) {
    //         console.log('hello world')
    //         if (xhr.status === 200) {
    //             // window.location.href = '/loading';
    //         } else {
    //             console.error('Error al procesar la solicitud');
    //         }
    //     }
        
    // };

    // xhr.send(formData);
});