const board_number = window.location.pathname.split('/board/')[1]

$.ajax({
    "url": `/api/v1/boards/board/${board_number}`,
    "method": "GET",
    "timeout": 0,
}).done(function (board) {
    console.log(board);
    $('#author').text(board.author === null ? 'anonymous' : board.author.username);
    $('#title').val(board.title);
    $('#content').val(board.content);
    $('#file').attr('src', board.image_url);
    $('#created_at').val(board.createdAt);
    $('#modified_at').val(board.modifiedAt);



    $('#image-container').append(`
            <img src="${board.image_url}">
            `);

    if (board.file !== null && board.file !== '') {
        $('#image-container').append(`
        <input type="radio" name="language" value="eng" id="eng-radio">
    <label for="eng-radio">English</label>
    <input type="radio" name="language" value="kor" id="kor-radio">
    <label for="kor-radio">Korean</label>
    <input type="radio" name="language" value="jpn" id="jpn-radio">
    <label for="jpn-radio">Japnanese</label>
            <button id="text-transfer">텍스트변환</button>
            <div id="image-text">
            <textarea id="content" name="content" readonly></textarea>
            </div>
            
            `);
    }

    $('#text-transfer').on('click', function () {
        const selectedLanguage = $('input[name="language"]:checked').val();
        const imageUrl = board.image_url;

    
        $.ajax({
            "url": '/api/v1/extract-text/',
            "method": "POST",
            "data": {
                "image_url": imageUrl,
                "language": selectedLanguage,
            },
            "timeout": 0,
        }).done(function (response) {
            
            $('#image-text').text(response.text);
        }).fail(function (error) {
            console.error("Error while extracting text:", error);
            $('#image-text').text("Error occurred during text extraction.");
        });
    });

});

