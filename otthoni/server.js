const express = require("express");
const app = express();
const cors = require("cors");
const mysql = require("mysql");
const bodyParser = require("body-parser");

app.use(bodyParser.json());
app.use(cors()); // CORS engedélyezése

// Adatbázis kapcsolat konfigurálása
const db = mysql.createConnection({
    user: "root",
    host: "127.0.0.1",
    password: "", // Ha van jelszavad, itt add meg
    database: "atletikavb2017" // Az adatbázis neve az SQL dump alapján
});

// Csatlakozás az adatbázishoz
db.connect((err) => {
    if (err) {
        console.error("Adatbázis csatlakozási hiba: ", err);
        return;
    }
    console.log("Sikeresen csatlakozva az adatbázishoz!");
});

// Alapértelmezett végpont
app.get("/", (req, res) => {
    res.send("Fut a backend!");
});

// Versenyszámok lekérdezése, ahol az időtartam több mint 60 perc
app.get("/versenyszamok-tobb-mint-60-perc", (req, res) => {
    const query = `
        SELECT DISTINCT Versenyszam
        FROM versenyekszamok
        WHERE Eredmeny REGEXP '^[0-9]:[0-9]{2}:[0-9]{2}' 
        AND TIME_TO_SEC(
            CASE 
                WHEN LENGTH(Eredmeny) = 7 THEN CONCAT('0', Eredmeny)
                ELSE Eredmeny
            END
        ) > 3600;
    `;

    db.query(query, (err, results) => {
        if (err) {
            console.error("Lekérdezési hiba: ", err);
            res.status(500).json({ error: "Szerver hiba történt a lekérdezés során" });
            return;
        }
        if (results.length === 0) {
            res.status(404).json({ message: "Nincs találat" });
            return;
        }
        res.json(results.map(row => row.Versenyszam));
    });
});

// Szerver indítása
app.listen(3001, () => {
    console.log("Server is running on port 3001");
});