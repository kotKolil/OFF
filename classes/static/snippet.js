var MsgSnippet = async (Author, Text) => {
    //Author, Text

    var TheDick =  `
        <div class="comments-container">
            <div class="body">
                <div class="authors">
                    <div class="username"><a href="">${Author.UserId}</a></div>
                     <span class="circle-image">
                          <img  src="/media/${Author.LogoPath}" width = "90" height = "90"   />
                      </span>
                </div>
                <div class="content">
                        ${Text}
                    <hr>
                    ${Author.citate}
                </div>
            </div>
        </div>

`
    return await TheDick
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
