const file_form = document.getElementById('file-form');
const file_list = document.getElementById('file-list');
const notes = document.getElementById('notes');

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
		
var editor = CKEDITOR.replace('editor', {
    skin : 'moono-lisa',
    'height': '400px'
});

editor.on('change', function(e){
    editor.updateElement();
})

					
// function delete_file(e){
//     var url = e.target.dataset.fileUrl;
//     e.preventDefault();
//     // const url = e.target.getAttribute("href");
//     console.log(url);
//     fetch(url).then(res => {
//         if(res.ok){
//             const f = e.target.closest('div.card');
//             f.remove();
//         }
//         else
//             console.log("ERROR usuwanie pliku");
//     });
// }

// file_form.onsubmit = function(e){
//     e.preventDefault();
//     formData = new FormData(file_form);
//     console.log('Wysyłam formularz');
//     const url = file_form.action;
//     const note = document.createElement('div');
//     fetch(url, {method : 'POST', body : formData}).then(res => {
//         if(res.ok){
//             res.text().then(res => {
//                 const parser = new DOMParser();
//                 const file_html = parser.parseFromString(res, "text/html");
//                 file_list.appendChild(file_html.body.firstChild);
//             })
//             //notes.appendChild
//         }
//         else
//             console.log('ERROR wysyłanie pliku');
//     });
// }


