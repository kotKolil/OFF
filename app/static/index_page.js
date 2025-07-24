$(document).ready(async () => {
    // Loading info about user via JS and API
    var UserToken = getCookie("token");
    if (await IsLogged(UserToken)) {
        var UserData = await UserDataGet(UserToken);
        $("#LogoImage").attr("src", `/media/${UserData.LogoPath}`);
        $("#UserName").text(`${UserData.UserId}`);
        $("#PersonalPage").attr("href", `UserPage?id=${UserData.UserId}`);
    } else {
        $("#LogoImage").attr("src", "/media/default.png");
        $("#UserName").text("Anonim");
    }

    // Fetching data
    var NumOfMessages = await (await fetch("/api/messages/all")).json();
    var ForumName = await (await fetch("/api/GetForumName")).json();
    var NumOfTopics = await (await fetch("/api/topic/all")).json();
    var UsersData = await (await fetch("/api/user/all")).json();

    // Getting the number of messages, topics, and users
    NumOfMessages = NumOfMessages.length;
    var NumOfTopicsCount = NumOfTopics.length;
    var NumOfUsers = UsersData.length;




    // Finding admin user
    var Admin = "";
    for (var i = 0; i < NumOfUsers; i++) {
        if (UsersData[i].IsAdmin == 1) {
            Admin = UsersData[i].UserId;
            break; // Exit loop after finding the first admin
        }
    }


    $(".brand").text(ForumName.ForumName);
    $(".brand").click( () =>  {

        document.location.href = "/";

    });
});