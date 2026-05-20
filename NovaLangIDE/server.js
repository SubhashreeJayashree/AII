require('dotenv').config();
const express = require('express');
const path = require('path');
const helmet = require('helmet');
const cors = require('cors');
const morgan = require('morgan');

const authRoutes = require('./auth/routes');
const langRoutes = require('./lang/routes');
const { requireAuth } = require('./auth/middleware');

const app = express();

app.use(helmet());
app.use(cors({ origin: true, credentials: true }));
app.use(morgan('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(express.static(path.join(__dirname, 'public')));

app.use('/api/auth', authRoutes);
app.use('/api', langRoutes);

app.get('/api/me', requireAuth, (req, res) => {
  res.json({ userid: req.user.userid, id: req.user.sub });
});

const port = process.env.PORT || 4000;
app.listen(port, () => console.log(NovaLang IDE running at http://localhost:\));
