
"""
    Rule analisis File Yang Dimodifikasi/direname
    *) Berbeda dengan Java, Method bisa memiliki kelas ataupun tidak
    *) Untuk setiap kelas yang terjadi perubahan,
       catat jumlah baris yang plus ataupun minus (yang mengandung karakter lebih dari 2)
       (tanpa method)
       Sturktur data:
       name kelas : {
            status : [ditambah, dikurangi, direname, atau netral]
            name_sebelum : jika rename
            baris plus = [angka]
            baris minus = [angka]
            method yang diubah = {
                name_method :{
                    status : [ditambah, dikurangi, direname, atau netral]
                    name_sebelum : jika rename
                    baris plus = [angka]
                    baris minus = [angka]
                }
            }
       }
    *) Untuk setiap method yang mengalami perubahan, catat sama seperti sebelumnya
    *) sesuatu dibilang rename kalau tidak ada jeda antar + dan -
    *) komentar adalah sesuatu yang diawali pagar atau kutip tiga kali, isinya diabaikan
    *) current def/class bisa ada di setelah @@

"""


class analyzePyCodeChange():
    savedMethods = []
    savedClass = []
    savedImport = []

    def __init__(self,status,codeChange):
        self.savedClass = {}
        self.savedMethods = []
        self.savedImport = []

        codeChange = codeChange.split('\n')
        self.changePy(codeChange)

    def cleanUp(self,isMethod):
        if isMethod:
            var = {
                "name" : "",
                "replacing" : "",
                "status" : "",
                "plus" : 0,
                "minus" : 0
            }
        else:
            var = {
                "name" : "",
                "replacing" : "",
                "status" : "",
                "plus" : 0,
                "minus" : 0,
                "methods" : []
            }

        return var

    def changePy(self,codeChange):
        classActive = False
        savedMethods = []
        savedClass = []
        savedImport = []

        isRenaming = False
        currentMethod = {
            "name" : "",
            "status" : "",
            "replacing" : "",
            "plus" : 0,
            "minus" : 0
        }

        currentClass = {
            "name" : "",
            "replacing" : "",
            "status" : "",
            "plus" : 0,
            "minus" : 0,
            "methods" : []
        }

        isChanging = False
        isMethod = False
        onClass = False
        isReplacing = False

        for line in codeChange:
            if line.startswith('@@ '):
                #cek apakah ada current class/def
                current = line.split('@@')
                if len(current) == 3:
                    line = current[2]

            lineStatus = ""
            if line.startswith("+"):
                lineStatus = "+"
                line = line.replace("+","",1)
            elif line.startswith("-"):
                lineStatus = "-"
                line = line.replace("-","",1)
            else:
                isReplacing = False
            line = line.strip()
            onReplace = False
            if line.startswith("def") or line.startswith("class"):
                if lineStatus=="-":
                    isReplacing=True
                elif lineStatus=="+":
                    if isReplacing:
                        if isMethod:
                            if line.startswith("def"):
                                onReplace = True
                                currentMethod["replacing"] = currentMethod["name"]
                                currentMethod["name"] = line
                                currentMethod["status"] = "R"
                        else:
                            if line.startswith("class"):
                                onReplace = True
                                currentClass["replacing"] = currentClass["name"]
                                currentClass["name"] = line
                                currentClass["status"] = "R"


                if isChanging == True and onReplace == False:
                    if isMethod and onClass:
                        currentClass["methods"].append(currentMethod)
                        currentMethod = self.cleanUp(True)
                    elif isMethod and not onClass:
                        savedMethods.append(currentMethod)
                        currentMethod = self.cleanUp(True)

                    if line.startswith("class") and onClass:
                        savedClass.append(currentClass)
                        currentClass = self.cleanUp(False)

                isChanging = False;

                if line.startswith("def"):
                    isMethod = True
                    currentMethod["name"] = line
                    currentMethod["status"] = lineStatus if currentMethod["status"]=="" else currentMethod["status"]
                if line.startswith("class"):
                    isMethod = False
                    onClass = True
                    currentClass["name"] = line
                    currentClass["status"] = lineStatus if currentClass["status"]=="" else currentClass["status"]

            if isChanging == False and (lineStatus == "+" or lineStatus=="-"):
                isChanging = True

            if line.startswith("import") or line.startswith("from"):
                if lineStatus == "+" or lineStatus == "-":
                    importing = {
                        'line' : line,
                        'status' : lineStatus
                    }
                    savedImport.append(importing)

            if len(line)<3:
                if lineStatus=="+":
                    if isMethod:
                        currentMethod["plus"] += 1
                    else:
                        currentClass["plus"] += 1
                elif lineStatus=="-":
                    if isMethod:
                        currentMethod["minus"] += 1
                    else:
                        currentClass["minus"] += 1

        if isMethod and onClass and (currentMethod["plus"]>0 or currentMethod["minus"]>0):
            currentClass["methods"].append(currentMethod)
            currentMethod = self.cleanUp(True)
        elif isMethod and not onClass and (currentMethod["plus"]>0 or currentMethod["minus"]>0):
            savedMethods.append(currentMethod)
            currentMethod = self.cleanUp(True)

        if onClass and (currentClass["plus"]>0 or currentClass["minus"]>0 or len(currentClass["methods"])>0):
            savedClass.append(currentClass)
            currentClass = self.cleanUp(True)

        self.savedClass = savedClass
        self.savedMethods = savedMethods
        self.savedImport = savedImport
