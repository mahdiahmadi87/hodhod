// script.js


function changeRange(n, id) {
    $.ajax({
        type: "GET",
        url: '/newsRating',
        data: {
            "result": {"n": n, "id": id},
        },
        dataType: "json",
    });
}

function changeColor(n, id) {
    let star = document.getElementById(`star${id}`);
    let r ,g
    if (n <= 2.5){
        r = 255
        g = n * 102
    }
    else {
        g = 255
        r = 5 - n 
        r = r * 102
    }
    star.style.accentColor = `rgb(${r}, ${g}, 0)`
}
