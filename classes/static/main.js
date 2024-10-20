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
    const userRequest = await fetch(`/api/user?JWToken=${token}`);
  
    if (await userRequest.ok) {
      const userData = await userRequest.json();
      if (Object.keys(userData).length === 0) {
        return "0"; 
      } else {
        return userData;
      }
    } else {
      return "0";
    }
  };


var IsLogged = async (token) => {
  try {
    const response = await fetch(`/api/user/CheckToken`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "JWToken": token
      })
    });

    const JsonData = await response.json();

    if (JsonData[0] == 1) {
      return true;
    } else if (JsonData[0] == 0) { 
      return false;
    }

    return null;

  } catch (error) {
    return false  
  }
};