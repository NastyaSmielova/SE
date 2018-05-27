function uploadLectureText(link) {

    var fileDisplayArea = document.getElementById('fileDisplayArea');
    fileDisplayArea.innerHTML =getText(link);

}


function updateText() {
    var editorText = CKEDITOR.instances.editor1.getData();
    var request = new XMLHttpRequest();
    var link =  document.getElementById("link").innerHTML;
    request.open("PUT", link,false);
    request.send(editorText);
}


function getText(link) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", link, false );
    xmlHttp.send( null );
    ans = xmlHttp.responseText;
    return ans;
}

function setLectureText(link) {
    var fileDisplayArea = document.getElementById('editor1');
    fileDisplayArea.innerHTML = getText(link);
}