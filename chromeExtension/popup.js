document.getElementById('downloadBtn').addEventListener('click', function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      let tab = tabs[0];
      let content = `${tab.url}`;
      let blob = new Blob([content], {type: 'text/plain'});
      let url = URL.createObjectURL(blob);

  
      // Generate a unique timestamp
      let timestamp = new Date().getTime();
  
      chrome.downloads.download({
        url: url,
        filename: 'Users/sabinemay/umd-fall-2023/technica2023/urls/websiteURL'+timestamp+'.txt',
        saveAs: false
      });
    });
  });

/* chrome.scripting.executeScript({
    target: { tabId: tabId },
    function: () => {
      return window.location.href;
    },
  }, (result) => {
    const currentUrl = result[0].result;
    document.getElementById('current-url').textContent = currentUrl;
  }); */ 