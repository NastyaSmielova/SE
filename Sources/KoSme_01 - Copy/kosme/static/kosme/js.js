function uploadLectureText(text) {
var fileDisplayArea = document.getElementById('fileDisplayArea');

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", text, false ); // false for synchronous request
    xmlHttp.send( null );
    ans = xmlHttp.responseText;
    console.log( xmlHttp.responseText);

    fileDisplayArea.innerHTML =ans;


}



$('#form').submit(function() {
    // DO STUFF...

var host = "http:/127.0.0.1:8800/";
host = host.concat(document.getElementById('fileName').innerHTML);
console.log(host);
alert(host);

var request = new XMLHttpRequest();

request.open("PUT", host,false);
    var fileDisplayArea = document.getElementById('editor1').innerHTML;

request.send(fileDisplayArea)
        ans = request.responseText;

console.log(ans);
console.log("___________")

    return true; // return false to cancel form action
});

function saveDocumentByName() {
var host = "http://127.0.0.1:8800/";
host = host.concat(document.getElementById('fileName').value);
host = host.concat('.txt');
console.log(host);
//alert(host);

var request = new XMLHttpRequest();
request.open("PUT", host ,false);
    var fileDisplayArea = document.getElementById('HTMLtoPDF').value;

request.send(fileDisplayArea)
        ans = request.responseText;

console.log(ans);
console.log("___________")


}

function setLectureText(text) {
    var fileDisplayArea = document.getElementById('editor1');
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", text, false );
    xmlHttp.send( null );
    ans = xmlHttp.responseText;
    console.log( xmlHttp.responseText);
    fileDisplayArea.innerHTML =ans;


}