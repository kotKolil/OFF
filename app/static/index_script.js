$("document").ready( async () =>
        {
            fetch("/api/topic/all")
            .then( async  (response) => {
                    return response.json()
                }
            )
            .then ( async (data) => {
                data.forEach( (element) => {
                    $("#TopicList").append(TopicSnippet(element.theme, element.about, element.author, element.TopicId))
                });
            }
        )
    }
)
