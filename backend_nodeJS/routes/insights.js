const express = require('express');
const router = express.Router();

router.post('/', (req, res) => {
  res.json({ message: "LLM insight route not implemented yet." });
});

module.exports = router;
