from flask import Flask, render_template, request, redirect, session
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import secrets
from config import config
from useful import isInt
from AdminTools import AdminTools
from UserTools import UserTools
from adminUser import AdminUser


app = Flask(__name__)
adminTools = AdminTools(config)
userTools = UserTools(config)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(username):
    return AdminUser(username)

quizuserdict = {"users":{}, "nextId": userTools.getMaxId()+1}


@app.route('/')
def index():
    return render_template('index.html', msg = 'Velkommen')

# main page for admins
@app.route('/quizadmin/')
@login_required
def quizAdmin():
    quizOversikt = adminTools.adminMainpage()
   
    quizOversikt = [quiz for quiz in quizOversikt[0]]
    if "msg" in session:
        msg = session.pop("msg")
        return render_template('quizoversiktadmin.html', quizes = quizOversikt, msg = msg) 


   
    return render_template('quizoversiktadmin.html', quizes = quizOversikt)


@app.route('/newquizadmin', methods = ["GET", "POST"])
@login_required
def newquiz():
    if request.method == "POST": 
        tittel = request.form.get('tittel')
        antallSpørsmål = request.form.get('antallSpørsmål')
        if isInt(antallSpørsmål) and 16 > int(antallSpørsmål) > 4:
            antallSpørsmål = int(antallSpørsmål)
            error = adminTools.createNewQuiz(tittel, antallSpørsmål)
            if error:
                return render_template('newquiz.html', error = error)
            quizId = adminTools.getQuizId(tittel)  
            return redirect(f'/quizadmin/{quizId}')
        return redirect(f'/quizadmin')
    return render_template('newquiz.html')


@app.route('/inactivatequiz/<quizId>')
@login_required
def inactivateQuiz(quizId):
   adminTools.inactivateQuiz(quizId)
   return redirect(f'/quizadmin/')


@app.route('/activatequiz/<quizId>')
@login_required
def activateQuiz(quizId):
    adminTools.activateQuiz(quizId)
    return redirect(f'/quizadmin/')

@app.route('/endquiz/<quizId>')
@login_required
def endQuiz(quizId):
    adminTools.endQuiz(quizId)
    return redirect(f'/quizadmin/')

@app.route('/approvequiz/<quizId>')
@login_required
def approveQuiz(quizId):
    success = adminTools.approveQuiz(quizId)      
    if not success:
        session["msg"] = "Kan ikke godkjenne quizen" 
    return redirect(f'/quizadmin/')


# page to delete or edit a specified question
@app.route('/spmadminedit/<quizId>/<spmId>')
@login_required
def questionEdit(spmId, quizId):

    if not isInt(spmId) or not isInt(quizId):
        return redirect(f'/quizuser')
    
    responds = adminTools.questionOptions(spmId)
    sporsmal, svarAlternativer = responds
    if sporsmal != []:
        kategori = [sporsmal[2] for sporsmal in sporsmal]
        sporsmal = [sporsmal for sporsmal in sporsmal][0]
        print(sporsmal)
        svarAlternativer = [svarAlternativ for svarAlternativ in svarAlternativer]

    return render_template('spmadminedit.html', quizId = quizId, spmId = spmId,\
                            sporsmal = sporsmal, svarAlternativer = svarAlternativer,\
                            kategori = kategori[0])


@app.route('/deleteSpm/<quizId>/<spmId>')
@login_required
def deleteSpm(quizId, spmId):
    adminTools.deleteQuestion(spmId)
    
    return redirect(f'/quizadmin/{quizId}')


@app.route('/restoreSpm/<quizId>/<spmId>')
@login_required
def restoreSpm(quizId, spmId):
    adminTools.restoreQuestion(spmId) 
    return redirect(f'/quizadmin/{quizId}')


@app.route('/update/<spmId>',methods=["GET", "POST"])
@login_required
def update(spmId):
    if request.method == "POST":
        adminTools.updateSpm(request.form, spmId)
        return redirect(f'/quizadmin/{request.form.get("quizId")}')


# Admins view of a specified quiz;  (option to edit or view) questions and users who completed the quiz
@app.route('/quizadmin/<quizId>')
@login_required
def adminuse(quizId):
    responds = adminTools.questionsInQuizOverview(quizId)
    if not responds:
        return redirect('/quizadmin')
    
    tittel, sporsmal, brukere = responds
    tittel = tittel[0][0]
    sporsmal = [sporsmal for sporsmal in sporsmal]
    bruker = [brukere for brukere in brukere]
    
    return render_template('adminquiz.html', tittel = tittel,\
                            sporsmaler = sporsmal, brukere = bruker, quizId = quizId)


