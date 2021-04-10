console.log('Dziala')
async function course_signup(e){
    var res;
    var url = e.target.dataset.url;
    res = await fetch(url).then(response => {return response.text()});
    console.log(res)
    if(res == 'OK'){
        const f = e.target;
        f.remove();
        //e.target.remove()
    }
    else
        console.log("Coś się zepsuło...")
}