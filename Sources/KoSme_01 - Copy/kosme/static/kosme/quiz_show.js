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

function loadSurvey() {
    var json = document.getElementById('surveyJSON');
    json.value = editor.text;
    alert(editor.text);
}

var editorOptions = {showEmbededSurveyTab: false, showJSONEditorTab: false, showElementEditor: false, showDesigner: false };
var editor = new SurveyEditor.SurveyEditor("editorElement", editorOptions);
editor.text = document.getElementById('mainJSON');
loadSurvey();




