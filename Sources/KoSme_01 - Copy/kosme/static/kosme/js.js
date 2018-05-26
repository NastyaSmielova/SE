

function uploadLectureText(text) {
    var fileDisplayArea = document.getElementById('fileDisplayArea');

     text = text.replace(/__4__/g, '<');
    text = text.replace(/___6___/g, '>');


    fileDisplayArea.innerHTML =text;

}



function setLectureText(text) {
    var fileDisplayArea = document.getElementById('editor1');

     text = text.replace(/__4__/g, '<');
    text = text.replace(/___6___/g, '>');


    fileDisplayArea.innerHTML =text;

}