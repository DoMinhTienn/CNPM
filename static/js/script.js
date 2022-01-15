function addToNote(id, name, gioitinh, yearofbirth, address) {
    event.preventDefault();
    fetch('/api/add_to_note', {
        method: 'post',
        body: JSON.stringify({
           'id': id,
           'name': name,
           'gioitinh' : gioitinh,
           'yearofbirth' : yearofbirth,
           'address' : address,
           'ngay' : ngay
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        location.reload()
        console.info(res)
        return res.json()
    }).catch(function(err) {
        console.error(err)
    })
}

function save(){

    if (confirm('Bạn chắc chắn muốn phiếu khám?') == true) {
        fetch('/api/save', {
            method: 'post'
        }).then(res => res.json()).then(data => {
            if (data.code == 200)
                location.reload()
            if (data.code == 400)
                alert("Lỗi")
        }).catch(err =>  console.error(err))
    }
}

function deleteNote(pId) {
    if (confirm('Ban chac chan xoa benh nhan!!!') == true) {
        fetch(`/api/delete-note/${pId}`, {
            method: 'delete'
        }).then(res => res.json()).then(data => {
            if (data.code == 200) {
                location.reload()
                let r = document.getElementById(`p${pId}`)
                r.style.display = 'none'
            } else if (data.code == 404)
                alert(data.err_msg)
        }).catch(err => console.error(err))
    }
}

$(window).on('scroll', function () {
    if ($(window).scrollTop() > 70) {
        $('.backtop').addClass('reveal');

    } else {
        $('.backtop').removeClass('reveal');
    }
});