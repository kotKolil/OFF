function getQueryParam(name) {
    const queryString = window.location.search.substring(1);
    const urlParams = new URLSearchParams(queryString);
    return urlParams.get(name);
  }

  function getCookie(cookieName) {
    const name = cookieName + "=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const cookieArray = decodedCookie.split(';');
    
    for (let cookie of cookieArray) {
        while (cookie.charAt(0) == ' ') {
            cookie = cookie.substring(1);
        }
        if (cookie.indexOf(name) == 0) {
            return cookie.substring(name.length, cookie.length);
        }
    }
    return "";
}

var UserDataGet = async (token) => {
    var UserRequest = await fetch("/api/GetUserInfo");
    var UserData = await UserRequest.json
    return UserData
}