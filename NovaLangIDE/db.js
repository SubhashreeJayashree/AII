const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

const db = new sqlite3.Database(path.join(__dirname, 'data.sqlite'));

db.serialize(() => {
  const initSql = fs.readFileSync(path.join(__dirname, 'sql', 'init.sql'), 'utf8');
  db.exec(initSql);
});

module.exports = {
  run(sql, params = []) {
    return new Promise((resolve, reject) => {
      db.run(sql, params, function (err) {
        if (err) reject(err);
        else resolve({ id: this.lastID, changes: this.changes });
      });
    });
  },
  get(sql, params = []) {
    return new Promise((resolve, reject) => {
      db.get(sql, params, (err, row) => (err ? reject(err) : resolve(row)));
    });
  },
  all(sql, params = []) {
    return new Promise((resolve, reject) => {
      db.all(sql, params, (err, rows) => (err ? reject(err) : resolve(rows)));
    });
  }
};
