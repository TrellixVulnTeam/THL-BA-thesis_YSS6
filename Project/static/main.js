var picks = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1];

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

function selectHero(element, hero_mapping) {
    var hero_name = $(element).text();
    var hero_id = hero_mapping[hero_name];

    var pick_button_id = $(element).parent()[0].id;
    var index = parseInt(pick_button_id[5]);

    picks[index] = hero_id;
    document.getElementById(pick_button_id).innerHTML = hero_name;
}

function resetHero(element) {
    var pick_button_id = element.id;
    var index = parseInt(pick_button_id[5]);

    picks[index] = -1;
    document.getElementById(pick_button_id).innerHTML = '';
}

var click_timeout = 0;

function clickEvent(event) {
    var click_time = event.originalEvent.detail;
    var pick_button = this;

    if (click_timeout) {
        clearTimeout(click_timeout);
        click_timeout = 0;
    }

    switch (click_time) {
        case 1:
            click_timeout = setTimeout(function () {
                showMenu(pick_button)
            }, 200);
            break;
        case 2:
            resetHero(pick_button);
            break;
    }
}

$(document).ready(function () {
    $('.pick').on('click', clickEvent);
});

function predict() {
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

                console.log(res);

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

function recommend(){
    $.ajax({
        url: "/recommend",
        type: "POST",
        data: JSON.stringify(picks),
        contentType: 'application/json',
        success: function (res) {
            alert('Recommendation: Try '+res['hero_name']);
            console.log(res['hero_name']);
        }
    });
}