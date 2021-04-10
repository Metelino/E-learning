const test_form = document.getElementById('test');

test_form.onsubmit = function(e){
    e.preventDefault();
    const formData = new FormData(test_form);
    
}