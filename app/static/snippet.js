var MsgSnippet = (Author, element) => {
    //Author, Text

    var MisatoForever =  `
        <div class="comments_container" id = "${element.MessageId}">
            <div class="body">
                <div class="authors">
                    <div class="username"><a href="/UserPage?id=${Author.UserId}">${Author.UserId}</a></div>
                     <span class="circle-image">
                          <img  src="/media/${Author.LogoPath}" width = "90" height = "90"   />
                      </span>
                      <p>Posts: ${Author.NumOfPosts}</p>
                      <button onclick="DeleteMessage('${element.MessageId}')">delete message</button>
                      <button onclick="ReplyToMsg('#${element.MessageId}')">reply to message</button>
                </div>
                <div class="content">
                        ${element.text}
                    <hr>
                    ${Author.citate}
                </div>
            </div>
        </div>

`
    return MisatoForever
}

var TopicSnippet = (title, description, author, TopicId) => {

return `

     <div class="subforum-row" onclick = "window.location.replace('/topic?id=${TopicId}')">
                <div class="subforum-icon subforum-column center">
                    <i class="fa fa-car center"></i>
                </div>
                <div class="subforum-description subforum-column" onclick = "window.location.replace('/topic?id=${TopicId}')">
                    <h4 onclick = "window.location.replace('/topic?id=${TopicId}')"><a href="#">${title}</a></h4>
                    <a href="/topic?id=${TopicId}" ><p>${description}</p> </a>
                </div>
                <div class="subforum-stats subforum-column center" onclick = "window.location.replace('/topic?id=${TopicId}')">
                    <span onclick = "window.location.replace('/topic?id=${TopicId}')">${title}</span>
                </div>
                <div class="subforum-info subforum-column" onclick = "window.location.replace('/topic?id=${TopicId}')">
                    <br>${author}</small>
                </div>
            </div>
        </div>

`

}
