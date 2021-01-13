var picks = new Array();

function predict() {
    //console.log(picks);
    $.ajax({
        url: "/predict",
        type: "POST",
        data: JSON.stringify(picks),
        contentType: 'application/json',
        success: function (res) {
            console.log(res)
        }
    });
}