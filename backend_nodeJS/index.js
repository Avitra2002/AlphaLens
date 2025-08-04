//Express app entry point
const express = require('express');
const cors = require('cors');

const summaryRouter = require('./routes/summary');
const insightRouter = require('./routes/insights');
const chatbotRouter = require('./routes/chatbot')

const app = express();
app.use(cors());
app.use(express.json());

app.use('/api/summary', summaryRouter);
app.use('/api/insight', insightRouter);
app.use('/api/chatbot', chatbotRouter)


const PORT = 4000;
app.listen(PORT, () => console.log(`✅ Backend running at http://localhost:${PORT}`));
