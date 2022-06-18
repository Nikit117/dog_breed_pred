const input_image = document.getElementById('image');
const image_preview = document.getElementById('image_preview');
const image_caption = document.getElementById('caption');
const predict = document.getElementById("predict");
const reset = document.getElementById("reset");
const loading_div = document.getElementById('loading');
const result_div = document.getElementById('result_section');
const prediction_table = document.getElementById('prediction_table')
let file_object;

input_image.addEventListener('change', function () {
    preview(this.files[0]);
})

image_preview.onclick = () => {
    input_image.click();
}

image_preview.ondragover = () => {
    image_preview.classList.add('border-secondary');
    return false;
}

image_preview.ondragleave = () => {
    image_preview.classList.remove('border-secondary');
    return false;
}

image_preview.ondrop = (event) => {
    event.preventDefault();
    const supportedTypes = ["image/png", "image/jpeg"];
    const file = supportedTypes.includes(event.dataTransfer.files[0].type) ? event.dataTransfer.files[0] : undefined;
    preview(file);
}

reset.onclick = (e) => {
    input_image.value = '';
    preview(undefined);
    image_caption.innerText = 'No Image';
}

predict.onclick = (e) => {
    e.preventDefault();
    if (file_object) {
        resetDiv();
        result_div.classList.remove('d-none');
        getPrediction();
    }
}

function getPrediction() {
    let form_data = new FormData();
    form_data.append('file', file_object);
    fetch('/prediction', {
        method: 'POST',
        body: form_data
    }).then(
        (res) => {
            res.json().then(
                (data) => {
                    if (res.status !== 200) {
                        resetDiv();
                        showAlert(`${res.status} Error  :  ${data.Error}`);
                    } else {
                        showResult(data);
                        loading_div.classList.add('d-none');
                        prediction_table.classList.remove('d-none');
                    }
                }
            )
        }
    )
    .catch(
        (err) => {
            showAlert(err);
        }
    )
}

function resetDiv(){
    if (!result_div.classList.contains('d-none')){
        result_div.classList.add('d-none');
    }
    if (loading_div.classList.contains('d-none')){
        loading_div.classList.remove('d-none');
    }
    if (!prediction_table.classList.contains('d-none')){
        prediction_table.classList.add('d-none');
    }
}

function showResult(results) {
    let row;
    let prediction_body = document.getElementById("prediction_data");
    prediction_body.innerHTML = '';
    let percent;
    for (let result in results) {
        percent = parseFloat(results[result]);
        percent = (percent.toFixed(4)*100).toFixed(2);
        row = `<tr>
                <td>${result}</td>
                <td class="border-left border-dark" data-toggle="tooltip" data-placement="right" title='${results[result]}'>${percent}</td>
            </tr>`;
        prediction_body.innerHTML += row;
    }
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })
    document.getElementById('prediction_file_name').innerText = 'on ' + file_object.name;
    document.getElementById('result_section').classList.remove('d-none');
}

function showAlert(msg) {
    msg = `<div class="alert alert-danger alert-dismissible fade show text-center" role="alert">
            <span> ${msg} </span>
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>`;
    let alert_box = document.getElementById('alert_box');
    alert_box.innerHTML += msg;
}

function preview(file) {
    if (file && (file.type === 'image/png' || file.type === 'image/jpeg')) {
        const reader = new FileReader();
        reader.addEventListener('load', function () {
            image_preview.setAttribute('src', this.result);
            image_preview.style.width = '100%';
            image_preview.style.borderStyle = 'solid';
            image_preview.classList.remove('border-secondary');
            image_caption.innerText = file.name;
        });
        reader.readAsDataURL(file);
        file_object = file;
    } else {
        image_preview.setAttribute('src', `/static/image/drop_here.jpg`);
        image_preview.style.width = '60%';
        input_image.value = '';
        image_preview.style.setProperty('border-style', 'dashed', 'important');
        image_preview.classList.remove('border-secondary');
        image_caption.innerText = 'Image Not Selected';
        file_object = undefined;
    }
}