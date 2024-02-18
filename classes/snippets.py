def tt_snippet(title, description, topic_num, author):

       return f"""
            <div class="subforum-row">
                <div class="subforum-icon subforum-column center">
                    <i class="fa fa-car center"></i>
                </div>
                <div class="subforum-description subforum-column">
                    <h4><a href="#">Description Title</a></h4>
                    <p>{description}</p>
                </div>
                <div class="subforum-stats subforum-column center">
                    <span>{title}</span>
                </div>
                <div class="subforum-info subforum-column">
                    <br>{author}</small>
                </div>
            </div>
        </div>
    """

def MessageSnippet(LogoPath,Username, Message, Phrase):
       return f"""
 <div class="authors">
                    <div class="username"><a href="">{Username}</a></div>
                    <div>Role</div>
                    <img src="{LogoPath}" alt="">
                </div>
                <div class="content">
                     {Message}
                    <hr>
                    {Phrase}
                    <br>
                </div>
       """
