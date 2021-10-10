document.addEventListener('DOMContentLoaded', function() {

    document.getElementById('search-text').addEventListener('input', () => monitor_search());
    //document.getElementById('search_form').addEventListener('submit', () => submit_search());

})



function monitor_search() {

    /**
     * Function constantly monitors search text input field and determines whether it needs to suggest user resutls based on inputs
     */

    let searchtext = document.getElementById("search-text").value;


    if (searchtext.length % 2 == 0) {

        let apiUrl = `https://www.googleapis.com/books/v1/volumes?q=` + searchtext;
        // fetch open library books
        fetch(apiUrl)
            .then(res => res.json())
            .then(result => {
                let items = result["items"];

                let htmlText = "";
                let resultsList = [];

                for (let i = 0; i < items.length; i++) {
                    try {
                        let volumeInfo = items[i]['volumeInfo'];
                        let title = volumeInfo["title"];
                        let authors = volumeInfo["authors"];
                        htmlText = htmlText + `<option value="${title} by ${authors}">`;
                        resultsList.push(htmlText);
                    }
                    catch (e) {
                        console.log("failed" + e);
                    }

                    if (i > 12) { break; }
                }

                try {
                    document.getElementById("search-suggestions").innerHTML = htmlText;
                }
                catch (e) {
                    console.log("failed" + e);
                }

            }).catch(err => console.log(err));


    }

}
