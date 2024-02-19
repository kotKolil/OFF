def tt_snippet(title, description, author, TopicId):

       return f"""
            <div class="subforum-row" onclick = "window.location.replace('/topic?id={TopicId}')">
                <div class="subforum-icon subforum-column center">
                    <i class="fa fa-car center"></i>
                </div>
                <div class="subforum-description subforum-column" onclick = "window.location.replace('/topic?id={TopicId}')">
                    <h4 onclick = "window.location.replace('/topic?id={TopicId}')"><a href="#">{title}</a></h4>
                    <a href="/topic?id={TopicId}" ><p>{description}</p> </a>
                </div>
                <div class="subforum-stats subforum-column center" onclick = "window.location.replace('/topic?id={TopicId}')">
                    <span onclick = "window.location.replace('/topic?id={TopicId}')">{title}</span>
                </div>
                <div class="subforum-info subforum-column" onclick = "window.location.replace('/topic?id={TopicId}')">
                    <br>{author}</small>
                </div>
            </div>
        </div>
    """

def MessageSnippet(LogoPath,Username, Message, Phrase):

       return f"""
        <div class="comments-container">
            <div class="body">
                <div class="authors">
                    <div class="username"><a href="">{Username}</a></div>
                    <div>Role</div>
                     <span class="circle-image">
                          <img  src="media/{LogoPath}" width = "90" height = "90"   />
                      </span>
                    <img src="{LogoPath}" alt="">
                    <div>Posts: <u>455</u></div>
                    <div>Points: <u>4586</u></div>
                </div>
                <div class="content">
                    {Message}
                    <hr>
                    {Phrase}
                </div>
            </div>
        </div>
        <!--Reply Area-->
        <div class="comment-area hide" id="reply-area">
            <textarea name="reply" id="" placeholder="reply here ... "></textarea>
            <input type="submit" value="submit">
        </div>

"""

