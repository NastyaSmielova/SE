//add a property to the survey object
Survey
    .JsonObject
    .metaData
    .addProperty("survey", "tag:number");

//remove a property to the page object. You can't set it in JSON as well
Survey
    .JsonObject
    .metaData
    .removeProperty("page", "visibleIf");
//remove a property from the base question class and as result from all questions
Survey
    .JsonObject
    .metaData
    .removeProperty("questionbase", "visibleIf");

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

var editorOptions = {showEmbededSurveyTab: false, questionTypes : ["text", "checkbox", "dropdown","radiogroup"] };
var editor = new SurveyEditor.SurveyEditor("editorElement", editorOptions);

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

editor.saveSurveyFunc = function () {
    //save the survey JSON
    var jsonEl = document.getElementById('surveyJSON');
    //jsonEl.value = editor.text;
    var quiz_name = document.getElementById('quiz_name').value;

    if(quiz_name.trim() === '')
        alert("Quiz cannot be saved.Enter quiz name!");
    else
        $.ajax({
                headers: { "X-CSRFToken": $.cookie("csrftoken") },
                type: "POST",
                data: { Json : editor.text, quiz_name : quiz_name},
                success: function(data) {
                    top.location.href = "/kosme/user";
                }
            });
        alert("Quiz saved")
};

