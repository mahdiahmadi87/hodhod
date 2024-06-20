// script.js


// Funtion to update rating
function gfg(n, id) {
    let stars = document.getElementsByClassName(`star${id}`);
	remove(id);
	for (let i = 0; i < n; i++) {
        switch (n) {
            case 1:
                cls = "one"; break;
            case 2:
                cls = "two"; break;
            case 3:
                cls = "three"; break;
            case 4:
                cls = "four"; break;
            case 5:
                cls = "five"; break;                         
            }
		stars[i].className = `star${id} ` + cls;
	}
    $.ajax({
        type: "GET",
        url: '/newsRating',
        data: {
            "result": {"n": n, "id": id},
        },
        dataType: "json",
    });
}

function remove(id) {
	let i = 0;
    let stars = document.getElementsByClassName(`star${id}`);
	while (i < 5) {
        stars[i].className = `star${id}`;
		i++;
	}
}
