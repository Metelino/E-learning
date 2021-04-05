console.log("DZIALA")
var question_count = 2;
const question_list = document.getElementById("question-list");
const question_form = document.getElementById("question-form");
const question_content = document.getElementById("question-content");
// const real_form = document.getElementById("real-form");
// const real_answer = document.getElementById('real_answer')
// const real_content = document.getElementById('real_content')
// const real_fields = document.getElementById('real_fields')
const q_count = document.getElementById("question-count");
q_count.value = question_count;

function add_question(){
    question_count++;
    q_count.value = question_count;

    const label = document.createElement("label");
    label.className = 'label is-small';
    label.innerText = 'Odpowiedź ' + String(question_count);

    const text_input = document.createElement("input");
    text_input.type = 'text';
    text_input.className = 'input';
    text_input.setAttribute('name', 'question-' + String(question_count));
    text_input.setAttribute('id', 'question-' + String(question_count));

    const radio_input = document.createElement("input"); 
    radio_input.type = 'radio';
    radio_input.setAttribute('id', 'radio-'+ String(question_count));
    radio_input.setAttribute('name', 'answer');
    radio_input.value = question_count-1;

    const control = document.createElement("div");
    control.className = 'control';
    control.appendChild(radio_input);
    control.appendChild(text_input);

    const field = document.createElement("div");
    field.className='field';
    field.appendChild(label);
    field.appendChild(control);
    question_form.appendChild(field);
}

function remove_question(){
    if(question_count > 2){
        question_count--;
        q_count.value = question_count;
        question_form.removeChild(question_form.lastChild);
    }
}

function submit_form(){
    // const answer_fields = {'fields' : []};
    // for(var i=1; i < question_count+1; i++){
    //     const q = document.getElementById('question-'+String(i));
    //     answer_fields.fields.push(q.value);
    //     //question_form['radio-'+ String(i)].value = 
    // }
    //const radio = document.getElementById('radio-'+ String(question_count))
    //radio.value = document.getElementById('question-'+ String(question_count)).value
    question_form.submit();
}

