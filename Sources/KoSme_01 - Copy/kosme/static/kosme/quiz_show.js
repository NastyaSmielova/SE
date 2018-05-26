

Survey
    .StylesManager
    .applyTheme("default");

json = document.getElementById('mainJSON').value;
result = {completedHtml: "<h3>You have answered correctly <b>{correctedAnswers}</b> questions from <b>{questionCount}</b>.</h3>"};
alert(json);
var newJson = $.extend({}, JSON.parse(json) , result);

window.survey = new Survey.Model(newJson);
function surveyValidateQuestion(survey, options) {
    result =  survey.getCorrectedAnswerCount();
    $.ajax({
                headers: { "X-CSRFToken": $.cookie("csrftoken") },
                type: "POST",
                data: { result : result}
            });
        alert("data sended");
        options.complete();
}


survey.onComplete.add(function (result) {
        document.querySelector('#surveyResult').innerHTML = "result: " + JSON.stringify(result.data);
    });

$("#surveyElement").Survey({model: survey,onServerValidateQuestions: surveyValidateQuestion});
//loadSurvey();




