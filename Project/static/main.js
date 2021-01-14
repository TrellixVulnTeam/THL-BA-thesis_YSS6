var picks = new Array(10);

window.onclick = function (event) {
    if (!event.target.matches('.pick')) {
        $('.menu').css('visibility', 'hidden');
    }
}

function showMenu(element) {
    var pick_button_id = element.id;
    $('.menu').attr('id', pick_button_id);
    $('.menu').css('visibility', 'visible');
}

function selectHero(element, hero_id) {
    var pick_button_id = $(element).parent()[0].id;
    var index = parseInt(pick_button_id[5]);
    picks[index] = hero_id;

    var hero_name = $(element)[0].id
    document.getElementById(pick_button_id).innerHTML = hero_name;
}

function predict() {
    //console.log(picks);
    $.ajax({
        url: "/predict",
        type: "POST",
        data: JSON.stringify(picks),
        contentType: 'application/json',
        success: function (res) {
            if (res instanceof Object == true) {
                var prob_radiant = res[0];
                var prob_dire = res[1];
                var team_radiant = $('.team_radiant');
                var team_dire = $('.team_dire');
                if (prob_radiant > prob_dire) {
                    team_radiant.css('background-color', 'rgb(143, 188, 143)');
                    team_dire.css('background-color', 'rgb(200, 80, 80)');
                } else {
                    team_radiant.css('background-color', 'rgb(200, 80, 80)');
                    team_dire.css('background-color', 'rgb(143, 188, 143)');
                }
            } else {
                alert(res);
            }
        }
    });
}