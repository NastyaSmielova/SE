//add a property to the survey object
Survey
    .JsonObject
    .metaData
    .addProperty("survey", "tag:number");
//add a property to the page object
Survey
    .JsonObject
    .metaData
    .addProperty("page", {
        name: "tag:number",
        default: 1
    });
//add a property to the base question class and as result to all questions
Survey
    .JsonObject
    .metaData
    .addProperty("questionbase", {
        name: "tag:number",
        default: 0
    });

var editorOptions = {showEmbededSurveyTab: false,showPagesToolbox: false, questionTypes : ["text", "checkbox", "dropdown","radiogroup"]};
var editor = new SurveyEditor.SurveyEditor("editorElement", editorOptions);
myWhiteList = ["correctAnswer"];

editor.onCanShowProperty.add(function (sender, options) {
    options.canShow = myWhiteList.indexOf(options.property.name) > -1;
});

function checkAnswers(json) {
     parsedJson = JSON.parse(json);
        // change
        for (x=0; x < parsedJson.pages[0].elements.length; x++) {
              if(parsedJson.pages[0].elements[x].correctAnswer === undefined)
                  return false;
              }
        return true;
}


editor.saveSurveyFunc = function () {
    var quizName = document.getElementById('quiz_name').value;
    parsedJson = JSON.parse(editor.text);

    if(quizName.trim() === '')
        alert("Quiz cannot be saved.Enter quiz name!");

    if(checkAnswers(editor.text) === true) {
        $.ajax({
            headers: {"X-CSRFToken": $.cookie("csrftoken")},
            type: "POST",
            data: {Json: editor.text, quiz_name: quizName},
            success: function (data) {
                top.location.href = "/kosme/courses";
            }
        });
        alert("Quiz saved");
    }
    else
        alert("Complete answers");
};

function loadSurvey() {
    var json = document.getElementById('surveyJSON');
   json.value = editor.text
}

editor.text = document.getElementById('mainJSON').value;
loadSurvey();



