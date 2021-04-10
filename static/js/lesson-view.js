console.log("DZIALA")
const player = document.getElementById('media-player');
const learning_form = document.getElementById('learning-form');

// function get_file(file_pk){
//     fetch('courses/stream_file/' + file_pk).then(
//         data => {
//             player.data = data;
//         }
//     )
// }

try{
    learning_form.oninput = function(e){
        learning_form.submit();
    }
}catch{
    console.log("Nie nauczyciel");
}

function set_file(event){
    player.data = event.target.dataset.fileUrl;
}

async function pass_lesson(e){
    var url = e.target.dataset.url;
    console.log(url);
    await fetch(url).then(res => {
        console.log(res.ok);
        if(res.ok){
            e.target.disabled=True;
        }
        else
            console.log("ERROR");
    });
    
}