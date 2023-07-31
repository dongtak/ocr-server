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
    $('#file').attr('src', board.file);
    $('#created_at').val(board.createdAt);
    $('#modified_at').val(board.modifiedAt);


    image_url = 'media/tvPWB89.webp';
    image_url = board.file === null ? image_url : board.file;

    $('#image-container').append(`
            <img src="${image_url}">
            `)
    if (board.file !== null) {
        $('#image-container').append(`
        <select id="language-select" multiple>
        <option value="eng">English</option>
        <option value="kor">Korean</option>
        <option value="chi_sim">Simplified Chinese</option>
        <option value="chi_tra">Traditional Chinese</option>
        <option value="jpn">Japanese</option>
        <option value="fra">French</option>
        <option value="deu">German</option>
        <option value="spa">Spanish</option>
        <option value="ita">Italian</option>
        <option value="por">Portuguese</option>
    </select>
            <button id="text-transfer">텍스트변환</button>
            <div id="image-text"></div>
            `);
        }
});