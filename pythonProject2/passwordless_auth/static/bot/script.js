btn.addEventListener("click",()=>{
            let questionVal = document.getElementById('question').value 
            let url = `http://localhost:3000/data?query=${questionVal}`
            let r = fetch(url)
            r.then((response)=>{
                return response.json()
            }).then((resp)=>{
                console.log(resp)
                resulttext.innerText = resp
                // result.style.display = "block"
                return resp
            })
        })
