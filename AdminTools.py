import mysql.connector



class AdminTools:
    def __init__(self, config):
        self.__config = config
    
    def adminMainpage(self):
        conn = mysql.connector.connect(**self.__config)
        cursor = conn.cursor()
        queries = f'SELECT quizId, status, tittel, antallSpørsmål FROM quizOversikt;'
        results = cursor.execute(queries, multi = True)
        quizOversikt = []
        try: 
            for result in results:
                quizOversikt.append(result.fetchall())
            conn.commit()
            cursor.close()
            conn.close()
        
            return quizOversikt
        except: 
            return False
    
    def createNewQuiz(self, tittel, antallSpørsmål):
        spmInserts = []
        fasitInserts = [] 
            
        for i in range(antallSpørsmål):
            spmInserts.append(f'("spørsmål {i+1}", "enkeltvalgs", (SELECT quizId from\
                            quizOversikt WHERE tittel = "{tittel}" ))')
        for i in range(antallSpørsmål):
            for j in range(3):
                fasitInserts.append(f'((select spørsmålId+{i} from spørsmålsbank where\
                            quizId = (SELECT quizId from quizOversikt WHERE tittel =\
                            "{tittel}") and spørsmål = "spørsmål 1"), "svar{j + 1}")')

        queries = []
        queries.append(f'INSERT INTO quizOversikt(`tittel`, `antallSpørsmål`)\
                            VALUES ("{tittel}", {antallSpørsmål})')
        queries.append(f'INSERT INTO spørsmålsbank(`spørsmål`, `spørsmålstype`,\
                            `quizId`) VALUES {",".join(spmInserts)}')
        queries.append(f'INSERT INTO fasitsvar (`spørsmålId`, `svaralternativ`)\
                            VALUES {",".join(fasitInserts)};')  
        queries = ";".join(queries)

        conn = mysql.connector.connect(**self.__config)
        cursor = conn.cursor()
        try:
            for result in cursor.execute(queries, multi = True):
                pass
        except mysql.connector.Error as err:
            return err
        
        conn.commit()
        cursor.close()
        conn.close()
        return False
    
    def inactivateQuiz(self, quizId):
        conn = mysql.connector.connect(**self.__config)
        cursor = conn.cursor()
        try:
            query = f"UPDATE quizOversikt SET status = 'inaktiv' WHERE quizId = {quizId};"
            cursor.execute(query)
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
                print(err)
            
    def activateQuiz(self, quizId):
        conn = mysql.connector.connect(**self.__config)
        cursor = conn.cursor()
        try:
            query = f"UPDATE quizOversikt SET status = 'aktiv' WHERE quizId = {quizId};"
            cursor.execute(query)
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
                print(err)

    def endQuiz(self, quizId):
        conn = mysql.connector.connect(**self.__config)
        cursor = conn.cursor()
        try:
            query = f"UPDATE quizOversikt SET status = 'ferdig' WHERE quizId = {quizId};"
            cursor.execute(query)
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
                print(err)
    
    def approveQuiz(self, quizId):
        conn = mysql.connector.connect(**self.__config)
        cursor = conn.cursor()
        rowcount = 0
        try:
            
            query = f"UPDATE quizOversikt SET status = 'godkjent' WHERE\
                    quizId = {quizId} and (select count(besvarelse.status)\
                    as uvurdert from besvarelse, spørsmålsbank, quizOversikt, fasitsvar\
                    where quizOversikt.quizId = {quizId} and\
                    besvarelse.svarId = fasitsvar.svarId and fasitsvar.spørsmålId\
                    = spørsmålsbank.spørsmålId and\
                    spørsmålsbank.quizId = quizOversikt.quizId and\
                    besvarelse.status = 'uvurdert') = 0;"
            cursor.execute(query)
            rowcount = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            return rowcount
        except mysql.connector.Error as err:
            print(err)
        return rowcount

    def questionOptions(self, spmId):
        conn = mysql.connector.connect(**self.__config)
        cursor = conn.cursor()
        queries = f'SELECT spørsmål, spørsmålstype, kategori, kommentar FROM spørsmålsbank where\
                    spørsmålId = {spmId}; SELECT riktigGalt, svaralternativ,\
                    svarId FROM spørsmålsbank, fasitsvar where\
                    spørsmålsbank.spørsmålId = fasitsvar.spørsmålId and\
                    fasitsvar.spørsmålId = {spmId};'

        results = cursor.execute(queries, multi = True)
        responds = []
        try:
            for result in results:
                responds.append(result.fetchall())
            cursor.close()
            conn.close()
        except:
            return False
        return responds
    
    def deleteQuestion(self, spmId):
        conn = mysql.connector.connect(**self.__config)
        cursor = conn.cursor()
        try:
            query = f"UPDATE spørsmålsbank SET aktiv = 0 WHERE spørsmålId = {spmId};"
            cursor.execute(query)
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
                print(err)
    
    def restoreQuestion(self, spmId):
        conn = mysql.connector.connect(**self.__config)
        cursor = conn.cursor()
        try:
            query = f"UPDATE spørsmålsbank SET aktiv = 1 WHERE spørsmålId = {spmId};"
            cursor.execute(query)
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(err)

    def updateSpm(self, form, spmId):
        conn = mysql.connector.connect(**self.__config)
        cursor = conn.cursor()
        try:
            queries = f"UPDATE fasitsvar SET svaralternativ = '{form.get('svar1')}',\
                        riktigGalt = {1 if form.get('riktigGalt1') == 'on' else 0}\
                        WHERE svarId = {form.get('id1')};\
                        UPDATE fasitsvar SET svaralternativ = '{form.get('svar2')}',\
                        riktigGalt = {1 if form.get('riktigGalt2') == 'on' else 0}\
                        WHERE svarId = {form.get('id2')};\
                        UPDATE fasitsvar SET svaralternativ = '{form.get('svar3')}', \
                        riktigGalt = {1 if form.get('riktigGalt3') == 'on' else 0}\
                        WHERE svarId = {form.get('id3')};\
                        UPDATE spørsmålsbank SET spørsmål = '{form.get('spørsmål')}',\
                        spørsmålstype = '{form.get('spørsmålstype')}', kategori\
                        = '{form.get('kategori')}' WHERE spørsmålId = {spmId};"
            for result in cursor.execute(queries, multi = True):
                pass
        except mysql.connector.Error as err:
                print(err)
        conn.commit()
        cursor.close()
        conn.close()


    def questionsInQuizOverview(self, quizId):
        conn = mysql.connector.connect(**self.__config)
        cursor = conn.cursor()
        queries = f'SELECT tittel FROM quizOversikt WHERE quizId = {quizId};\
                    SELECT spørsmålId, spørsmål, aktiv FROM spørsmålsbank\
                    WHERE quizId = {quizId};\
                    SELECT brukernavn, id FROM brukere WHERE quizId = {quizId}'
        
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
                    fasitsvar, besvarelse where spørsmålsbank.spørsmålId = \
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

    def viewUserAnswers(self, brukerId):
        conn = mysql.connector.connect(**self.__config)
        cursor = conn.cursor()
        queries = f'select spørsmål from spørsmålsbank;\
                    select brukernavn from brukere where id = {brukerId};\
                    select brukersvar, riktigGalt from besvarelse, fasitsvar,\
                    spørsmålsbank where besvarelse.svarId = fasitsvar.svarId\
                    and fasitsvar.spørsmålid = spørsmålsbank.spørsmålId and\
                    id = {brukerId}'
        results = cursor.execute(queries, multi = True)
        responds = []
        try: 
            for result in results:
                responds.append(result.fetchall())
            cursor.close()
            conn.close()
            if len(responds[1]) == 0:
                return False

            return responds
        except:
            return False
        return responds
    
    def isAdmin(self, username, password):
        try:
            conn = mysql.connector.connect(**self.__config)
            cursor = conn.cursor()
            query = f'SELECT passord FROM adminUser where brukernavn = "{username}";'
            cursor.execute(query)
            passwordFromDB = cursor.fetchall()[0][0]
            conn.commit()
            cursor.close()
            conn.close()
            if passwordFromDB == password:
                return True
        except:
            return False
        return False

    def getQuizId(self, tittel):
        conn = mysql.connector.connect(**self.__config)
        cursor = conn.cursor()
        quizId = 1
        try:
            cursor.execute(f'SELECT quizId from quizOversikt WHERE tittel = "{tittel}";')
            quizId = cursor.fetchall()[0][0]
        except mysql.connector.Error as err:
            return quizId

        conn.commit()
        cursor.close()
        conn.close()
        return quizId
