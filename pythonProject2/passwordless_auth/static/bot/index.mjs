import { ChatGPTAPIBrowser } from 'chatgpt'
import express from 'express'
import dotenv from 'dotenv'
dotenv.config()
const app = express()
const port = 3000

app.get('/', (req, res) => {
  res.sendFile('D:/Youtube/chatgpt-clone/index.html')
})
app.get('/data', async (req, res) => {
    // console.log(req.query) //Just to try
  const api = new ChatGPTAPIBrowser({
    //Give credintials
    email: process.env.OPENAI_EMAIL,
    password: process.env.OPENAI_PASSWORD
  })
  await api.initSession()
  
  const result = await api.sendMessage(req.query.query)
  res.json(result.response)
})

app.listen(port, () => {
  console.log(`ChatGPT app listening on port ${port} AND That is present at http://localhost:${port}`)
})
