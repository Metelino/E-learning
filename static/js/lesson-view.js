console.log("DZIALA")
const player = document.getElementById('media-player');

// function get_file(file_pk){
//     fetch('courses/stream_file/' + file_pk).then(
//         data => {
//             player.data = data;
//         }
//     )
// }

function set_file(event){
    //const das = event.dataset;
    player.data = event.target.dataset.fileUrl;
}