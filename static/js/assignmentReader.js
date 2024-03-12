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

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    // event.preventDefault();
    var formData = new FormData();

    for (var i = 0; i < selectedFiles.length; i++) {
        formData.append('files[]', selectedFiles[i]);
    }

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/read-assignments");
    xhr.send(formData);
});