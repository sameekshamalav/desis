chrome.runtime.onMessage.addListener(request => {

    if (request == "OpenPopup") {
  
        chrome.windows.create({
            url: "/html/popup.html",
            type: "popup",
            focused: true,
            width: 300,
            height: 350,
            top: 0,
            left: 1000,
        }, () => {
            console.log("Opened popup!")
        })
  
    }
  
  })