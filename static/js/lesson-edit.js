const file_form = document.getElementById('file-form');
const file_list = document.getElementById('file-list');

// file_form.onsubmit = function(e){
//     e.preventDeafult();
//     var res;
//     var url = e.target.dataset.url;
//     res = await fetch(url).then(response => {return response.text()});
//     console.log(res)
//     if(res == 'OK'){
//         const f = e.target.closest('article');
//         f.remove();
//         //e.target.remove()
//     }
//     else
//         console.log("Coś się zepsuło...")
// }

async function delete_file(e){
    e.preventDefault();
    var url = e.target.href;
    var res = await fetch(url).then(response => {return response.text()});
    console.log(res)
    if(res == 'OK'){
        const f = e.target.closest('div.card');
        f.remove();
        //e.target.remove()
    }
    else
        console.log("Coś się zepsuło...")
}

file_form.onsubmit = function(e){
    e.preventDefault();
    formData = new FormData(file_form);
    console.log('Wysyłam formularz');
    const url = file_form.action;
    fetch(url, {method : 'POST', body : formData}).then(res => {
        if(res.ok){
            res.text().then(res => {
                const parser = new DOMParser();
                const file_html = parser.parseFromString(res, "text/html");
                file_list.appendChild(file_html.body);
            }) 
        }
        else
            console.log('ERROR');
    });
}


