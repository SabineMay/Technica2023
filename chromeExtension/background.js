
/* 
// Listen for tab updates (e.g., when navigating to a new page)
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === "complete") {
      // Page has finished loading, get the current URL
      const currentUrl = tab.url;
      saveUrlToFile(currentUrl);

        function saveUrlToFile(url) {
            // You can save the URL to a file here, as shown in the previous response
            // For example, use the chrome.downloads API to save it to a file
            // const blob = new Blob([url], { type: 'text/plain' });
            const fileName = 'current_url.txt';
            const downloadUrl = url; 
            const fileContents = `Download URL: ${url}`; // Create a string with the URL

            chrome.downloads.download({
                url: url,
                filename: fileName,
                saveAs: true, // Change to true if you want to prompt the user to choose a download location
            });
        }
    }
})
*/