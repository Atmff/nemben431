const express = require("express");
const app = express();
const cors = require("cors");
const mysql = require("mysql");
const bodyParser = require('body-parser');
const bodyParser = require("body-parser");
app.use(bodyParser.json());

app.use(cors());

const db = mysql.createConnection({
    user: "root",
    host:"127.0.0.1",
    port: 3306,
    password:"orban",
    database:"kozutak",
});

app.get("/", (req, res) => {
    res.send("Express is running");
})