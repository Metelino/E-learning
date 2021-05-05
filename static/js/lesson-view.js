console.log("DZIALA")
const player = document.getElementById('media-player');
const tabs_nav = document.getElementById("tabs-nav").getElementsByTagName('li');
const tabs = document.querySelectorAll('#tabs-container>div');
//console.log(tabs);
//console.log(tabs_nav);

// function set_file(event){
//     player.data = event.target.dataset.fileUrl;
// }
function set_file(event){
    player.src = event.target.dataset.fileUrl;
}

async function pass_lesson(e){
    var url = e.target.dataset.url;
    console.log(url);
    await fetch(url).then(res => {
        console.log(res.ok);
        if(res.ok){
            e.target.disabled=true;
        }
        else
            console.log("ERROR");
    });
    
}

function openTab(e, tabName) {
    var i;
    for (i = 0; i < tabs.length; i++) {
        tabs[i].style.display = "none";
        //tabs[i].style.visibility = "hidden";
        //tabs[i].style.height = "0px";
    }
    for (i = 0; i < tabs_nav.length; i++) {
        tabs_nav[i].classList.remove("is-active");
    }
    document.getElementById(tabName).style.display = "flex";
    //document.getElementById(tabName).style.visibility = "visible";
    //document.getElementById(tabName).style.height = "100%";
    e.target.parentNode.classList.add("is-active");
}

const learning_form = document.getElementById('learning-form');
const file_list = document.getElementById('file-list');
learning_form.oninput = async function(e){
    //learning_form.submit();
    formData = new FormData(learning_form);
    console.log('Zmieniam styl');
    const url = learning_form.action;

    await fetch(url, {method : 'POST', body : formData}).then(res => {
        if(!res.ok){
            console.log("ERROR przy zmianie stylu");
        }  
    });

    const file_url = learning_form.dataset.fileUrl;
    await fetch(file_url).then(res => {
        if(res.ok){
            res.text().then(res => {
                //const parser = new DOMParser();
                //const file_html = parser.parseFromString(res, "text/html");
                file_list.innerHTML = res;
                //file_list.appendChild(file_html.body.firstChild);
            })
        }
        else
            console.log('ERROR przy pobieraniu plików');
    });
}