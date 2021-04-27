console.log("DZIALA")
var question_count = 2;
const question_list = document.getElementById("question-list");
const question_form = document.getElementById("question-form");
var empty_form = document.getElementById('empty-form');
var form_idx = document.getElementById('id_form-TOTAL_FORMS');

function add_question(){
    const field = document.createElement("div");
    field.innerHTML = empty_form.innerHTML.replaceAll('__prefix__', String(form_idx.value))
    field.className='field';
    question_form.appendChild(field);
    form_idx.value++;
}

function remove_question(){
    if(form_idx.value > 2){
        form_idx.value--;
        question_form.removeChild(question_form.lastChild);
    }
}

// function submit_form(){
//     question_form.submit();
// }

function openTab(evt, tabName) {
    var i, x, tablinks;
    x = document.getElementsByClassName("content-tab");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tab");
    for (i = 0; i < x.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" is-active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " is-active";
  }
