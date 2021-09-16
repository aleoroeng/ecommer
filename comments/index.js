const express = require('express')
const cors = require('cors')
const {randomBytes} = require('crypto')

const app = express()
app.use(express.json())
app.use(cors())

const port = 8000
const commentsByPostId = {}

app.get('/posts/comments',(req,res)=>{
    res.send(commentsByPostId[req.query['post_id']] || [] ) 
})

app.post('/posts/comments',(req,res)=>{

    const id = randomBytes(4).toString('hex')
    const content = req.body['content']
    const postId = req.query['post_id']

    const comments = commentsByPostId[postId] || []
    comments.push({id, content})
    commentsByPostId[postId] = comments

    res.status(201).send(commentsByPostId[postId])
})

app.listen(port,()=>{
console.log(`Listening on port ${port}`)
})