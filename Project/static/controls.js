var picks = new Array();

function saveData() {
    picks.push(document.getElementById("pick_0").value);
    picks.push(document.getElementById("pick_1").value);
    picks.push(document.getElementById("pick_2").value);
    picks.push(document.getElementById("pick_3").value);
    picks.push(document.getElementById("pick_4").value);
    picks.push(document.getElementById("pick_5").value);
    picks.push(document.getElementById("pick_6").value);
    picks.push(document.getElementById("pick_7").value);
    picks.push(document.getElementById("pick_8").value);
    picks.push(document.getElementById("pick_9").value);
}

function predict() {
    //console.log(picks);
    $.ajax({
        url: "/prediction/",
        type: "POST",
        data: JSON.stringify(picks),
        contentType: 'application/json',
        success: function (res) {
            alert(res)
        }
    });
}