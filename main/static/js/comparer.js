document.addEventListener('DOMContentLoaded', function() {
    
   document.getElementById('search-text').addEventListener('input', () => monitor_search());
   document.getElementById('search_form').addEventListener('submit', () => submit_search());
})



function monitor_search()
{
    console.log("Input received")
    let searchtext = document.getElementById("search-text").value

    console.time("timespan")
    
    console.log(searchtext)
    if(searchtext.length > 2)
    {   
        
        let api_url = `https://openlibrary.org/search.json?q=`+searchtext
        // fetch open library books
        fetch(api_url)
            .then(res => res.json())
            .then(result => {
                console.log("Results returned: " +result["numFound"])
                let docs = result["docs"]

                let htmltext = ""
                let results_list = []
                
                for (let i = 0; i < docs.length; i++)
                {   
                    try
                    {
                    let title = docs[i]["title"]
                    let author = docs[i]["author_name"]
                    htmltext = htmltext+`<option value="${title} by ${author}">`
                    results_list.push(htmltext)
                    }
                    catch(e)
                    {
                        console.log("failed" + e)
                    }
                    
                    if(i>12){break;}
                }
                
                try
                {
                document.getElementById("search-suggestions").innerHTML = htmltext 
                }
                catch(e)
                {
                    console.log("failed" + e)
                }
                
                }).catch(err => console.log(err));
                
        
    }
   console.timeEnd("timespan")      
}

function submit_search()
{   
    console.log("Form Submitted")
    event.preventDefault()
    
    fetch('/search_book', {
        method: 'POST',
        body: JSON.stringify({
        "search_text": "search_text"
        })
    }).then(response => response.json())
    .then(data => {
        
    });
}


