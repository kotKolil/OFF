$(document).ready(() => {
    $("#CreateTopicForm").on('submit', (e) => {
        if ( ( $("#file_input").get(0).files[0].size / (2 ** 20) ) > 10 ) {
            e.preventDefault();
            alert("file too big")
        }
    });
});