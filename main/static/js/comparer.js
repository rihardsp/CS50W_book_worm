document.addEventListener('DOMContentLoaded', function() {

    document.getElementById('search-text').addEventListener('input', () => monitor_search());
    //document.getElementById('search_form').addEventListener('submit', () => submit_search());

})



function monitor_search() {

    let searchtext = document.getElementById("search-text").value


    if (searchtext.length % 2 == 0) {

        let api_url = `https://www.googleapis.com/books/v1/volumes?q=` + searchtext
        // fetch open library books
        fetch(api_url)
            .then(res => res.json())
            .then(result => {
                let items = result["items"]

                let htmltext = ""
                let results_list = []

                for (let i = 0; i < items.length; i++) {
                    try {
                        let volumeInfo = items[i]['volumeInfo']
                        let title = volumeInfo["title"]
                        let authors = volumeInfo["authors"]
                        htmltext = htmltext + `<option value="${title} by ${authors}">`
                        results_list.push(htmltext)
                    }
                    catch (e) {
                        console.log("failed" + e)
                    }

                    if (i > 12) { break; }
                }

                try {
                    document.getElementById("search-suggestions").innerHTML = htmltext
                }
                catch (e) {
                    console.log("failed" + e)
                }

            }).catch(err => console.log(err));


    }
    console.timeEnd("timespan")
}

function submit_search() {
    event.preventDefault()

    fetch('/search_book', {
        method: 'POST',
        body: JSON.stringify({
            "search_text": "search_text"
        })
    })

}

`
}).then(response => response.json())
    .then(data => {
        
    });
    
    `