# page to view all answers commited to a specified question id
@app.route('/spmadmin/<spmId>')
# @login_required
def adminspm(spmId):
    responds = adminTools.viewQuestionsReplies(spmId)
    if not responds:
        return redirect('/quizadmin')
     
    try:
        sporsmal, id, brukersvar = responds
        sporsmal = sporsmal[0]
        id = [id for id in id]
        brukersvar = [brukersvar for brukersvar in brukersvar]
        zipped = zip(id, brukersvar)
    except:
        return redirect('/quizadmin')

    return render_template('questionAnswers.html', sporsmal = sporsmal, zipped = zipped)


# page to view questions answered by a specified user
@app.route('/adm/user-<brukerId>')
@login_required
def usersubmits(brukerId): 
    responds = adminTools.viewUserAnswers(brukerId)
    if not responds:
        return redirect('/quizadmin')
    
    sporsmal, brukernavn, brukersvar = responds
    sporsmal = [sporsmal[0] for sporsmal in sporsmal]
    riktigGalt = [(brukersvar[i*3][1],brukersvar[i*3+1][1],brukersvar[i*3+2][1])\
                    for i in range(len(brukersvar)//3)]
    brukernavn = brukernavn[0][0]
    brukersvar = [(brukersvar[i*3][0],brukersvar[i*3+1][0],brukersvar[i*3+2][0])\
                    for i in range(len(brukersvar)//3)]

    zipped = zip(sporsmal, riktigGalt, brukersvar)
    return render_template('userSubmits.html', zipped = zipped, brukerId = brukerId, brukernavn = brukernavn)


# main page for users 
@app.route('/quizuser')
@app.route('/quizuser/') 
def quizUser():
    getQuizes = userTools.getQuiz()
    if not getQuizes:
        return redirect('/')
    activeQuiz, outdatedQuiz = [quiz for quiz in getQuizes]
    

    return render_template('quizoversiktuser.html', activeQuiz = activeQuiz, outdatedQuiz = outdatedQuiz)

# svarer på quiz
@app.route('/quizuser/<quizId>/<spmId>/', methods=["GET", "POST"])
def user(quizId, spmId):
    quizId = quizId
    spmId = spmId
    if "quizId" in session:
        quizId = session.pop("quizId")
    if "spmId" in session:
        spmId = session.pop("spmId")
    if not (isInt(quizId) and isInt(spmId)):
        return redirect(f'/quizuser')
    username = None
    userId = None
    if request.method == "POST":
        if "userId" in session:
            userId = session["userId"]
            username = session["username"]
            userTools.updateAnswer(request.form, quizuserdict, userId)
        else:
            username = session["username"] = request.form.get("username")
            userId = session["userId"] = secrets.token_hex(16)
            quizuserdict["users"][userId] = {"brukernavn":username,\
                        "quizId":quizId, "besvarelse": {}}
        # userId = request.form.get("userId")
        # username = request.form.get("username")
        # if not userId:
        #     # Create the user in dictionary
        #     userId = secrets.token_hex(16)
        #     quizuserdict["users"][userId] = {"brukernavn":username,\
        #                 "quizId":quizId, "besvarelse": {}}
        # else:
        #     userTools.updateAnswer(request.form, quizuserdict)
        next = request.form.get('next')
        svar = request.form.get('svar')
        if svar:
            # Send/lagre
            id = quizuserdict["nextId"]
            quizuserdict["nextId"] += 1
            userTools.createQuizUser(request.form, quizId, id)
            userTools.insertAnswers(request.form, quizuserdict, id, userId)
            if "quizId" in session:
                session.pop("quizId")
            if "userId" in session:
                session.pop("userId")
            if "username" in session:
                session.pop("username")
            return redirect(f'/completed')
        getQuestions = userTools.getQuestions(quizId, spmId)
        if not getQuestions:
            return redirect('/quizuser')
        sporsmal, svarAlternativer, minId, maxId = getQuestions
        if sporsmal != []:
            sporsmalstype = sporsmal[0][1]
            sporsmal = sporsmal[0][0]
            svarAlternativer = [svarAlternativ for svarAlternativ in svarAlternativer]
        else:
            sporsmalstype = sporsmal
            sporsmal = sporsmal    
        minId = minId[0][0]
        maxId = maxId[0][0]
        template = 'flervalgsquiz.html'
        if sporsmalstype == 'enkeltvalgs':
            template = 'enkeltvalgs.html'
        elif sporsmalstype == 'essay':
            template = 'essay.html'
        
        # Return correct page and variables
        if spmId == str(minId):
            return render_template(template, quizId = quizId, spmId = spmId,\
                                    sporsmal = sporsmal, svarAlternativer = svarAlternativer,
                                    next = str(int(spmId)+1), username = username, userId = userId)
        if spmId == str(maxId):
            return render_template(template, quizId = quizId, spmId = spmId,\
                                    sporsmal = sporsmal, svarAlternativer = svarAlternativer,\
                                    next = str(int(spmId)+1), svar = quizId, \
                                    username = username, userId = userId)
        if int(spmId) < minId:
            return render_template(f'/pickusername.html', quizId = quizId, spmId = minId)
        if int(spmId) > maxId:
            return redirect(f'/quizuser/{quizId}/{minId}')
        if sporsmal == []:
            session["quizId"] = quizId
            session["spmId"] = str(int(spmId)+1)
            return redirect(f'/quizuser/{quizId}/{str(int(spmId)+1)}')
        if template == "essay.html":
            return render_template(template, sporsmal = sporsmal)
        
        return render_template(template, quizId = quizId, spmId = spmId, \
                                sporsmal = sporsmal, svarAlternativer = svarAlternativer,\
                                next = str(int(spmId)+1), username = username, userId = userId)
    getQuestions = userTools.getQuestions(quizId, spmId)
    if not getQuestions:
        return redirect('/quizuser')
    sporsmal, svarAlternativer, minId, maxId = getQuestions
    
    if sporsmal != []:
        sporsmalstype = sporsmal[0][1]
        sporsmal = sporsmal[0][0]
        svarAlternativer = [svarAlternativ for svarAlternativ in svarAlternativer]
    else:
        sporsmalstype = sporsmal
        sporsmal = sporsmal   

    minId = minId[0][0]
    maxId = maxId[0][0]
    template = 'flervalgsquiz.html'
    if sporsmalstype == 'enkeltvalgs':
        template = 'enkeltvalgs.html'
    elif sporsmalstype == 'essay':
        template = 'essay.html'

    # Return correct page and variables
    if spmId == str(minId):
        return render_template(template, quizId = quizId, spmId = spmId,\
                                sporsmal = sporsmal, svarAlternativer = svarAlternativer,\
                                next = str(int(spmId)+1))
    if spmId == str(maxId):
        return render_template(template, quizId = quizId, spmId = spmId, sporsmal = sporsmal,\
                                svarAlternativer = svarAlternativer,  svar = quizId, next = str(int(spmId)+1))
    if int(spmId) < minId:
        return render_template(f'/pickusername.html', quizId = quizId, spmId = minId)
    if int(spmId) > maxId:
        return redirect(f'/quizuser/{quizId}/{minId}')
    if sporsmal == []:
        session["quizId"] = quizId
        session["spmId"] = str(int(spmId)+1)
        return redirect(f'/quizuser/{quizId}/{str(int(spmId)+1)}')
    return render_template(template, quizId = quizId, spmId = spmId, sporsmal = sporsmal,\
                            svarAlternativer = svarAlternativer, next = str(int(spmId)+1))      


# User oversikt over ferdige quizer!!
@app.route('/outdatedQuiz/<quizId>', methods=["GET", "POST"])
def outdatedQuiz(quizId):
    responds = userTools.questionsInQuizOverview(quizId)
    if not responds:
        return redirect('/quizadmin')
    
  
    tittel, sporsmal = responds
    tittel = tittel[0][0]
    sporsmal = [sporsmal for sporsmal in sporsmal]
    
  
 
    
    return render_template('outdatedQuizUser.html', tittel = tittel,\
                            sporsmaler = sporsmal,quizId = quizId)


@app.route('/outdatedQuiz/<quizId>/<spmId>')
def viewOutdatedQuestion(quizId, spmId):
    responds = userTools.viewQuestionsReplies(spmId)
    
    if not responds:
        return redirect('/quizadmin')
     
    try:
        sporsmal, id, brukersvar = responds
        sporsmal = sporsmal[0]
        id = [id for id in id]
        brukersvar = [brukersvar for brukersvar in brukersvar]
        zipped = zip(id, brukersvar)
    except:
        return redirect('/quizuser')

    return render_template('USERquestionsAnswered.html', sporsmal = sporsmal, zipped = zipped)




@app.route('/completed')
def userComplete():
    return render_template('completedquiz.html')
    

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST": 
        username = request.form.get('username')
        password = request.form.get('password')
        if adminTools.isAdmin(username,password):
            login_user(AdminUser(username), remember=True)
            return redirect('/quizadmin')
    
    return render_template('login.html', title = 'Sign In')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.errorhandler(401)
def custom_401(error):
    return render_template('error.html')

app.secret_key = secrets.token_urlsafe(16)


if __name__ == "__main__":
    app.run(debug=True)
