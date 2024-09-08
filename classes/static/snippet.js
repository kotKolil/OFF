var MsgSnippet = async (Author, Text) => {
    //Author, Text

    var UserData = await UserDataGet(getCookie("token"));
    console.warn(UserData)
    var TheDick =  `
        <div class="comments-container">
            <div class="body">
                <div class="authors">
                    <div class="username"><a href="">${Author}</a></div>
                     <span class="circle-image">
                          <img  src="/media/${UserData[0][5]}" width = "90" height = "90"   />
                      </span>
                </div>
                <div class="content">
                        ${Text}
                    <hr>
                    ${UserData[0][6]}
                </div>
            </div>
        </div>

`
    return await TheDick
}

// var TopicSnippet = async () {

// <div class="comments-container">
// <div class="body">
//     <div class="authors">
//         <div class="username"><a href="">{Username}</a></div>
//         <div>Role</div>
//          <span class="circle-image">
//               <img  src="media/{LogoPath}" width = "90" height = "90"   />
//           </span>
//         <img src="{LogoPath}" alt="">
//         <div>Posts: <u>455</u></div>
//         <div>Points: <u>4586</u></div>
//     </div>
//     <div class="content">
//         {Message}
//         <hr>
//         {Phrase}
//     </div>
// </div>
// </div>
// <!--Reply Area-->
// <div class="comment-area hide" id="reply-area">
// <textarea name="reply" id="" placeholder="reply here ... "></textarea>
// <input type="submit" value="submit">
// </div>


// }
