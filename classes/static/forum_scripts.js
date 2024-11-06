$(document).ready(async () => {
  // checking topic
  const TopicData = await (await fetch(`/api/topic?TopicId=${getQueryParam("id")}`)).json();

  if (TopicData.length === 0) {
    document.location.href = "/topic/create";
  }

  const TopicInfoVar = $("#TopicInfo");
  const TopicHTML = $(`<p> ${TopicData.time}|${TopicData.theme}|${TopicData.author}|${TopicData.about} </p>`);
  TopicInfoVar.append(TopicHTML);

  // defining socket var
  const socket = io();

  // handling start of connection
  socket.on("connect", () => {
    console.log("WebSockets connection established");
  });

  // handling incoming messages
  socket.on("NewMessage", (data) => {
    if (data.TopicId === getQueryParam("id")) {
      fetch(`/api/user?UserId=${data.author}`)
        .then((r) => r.json())
        .then((userData) => {
          return MsgSnippet(userData, data);
        })
        .then((msg) => {
          $("#Msgs").append(msg);
        });
    }
  });

  socket.on("TopicDelete", (data) => {
    if (data.TopicId === getQueryParam("id")) {
      document.location.href = "/";
    }
  }
);



  socket.on("MsgDel", (data) => {

      $(`#${data.MessageId}`).remove(); // Use template literal for dynamic ID selection

  });

  // loading message in topic via message and user API
  fetch(`/api/messages?TopicId=${getQueryParam("id")}`)
    .then((response) => response.json())
    .then((jsonData) => {
      jsonData.forEach((element) => {
        fetch(`/api/user?UserId=${element.author}`)
          .then((r) => r.json())
          .then((userData) => {
            return MsgSnippet(userData, element);
          })
          .then((msg) => {
            $("#Msgs").append(msg);
          });
      });
    })
    .catch((error) => {
      console.error("Error fetching messages:", error);
    });


  $("#TopicDelete").click(() => {
    const data = JSON.stringify({ TopicId: getQueryParam("id"), JWToken: getCookie("token") });
    console.log(data);
    socket.emit("TopicDelete", data);
  });

  // sending message
  $("#MsgForm").submit((e) => {
    e.preventDefault();
    if (IsLogged(getCookie("token")) && $("#MsgForm").find('input[name="Message"]').val() !== "") {
      const TopicId = getQueryParam("id");
      const AuthToken = getCookie("token");
      const message = $("#MsgForm").find('input[name="Message"]').val();
      socket.emit(
        "message",
        JSON.stringify({
          JWToken: AuthToken,
          TopicId: TopicId,
          message: message,
        })
      );
      $("#MsgForm").find('input[name="Message"]').val("");
    } else {
      alert("please, log in or type your message");
    }
  });
});