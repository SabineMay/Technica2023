document.getElementById('downloadBtn').addEventListener('click', function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      let tab = tabs[0];
      let content = `${tab.url}`;
      let blob = new Blob([content], {type: 'text/plain'});
      let url = URL.createObjectURL(blob);
  
      chrome.downloads.download({
        url: url,
        filename: 'websiteURL.txt',
        saveAs: true
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