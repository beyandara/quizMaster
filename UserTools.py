import mysql.connector

class UserTools:
    def __init__(self, config):
        self.__config = config
    
    def getQuiz(self, ):
        conn = mysql.connector.connect(**self.__config)
        cursor = conn.cursor()
        # queries = f'select spørsmålsbank.quizId, tittel, count(spørsmål) from \
        #             spørsmålsbank, quizOversikt where quizOversikt.quizId\
        #             = spørsmålsbank.quizId and spørsmålsbank.aktiv = 1 and\
        #             quizOversikt.status = "aktiv" group by quizOversikt.quizId'
        
        queries = f'select spørsmålsbank.quizId, tittel, count(spørsmål), status from\
                    spørsmålsbank, quizOversikt where quizOversikt.quizId\
                    = spørsmålsbank.quizId and spørsmålsbank.aktiv = 1 and\
                    quizOversikt.status = "aktiv" group by quizOversikt.quizId;\
                    \
                    select spørsmålsbank.quizId, tittel, count(spørsmål), status from \
                    spørsmålsbank, quizOversikt where quizOversikt.quizId\
                    = spørsmålsbank.quizId and spørsmålsbank.aktiv = 1 and\
                    quizOversikt.status = "godkjent" group by quizOversikt.quizId;'
                    # \
                    # select count(status) from besvarelse, fasitsvar, spørsmålsbank\
                    # where status = "uvurdert" and besvarelse.svarId =fasitsvar.svarId'
        results = cursor.execute(queries, multi = True)
        quizes = []
        try:
            for result in results:
                quizes.append(result.fetchall())
            cursor.close()
            conn.close()
            print(f'this is quizes: {quizes}')
            return quizes
        except:
            return False
     

    def getQuestions(self, quizId, spmId):
        conn = mysql.connector.connect(**self.__config)
        cursor = conn.cursor()
        queries = f'SELECT spørsmål, spørsmålstype FROM spørsmålsbank where spørsmålId = {spmId} and aktiv = 1;\
                    SELECT svaralternativ, svarId FROM spørsmålsbank, fasitsvar\
                    where spørsmålsbank.spørsmålId = fasitsvar.spørsmålId and\
                    fasitsvar.spørsmålId = {spmId} and aktiv = 1;\
                    SELECT min(spørsmålId) FROM spørsmålsbank WHERE quizId\
                    = {quizId} and aktiv = 1 ;\
                    SELECT max(spørsmålId) FROM spørsmålsbank WHERE quizId\
                    = {quizId} and aktiv = 1;'

        results = cursor.execute(queries, multi = True)
        questions = []
        try:
            for result in results:
                questions.append(result.fetchall())
            cursor.close()
            conn.close()
            return questions
        except:
            return False
        

    def getMaxId(self):
        conn = mysql.connector.connect(**self.__config)
        cursor = conn.cursor()
        try:
            query = f"SELECT max(id) FROM brukere;"
            cursor.execute(query)
            maxId = cursor.fetchall()[0][0]
            conn.commit()
            cursor.close()
            conn.close()
            return maxId
        except mysql.connector.Error as err:
            print(err)
            return 0
        
    def updateAnswer(self, form, dict, userId):
        reqSpmId = form.get('spmId')
        reqSvarId = form.get('svarId')
        svarIds =[str((int(reqSpmId)-1)*3+1), str((int(reqSpmId)-1)*3+2), str((int(reqSpmId)-1)*3+3)]
        if reqSvarId != None:
            dict["users"][userId]["besvarelse"][svarIds[0]] = 0
            dict["users"][userId]["besvarelse"][svarIds[1]] = 0
            dict["users"][userId]["besvarelse"][svarIds[2]] = 0
            dict["users"][userId]["besvarelse"][reqSvarId] = 1
        else:
            dict["users"][userId]["besvarelse"][svarIds[0]] = (0 if form.get(svarIds[0]) == None else 1)
            dict["users"][userId]["besvarelse"][svarIds[1]] = (0 if form.get(svarIds[1]) == None else 1)
            dict["users"][userId]["besvarelse"][svarIds[2]] = (0 if form.get(svarIds[2]) == None else 1)

    def createQuizUser(self, form, quizId, id):
        username = form.get("username")
        conn = mysql.connector.connect(**self.__config)
        cursor = conn.cursor()
        try:
            cursor.execute(f'INSERT INTO brukere(`id`, `brukernavn`, `quizId`) VALUES ({id}, "{username}", {quizId})')
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(err)

    def insertAnswers(self, form, dict, id, userId):
        queries = []
        for besvarelse in dict["users"][userId]["besvarelse"]:
            queries.append(f'({id}, {besvarelse}, {0 if dict["users"][userId]["besvarelse"][besvarelse] == False else 1})')
        print(queries)
        queries = f'INSERT INTO besvarelse(`id`, `svarId`, `brukersvar`) VALUES {",".join(queries)};'
        conn = mysql.connector.connect(**self.__config)
        cursor = conn.cursor()
        try:
            for result in cursor.execute(queries, multi = True):
                pass
        except mysql.connector.Error as err:
            print(err)
        conn.commit()
        cursor.close()
        conn.close()
        del dict["users"][userId]

    def questionsInQuizOverview(self, quizId):
        
        conn = mysql.connector.connect(**self.__config)
        cursor = conn.cursor()
        # queries = f'SELECT tittel FROM quizOversikt WHERE quizId = {quizId};\
        #             SELECT spørsmålId, spørsmål FROM spørsmålsbank\
        #             WHERE quizId = {quizId} AND status = "godkjent";\
        #             SELECT brukernavn, id FROM brukere WHERE quizId = {quizId}'
        
        queries = f'SELECT tittel FROM quizOversikt WHERE quizId = {quizId};\
                    SELECT DISTINCT  spørsmålId, spørsmål FROM spørsmålsbank, besvarelse,\
                    quizOversikt WHERE spørsmålsbank.quizId = {quizId} AND\
                    besvarelse.status = "godkjent" AND quizOversikt.status = "godkjent";'
        
        
        results = cursor.execute(queries, multi = True)
        responds = []
        try:
            for result in results:
                responds.append(result.fetchall())
            cursor.close()
            conn.close()
            return responds
        except:
            return False

    def viewQuestionsReplies(self, spmId):
        conn = mysql.connector.connect(**self.__config)
        cursor = conn.cursor()
        queries = f'select spørsmål from spørsmålsbank where spørsmålId = {spmId};\
                    select brukere.id, brukernavn from brukere, spørsmålsbank, \
                    fasitsvar, besvarelse where besvarelse.status = "godkjent" and spørsmålsbank.spørsmålId = \
                    fasitsvar.spørsmålId and fasitsvar.svarId = \
                    besvarelse.svarId and brukersvar = 1 and fasitsvar.spørsmålId\
                     = {spmId} and brukere.id = besvarelse.id order by brukere.id asc;\
                    select svaralternativ from spørsmålsbank, fasitsvar, besvarelse\
                    where spørsmålsbank.spørsmålId = fasitsvar.spørsmålId and\
                    fasitsvar.svarId = besvarelse.svarId and brukersvar = 1 and\
                    fasitsvar.spørsmålId = {spmId} order by id asc;'
        
        results = cursor.execute(queries, multi= True)
        responds = []
        try: 
            for result in results:
                responds.append(result.fetchall())
            cursor.close()
            conn.close()
            return responds
        except:
            return False


            

    