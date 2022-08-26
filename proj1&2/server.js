const express = require('express');
const app = express();
const path = require('path');
const fs = require('fs');
const { spawnSync } = require('child_process');
const multer = require('multer');
var storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'public//sample_input');
    },
    filename: function (req, file, cb) {
        cb(null, file.originalname);
    }
});
const upload = multer({ storage: storage })
if (fs.existsSync('public//sample_input')) {
    fs.rmSync('public//sample_input', { recursive: true, force: true });
}
if (fs.existsSync("marksheets")) {
    fs.rmSync("marksheets", { recursive: true, force: true });
}
if (fs.existsSync("transcriptsIITP")) {
    fs.rmSync("transcriptsIITP", { recursive: true, force: true });
}
fs.mkdirSync('public//sample_input');

app.use('/static', express.static(path.join(__dirname, 'public')))

// register view engine
app.set('views', path.join(__dirname, 'views'))
app.set('view engine', 'ejs');
app.get('/', (req, res) => {
    res.render('home')
});

var all = 0, r_from = "", r_upto = "", stmp = "", sgn = "", flag1 = 0,
    message1 = 'Upload grades.csv,subject.csv,names_roll.csv,seal,sign then genreate all transcripts or enter ranged input to genreate required transcripts';

app.get('/generateTranscripts', (req, res) => {
    res.render('p1', { message1, r_from, r_upto, flag1 });
});

const p1Upload = upload.fields([{ name: 'grades', maxCount: 1 }, { name: 'names_roll', maxCount: 1 }, { name: 'subject', maxCount: 1 }, { name: 'seal', maxCount: 1 }, { name: 'sign', maxCount: 1 }]);

app.post('/generateTranscripts', p1Upload, async (req, res) => {
    if (req.files.seal) { stmp = req.files.seal[0].originalname }
    if (req.files.sign) { sgn = req.files.sign[0].originalname }
    r_from = req.body.r_from;;
    r_upto = req.body.r_upto;
    if (req.body.rng) {
        all = 0, flag1 = 1;
        const result = spawnSync('python', ['pythonFiles//transcript_Generator.py', r_from, r_upto, all, stmp, sgn]);
        message1 = result.stdout.toString();
        error = result.stderr.toString();
        console.log(error)
    }
    if (req.body.all) {
        all = 1, flag1 = 1;
        const result = spawnSync('python', ['pythonFiles//transcript_Generator.py', r_from, r_upto, all, stmp, sgn]);
        message1 = result.stdout.toString();
        error = result.stderr.toString();
        console.log(error)
    };
    if (req.body.download) {
        return res.download('./transcriptsIITP.zip',);
    }
    res.redirect('/generateTranscripts');
});

var positive = -1, negative = 1, flag = 0,
    message = 'Upload master_roll.csv,respone.csv and fill +ve,-ve marks then generate roll no. wise marksheet or concise marksheet';

app.get('/generateMarksheets', (req, res) => {
    res.render('p2', { flag, positive, negative, message });
});

const p2Upload = upload.fields([{ name: 'master_roll', maxCount: 1 }, { name: 'response', maxCount: 1 }]);
app.post('/generateMarksheets', p2Upload, async (req, res) => {
    positive = req.body.positive;
    negative = req.body.negative;
    if (fs.existsSync('public//sample_input//master_roll.csv')) {
        // path exists
        console.log("exists:", 'public//sample_input//master_roll.csv');
    } else {
        console.log("DOES NOT exist:", 'public//sample_input//master_roll.csv');
    }
    if (req.body.Roll_Number_wise) {
        const result = spawnSync('python', ['pythonFiles//marksheet_Generator.py', positive, negative]);
        message = result.stdout.toString();
        error = result.stderr.toString();
        console.log(error)
        console.log(message)
        console.log("print line 86")
        flag = 1;
    }
    if (req.body.download) {
        return res.download('./marksheets.zip',);
    }
    if (req.body.Email) {
        const result = spawnSync('python', ['pythonFiles//send_Email.py']);
        message = result.stdout.toString();
        error = result.stderr.toString();
        console.log(error);
    }
    res.redirect('/generateMarksheets');
});

// listen for requests
const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Server started running on port ${port}`));