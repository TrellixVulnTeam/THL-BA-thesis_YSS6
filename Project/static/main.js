var picks = new Array();

window.onclick = function (event) {
    if (!event.target.matches('.pick')) {
        var dropdowns = document.getElementsByClassName("drop_down_menu");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

function showMenu(element) {
    $(element).after($('#menu'));
    document.getElementById('menu').classList.toggle('show');
}

function selectHero(element,hero_id){
    console.log(element.id);
    console.log(hero_id);
}

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