def tt_snippet(title, description, topic_num):

       return f""" <div class="subforum-title">

        <h1> <a href="">{title}</a></h1>
    </div>
    <div class="subforum-row">
        <div class="subforum-description subforum-column">
            <p>{description}</p>
        </div>
        <div class="subforum-stats subforum-column center">
            <span>{topic_num}</span>
        </div>
    </div>
    """

def mess_snippet():
       pass
