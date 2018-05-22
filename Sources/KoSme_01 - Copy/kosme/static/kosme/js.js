
// Create `client` using an oAuth token:

function uploadLectureText(text) {
var fileDisplayArea = document.getElementById('fileDisplayArea');

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", text, false ); // false for synchronous request
    xmlHttp.send( null );
    ans = xmlHttp.responseText;
    console.log( xmlHttp.responseText);

    fileDisplayArea.innerHTML =ans;
  //   var f = new File([""], "filename.txt", {type: "text/plain", lastModified: new Date(1995, 11, 17)})
  //
  //   var xhttp = new XMLHttpRequest();
  //
  // xhttp.open("PUT", "http://127.0.0.1:8800", true);
  // xhttp.send(f);

}

function setLectureText(text) {
    var fileDisplayArea = document.getElementById('editor1');

     var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", text, false ); // false for synchronous request
    xmlHttp.send( null );
    ans = xmlHttp.responseText;
    console.log( xmlHttp.responseText);

    fileDisplayArea.innerHTML =ans;

  //  fileDisplayArea.innerHTML =text;

}