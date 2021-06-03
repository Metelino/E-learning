const file_form = document.getElementById('file-form');
const file_list = document.getElementById('file-list');
const notes = document.getElementById('notes');
		
var editor = CKEDITOR.replace('editor', {
    skin : 'moono-lisa',
    'height': '400px'
});

editor.on('change', function(e){
    editor.updateElement();
})

// tinymce.init({
//     selector: '#editor',
//     plugins: 'fullscreen',
//     setup: function (editor) {
//         editor.on('change', function () {
//             editor.save();
//         });
//     }
//   });

