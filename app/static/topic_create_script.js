$(document).ready(() => {
    $("#CreateTopicForm").on('submit', (e) => {
        const fileInput = $("#file_input").get(0);
        const file = fileInput.files[0];
        if (!file) {
            return;
        }
        const maxSize = 10 * 1024 * 1024; // 10 МБ
        if (file.size > maxSize) {
            e.preventDefault();
            alert("File too big");
        }
    });
});