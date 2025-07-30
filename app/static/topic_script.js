const socket = io();
var reply = ""
var numOFReply = 0

function DeleteMessage (MsgId) {

   var data = JSON.stringify( {"JWToken":getCookie("token"), "MessageId":MsgId })
   socket.emit("MessageDelete", data)

}


function ReplyToMsg(element) {
  if ( numOFReply < 3 ) {
      console.log(element)
      reply = reply + DOMPurify.sanitize(`<div style="border: 2px white solid;">${$(element).html()}</div>`)
      console.log(reply)
      numOFReply = numOFReply + 1
      console.log(numOFReply)
  }
  else {
    alert("you cant make more than 3 replies")
  }
}

