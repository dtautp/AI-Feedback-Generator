var selectedFiles = [];
var maxUploadFiles = 19;
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
    var extensionErrorList = [];

    for (var i = 0; i < files.length; i++) {
        if (allowedTypes.includes(files[i].type)) {
            validFiles.push(files[i]);
        } else {
            extensionErrorList.push(files[i].name)
        }
    }

    if (extensionErrorList.length > 0) {
        let errorMessage = `<p>No se pudieron agregar los siguientes archivos, ya que solo se permiten archivos de tipo Word (docx) o PDF:</p><ul>`;
        extensionErrorList.forEach(function(errorItem) {
            errorMessage += `<li><p>${errorItem}</p></li>`;
        });
        errorMessage += `</ul>`;
        $('#extensionErrorModalBody').html(errorMessage);
        $('#extensionErrorModal').modal('show');
    }

    if (validFiles.length > 0) {
        handleSelectedFiles(validFiles);
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
    var sizeErrorList = []
    var quantityErrorList = []
    
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

        if (selectedFiles.length <= maxUploadFiles) {
            if (files[i].size <= 5 * 1024 * 1024) { // Verificar si el tamaño del archivo es menor o igual a 5 MB
                listItem.id = fileId;
                listItem.innerHTML = liContent;
                deleteButton.appendChild(deleteImage);
                listItem.appendChild(deleteButton);
                fileList.appendChild(listItem);
                selectedFiles.push(files[i]);
                console.log(files[i].size);
            } else {
                sizeErrorList.push(files[i].name)
            }
        } else {
            quantityErrorList.push(files[i].name)
        }
    }

    // Mostrar modal de errores maximo de peso y archivos
    if (sizeErrorList.length > 0) {
        let errorMessage = `<p>No se pudieron agregar los siguientes archivos, ya que superaron el tamaño máximo de 5 MB:</p><ul>`;
        sizeErrorList.forEach(function(errorItem) {
            errorMessage += `<li><p>${errorItem}</p></li>`;
        });
        errorMessage += `</ul>`;
        $('#sizeErrorModalBody').html(errorMessage);
        $('#sizeErrorModal').modal('show');
    }

    if (quantityErrorList.length > 0) {
        let errorMessage = `<p>No se pudieron agregar los siguientes archivos, ya que superaron el número máximo de ${maxUploadFiles + 1} archivos:</p><ul>`;
        quantityErrorList.forEach(function(errorItem) {
            errorMessage += `<li><p>${errorItem}</p></li>`;
        });
        errorMessage += `</ul>`;
        $('#quantityErrorModalBody').html(errorMessage);
        $('#quantityErrorModal').modal('show');
    }
    
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
      let form = document.getElementById("uploadForm");
      document.getElementById('homework_number').value = document.getElementById('tarea_numero').value
      form.removeChild(document.getElementById("fileInput"));
      document.getElementById("request_group").value = data;
      form.submit()
    //   window.location.href = '/loading';
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
});