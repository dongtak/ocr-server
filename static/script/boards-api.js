$.ajax({
    "url": "/api/v1/boards",
    "method": "GET",
    "timeout": 0,
}).done(function (list) {
    list.forEach(board => {

        image_url = 'media/tvPWB89.webp';

        if (board.image_url !== null && board.image_url !== '') {
            image_url = board.image_url;
        }
    
        
        $('#boards-container').append(`
        <div class="board">
                <img src="${image_url}">
                <p>
                    <a href="/board/${board.bNum}"><h4>${board.title}</h4></a>
                    <span>${board.author}</span>
                </p>
            </div>
        `)
    })
});