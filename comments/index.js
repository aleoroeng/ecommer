const express = require('express')
const bodyParser = require('body-parser')
const {randomBytes} = require('crypto')
const app = express()
app.use(bodyParser.json())

const port = 8000
const commentsByPostId = {}

app.get('/posts/:id/comments',(req,res)=>{
    res.send(commentsByPostId[req.params.id] || [] ) 
})

app.post('/posts/:id/comments',(req,res)=>{

    const id = randomBytes(4).toString('hex')
    const content = req.body['content']
    const postId = req.body['post_id']

    const comments = commentsByPostId[req.params.id] || []
    comments.push({id, content})
    commentsByPostId[req.params.id] = comments
    res.status(201).send(commentsByPostId[req.params.id])
})

app.listen(port,()=>{
console.log(`Listening on port ${port}`)
})