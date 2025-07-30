$(document).ready(async () => {
  // checking topic
  const TopicData = await (await fetch(`/api/topic?TopicId=${getQueryParam("id")}`)).json();




  if (TopicData.length === 0) {
    document.location.href = "/topic/create";
  }

  const TopicInfoVar = $("#TopicInfo");
  console.log(TopicData)
  TopicInfoVar.append( $(`<img width=20% height=20% src="/media/${TopicData.image}" />`) )
  const TopicHTML = $(`<p id = "StatusBar"> ${TopicData.time}|${TopicData.theme}|${TopicData.author} </p><div>${TopicData.about}</div>`);
  TopicInfoVar.append($(`<h3>${TopicData.name}</h3`))
  TopicInfoVar.append(TopicHTML);

  if (TopicData.protected == 1) {

        $("#StatusBar").append("<p id='UserNameProfileAdmin' >in this topic can write only his creator</p>")

  }

  var ImgData = ""

  function encodeImageFile() {

    return new Promise( (resolve, reject) => {
        var filesSelected = document.getElementById("FileInput").files;
        if (filesSelected.length > 0) {
          var fileToLoad = filesSelected[0];
          var fileReader = new FileReader();

          fileReader.onload = function(fileLoadedEvent) {
            var srcData = fileLoadedEvent.target.result;
            resolve(srcData);
          }
          fileReader.readAsDataURL(fileToLoad);
        }
        resolve("");
      }
  )
}

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
  $("#MsgForm").submit( async (e) => {
    e.preventDefault();
    if (IsLogged(getCookie("token")) && $("#MsgForm").find('input[name="Message"]').val() !== "") {
      var TopicId = getQueryParam("id");
      var AuthToken = getCookie("token");
      var message =  DOMPurify.sanitize( $("#MsgForm").find('input[name="Message"]').val() + reply )
      ImgData = await encodeImageFile()
      console.log(ImgData)

      socket.emit(
        "message",
        JSON.stringify({
          JWToken: AuthToken,
          TopicId: TopicId,
          message: message,
          ImgData: ImgData,
        })
      );
      $("#MsgForm").find('input[name="Message"]').val("");
      numOfReply = 0;
    } else {
      alert("please, log in or type your message");
    }
  });
});