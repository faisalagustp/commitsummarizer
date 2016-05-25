from analyzePyCodeChange import analyzePyCodeChange
from pprint import pprint


class analyzeChange():
    htmlChange = {}
    cssChange = {}
    jsChange = {}
    confChange = {}
    xmlChange = {}
    pyChange = {}

    methodSet = []
    methodGet = []
    commitStereotypes = []

    miscFiles = 0
    getMethodCount = 0
    setMethodCount = 0
    getSetMethodCount = 0
    accessorMethodCount = 0
    mutatorMethodCount = 0
    importCount = 0
    classCount = 0

    def __init__(self):
        self.htmlChange = {
            'added' : [],
            'removed' : [],
            'modified' : [],
            'renamed' : []
        }
        self.cssChange = {
            'added' : [],
            'removed' : [],
            'modified' : [],
            'renamed' : []
        }
        self.jsChange = {
            'added' : [],
            'removed' : [],
            'modified' : [],
            'renamed' : []
        }
        self.confChange = {
            'added' : [],
            'removed' : [],
            'modified' : [],
            'renamed' : []
        }
        self.xmlChange = {
            'added' : [],
            'removed' : [],
            'modified' : [],
            'renamed' : []
        }
        self.pyChange = {
            'added' : [],
            'removed' : [],
            'modified' : [],
            'renamed' : []
        }

        self.methodGet = []
        self.methodSet = []
        self.commitStereotypes = []

        self.miscFiles = 0
        self.getMethodCount = 0
        self.setMethodCount = 0
        self.getSetMethodCount = 0
        self.accessorMethodCount = 0
        self.mutatorMethodCount = 0
        self.importCount = 0
        self.classCount = 0

    def generateDetailClassOrMethod(self,objects):
        objects["name"] = objects["name"].replace("def","method")
        objects["replacing"] = objects["replacing"].replace("def","method")
        commitMessage = ""
        if objects["status"]=="+":
            commitMessage += "Penambahan " + objects["name"]
        elif objects["status"]=="+":
            commitMessage += "Penghapusan " + objects["name"]
        elif objects["status"]=="":
            commitMessage += "Modifikasi " + objects["name"]
        elif objects["status"]=="R":
            commitMessage += "Penggantian " + objects["replacing"] + " menjadi " + objects["name"]
        commitMessage += " (" + str(objects["plus"]) +" baris ditambahkan dan "+ str(objects["minus"]) +" baris dihapus)\n"
        return commitMessage

    def generateMessageFromPy(self,change,noFile,jenis):
        commitMessage = "\n" + str(noFile) + ". "+jenis+" File " + change[0] + "\n"
        noLevel1 = 1
        #class yang ditambah
        for imported in change[1][2]:
            commitMessage += str(noFile) + "." + str(noLevel1) + ". "
            commitMessage += "Penambahan" if imported["status"]=="+" else "Penghapusan"
            commitMessage += " import kelas "
            importing = imported["line"].split('import')
            commitMessage += importing[-1]
            if imported["line"].startswith("from"):
                commitMessage += " dari module " + importing[0].replace("from","").strip()
            commitMessage += "\n"
            noLevel1 += 1

        for classes in change[1][0]:
            commitMessage += str(noFile) + "." + str(noLevel1) + ". "
            commitMessage += self.generateDetailClassOrMethod(classes)
            noMethod = 1
            for methods in classes["methods"]:
                commitMessage += str(noFile) + "." + str(noLevel1) + "." + str(noMethod) + ". "
                commitMessage += self.generateDetailClassOrMethod(methods)
                noMethod += 1
            noLevel1 += 1

        #method yang ditambah
        for methods in change[1][1]:
            commitMessage += str(noFile) + "." + str(noLevel1) + ". "
            commitMessage += self.generateDetailClassOrMethod(methods)
            noLevel1 += 1
        return commitMessage

    def generateCommitMessage(self):
        dictionary = {
            "Strcture" : "terdiri atas perubahan get dan set saja",
            "State Access" : "secara umum diisi oleh perubahan method accessor",
            "State Update" : "secara umum diisi oleh perubahan method mutator",
            "Large" : "terdiri dari perubahan method get/set dan perubahan method lainnya",
            "Lazy" : "terdiri dari perubahan pasangan get-set saja",
            "Small" : "terdiri dari perubahan method kurang dari tiga",
            "Non" : "tidak terjadi perubahan pada kelas/method dalam kode python",
            "Unidentified" : "perubahan kode python yang tidak dikenali",
            "View" : "Perubahan kode program yang terjadi juga lebih banyak terjadi pada perubahan tampilan",
            "Design" : "Perubahan kode program yang terjadi juga lebih banyak terjadi pada perubahan desain tampilan",
            "Javascript" : "Perubahan kode program yang terjadi juga lebih banyak terjadi pada kode-kode javascript",
            "Konfigurasi" : "Perubahan kode program yang terjadi juga lebih banyak terjadi pada konfigurasi sistem",
            "Konfigurasi XML" : "Perubahan kode program yang terjadi juga lebih banyak terjadi pada konfigurasi sistem berekstensi XML",
            "Miscelanous" : "Perubahan kode program yang terjadi juga lebih banyak terjadi pada file-file yang tidak dikenali",
            "Addition" : "Perubahan kode python lebih banyak terjadi pada penambahan berkas kode program",
            "Renaming" : "Perubahan kode python lebih banyak terjadi pada renaming berkas kode program",
            "Modification" : "Perubahan kode python lebih banyak terjadi pada modifikasi kode program",
            "Removing" : "Perubahan kode python lebih banyak terjadi pada kegiatan penambahan penghapusan kode program"
        }

        commitMessage = "Commit ini adalah "
        if(len(self.commitStereotypes)>1):
            commitMessage += ", ".join(self.commitStereotypes[:-1])
            commitMessage += " dan " + self.commitStereotypes[-1]
        else:
            commitMessage += self.commitStereotypes[0]
        commitMessage += " modifier. Perubahan yang terjadi "
        for stereotype in self.commitStereotypes:
            commitMessage += dictionary[stereotype] + ". "

        commitMessage+= " Detail kegiatan perubahan yang terjadi adalah sebagai berikut:"

        #addition
        noFile = 1
        if len(self.pyChange["added"])>0:
            for change in self.pyChange["added"]:
                commitMessage += self.generateMessageFromPy(change,noFile,"Penambahan")
                noFile+=1

        #penghapusan
        if len(self.pyChange["removed"])>0:
            for change in self.pyChange["removed"]:
                commitMessage += self.generateMessageFromPy(change,noFile,"Penghapusan")
                noFile+=1

        #Modifikasi
        if len(self.pyChange["modified"])>0:
            for change in self.pyChange["modified"]:
                commitMessage += self.generateMessageFromPy(change,noFile,"Pada")
                noFile+=1

        #Renaming
        if len(self.pyChange["renamed"])>0:
            for change in self.pyChange["renamed"]:
                commitMessage += self.generateMessageFromPy(change,noFile,"Penggantian nama")
                noFile+=1

        commitMessage += "\n"

        #filehtml
        if len(self.htmlChange["added"]) != 0:
            commitMessage += "File HTML yang ditambahkan adalah " + ", ".join(self.htmlChange["added"]) + ". "
        if len(self.htmlChange["removed"]) != 0:
            commitMessage += "File HTML yang dihapus adalah " + ", ".join(self.htmlChange["removed"]) + ". "
        if len(self.htmlChange["renamed"]) != 0:
            commitMessage += "File HTML yang diubah namanya adalah " + ", ".join(self.htmlChange["renamed"]) + ". "
        if len(self.htmlChange["modified"]) != 0:
            commitMessage += "File HTML yang dimodifikasi adalah " + ", ".join(self.htmlChange["modified"]) + ". "

        if len(self.cssChange["added"]) != 0:
            commitMessage += "File CSS yang ditambahkan adalah " + ", ".join(self.cssChange["added"]) + ". "
        if len(self.cssChange["removed"]) != 0:
            commitMessage += "File CSS yang dihapus adalah " + ", ".join(self.cssChange["removed"]) + ". "
        if len(self.cssChange["renamed"]) != 0:
            commitMessage += "File CSS yang diubah namanya adalah " + ", ".join(self.cssChange["renamed"]) + ". "
        if len(self.cssChange["modified"]) != 0:
            commitMessage += "File CSS yang dimodifikasi adalah " + ", ".join(self.cssChange["modified"]) + ". "

        if len(self.jsChange["added"]) != 0:
            commitMessage += "File JS yang ditambahkan adalah " + ", ".join(self.jsChange["added"]) + ". "
        if len(self.jsChange["removed"]) != 0:
            commitMessage += "File JS yang dihapus adalah " + ", ".join(self.jsChange["removed"]) + ". "
        if len(self.jsChange["renamed"]) != 0:
            commitMessage += "File JS yang diubah namanya adalah " + ", ".join(self.jsChange["renamed"]) + ". "
        if len(self.jsChange["modified"]) != 0:
            commitMessage += "File JS yang dimodifikasi adalah " + ", ".join(self.jsChange["modified"]) + ". "

        if len(self.confChange["added"]) != 0:
            commitMessage += "File konfigurasi yang ditambahkan adalah " + ", ".join(self.confChange["added"]) + ". "
        if len(self.confChange["removed"]) != 0:
            commitMessage += "File konfigurasi yang dihapus adalah " + ", ".join(self.confChange["removed"]) + ". "
        if len(self.confChange["renamed"]) != 0:
            commitMessage += "File konfigurasi yang diubah namanya adalah " + ", ".join(self.confChange["renamed"]) + ". "
        if len(self.confChange["modified"]) != 0:
            commitMessage += "File konfigurasi yang dimodifikasi adalah " + ", ".join(self.confChange["modified"]) + ". "

        if len(self.xmlChange["added"]) != 0:
            commitMessage += "File XML yang ditambahkan adalah " + ", ".join(self.xmlChange["added"]) + ". "
        if len(self.xmlChange["removed"]) != 0:
            commitMessage += "File XML yang dihapus adalah " + ", ".join(self.xmlChange["removed"]) + ". "
        if len(self.xmlChange["renamed"]) != 0:
            commitMessage += "File XML yang diubah namanya adalah " + ", ".join(self.xmlChange["renamed"]) + ". "
        if len(self.xmlChange["modified"]) != 0:
            commitMessage += "File XML yang dimodifikasi adalah " + ", ".join(self.xmlChange["modified"]) + ". "

        commitMessage += (" Dan perubahan pada " + str(self.miscFiles) + "buah file.")   if self.miscFiles!= 0 else ""
        return commitMessage


    def calculateCommitStereotype(self):
        allMethod = self.getMethodCount + self.setMethodCount + self.accessorMethodCount + self.mutatorMethodCount
        if allMethod < 3 and allMethod > 0 :
            self.commitStereotypes.append("Small")
        elif allMethod == 0 :
            self.commitStereotypes.append("Non")
        elif (self.getMethodCount + self.setMethodCount != 0) and (self.accessorMethodCount + self.mutatorMethodCount == 0):
            self.commitStereotypes.append("Structure")
        elif self.accessorMethodCount >= (2 / 3 * allMethod):
            self.commitStereotypes.append("State Access")
        elif self.mutatorMethodCount >= (2 / 3 * allMethod):
            self.commitStereotypes.append("State Update")
        elif self.getSetMethodCount <= (1 / 5 * allMethod) and allMethod >= 15:
            self.commitStereotypes.append("Large")
        elif self.getSetMethodCount > 0 and allMethod - (2 * self.getSetMethodCount) <= 1 / 3 * allMethod:
            self.commitStereotypes.append("Lazy")
        else :
            self.commitStereotypes.append("Unidentified")

        jumlahPyAdded = len(self.pyChange["added"])
        jumlahPyRemoved = len(self.pyChange["removed"])
        jumlahPyModified = len(self.pyChange["modified"])
        jumlahPyRenamed = len(self.pyChange["renamed"])
        jumlahPy = jumlahPyAdded + jumlahPyModified + jumlahPyRemoved + jumlahPyRenamed

        jumlahHTML = len(self.htmlChange["added"])+len(self.htmlChange["removed"])+len(self.htmlChange["modified"])+len(self.htmlChange["renamed"]);
        jumlahCSS = len(self.cssChange["added"])+len(self.cssChange["removed"])+len(self.cssChange["modified"])+len(self.cssChange["renamed"]);
        jumlahJS = len(self.jsChange["added"])+len(self.jsChange["removed"])+len(self.jsChange["modified"])+len(self.jsChange["renamed"]);
        jumlahCONF = len(self.confChange["added"])+len(self.confChange["removed"])+len(self.confChange["modified"])+len(self.confChange["renamed"]);
        jumlahXML = len(self.xmlChange["added"])+len(self.xmlChange["removed"])+len(self.xmlChange["modified"])+len(self.xmlChange["renamed"]);
        jumlahMISC = self.miscFiles

        if jumlahHTML > jumlahPy:
            self.commitStereotypes.append("View")
        if jumlahCSS > jumlahPy:
            self.commitStereotypes.append("Design")
        if jumlahJS > jumlahPy:
            self.commitStereotypes.append("Javascript")
        if jumlahCONF > jumlahPy:
            self.commitStereotypes.append("Konfigurasi")
        if jumlahXML > jumlahPy:
            self.commitStereotypes.append("Konfigurasi XML")
        if jumlahMISC > jumlahPy:
            self.commitStereotypes.append("Miscelanous")

        if jumlahPyAdded > jumlahPy - jumlahPyAdded:
            self.commitStereotypes.append("Addition")
        if jumlahPyRenamed > jumlahPy - jumlahPyRenamed:
            self.commitStereotypes.append("Renaming")
        if jumlahPyModified > jumlahPy - jumlahPyModified:
            self.commitStereotypes.append("Modification")
        if jumlahPyRemoved > jumlahPy - jumlahPyRemoved:
            self.commitStereotypes.append("Removing")

    def analyzePyChange(self):
        '''
        Setelah semuanya didapatkan, nanti dianalisis untuk menghitung:
        * jumlah method get
        * jumlah method set
        * jumlah pasangan get-set
        * jumlah method acessor
        * jumlah method mutator
        '''
        #untuk added
        for change in self.pyChange["added"]:
            #classRemoved
            self.classCount += len(change[1][0])
            for val in change[1][0]:
                for kelas in change[1][0]:
                    for methods in kelas["methods"]:
                        self.checkMethod(methods)

            #methodRemoved
            for methods in change[1][1]:
                self.checkMethod(methods)

            #countRemoved
            self.importCount += len(change[1][2])

        #untuk removed
        for change in self.pyChange["removed"]:
            #classRemoved
            self.classCount += len(change[1][0])
            for val in change[1][0]:
                for kelas in change[1][0]:
                    for methods in kelas["methods"]:
                        self.checkMethod(methods)

            #methodRemoved
            for methods in change[1][1]:
                self.checkMethod(methods)

            #countRemoved
            self.importCount += len(change[1][2])

        #untuk modified
        for change in self.pyChange["modified"]:
            #classRemoved
            self.classCount += len(change[1][0])
            for val in change[1][0]:
                for kelas in change[1][0]:
                    for methods in kelas["methods"]:
                        self.checkMethod(methods)

            #methodRemoved
            for methods in change[1][1]:
                self.checkMethod(methods)

            #countRemoved
            self.importCount += len(change[1][2])

        for change in self.pyChange["renamed"]:
            #classRemoved
            self.classCount += len(change[1][0])
            for val in change[1][0]:
                for kelas in change[1][0]:
                    for methods in kelas["methods"]:
                        self.checkMethod(methods)

            #methodRemoved
            for methods in change[1][1]:
                self.checkMethod(methods)

            #countRemoved
            self.importCount += len(change[1][2])

        #untuk pasangan getset
        for sm in self.methodSet:
            for gm in self.methodGet:
                if gm == sm :
                    self.getSetMethodCount += 1

    def checkMethod(self,methodnya):
        pureMethodName = methodnya["name"].replace("def ","").split("(")[0]
        parameters = methodnya["name"].replace("def ","").replace(")","").split("(")[-1]
        parameters = parameters.split(",")

        if pureMethodName.lower().startswith("get"):
            self.getMethodCount+=1
            self.methodGet = pureMethodName
        elif pureMethodName.lower().startswith("set"):
            self.setMethodCount+=1
            self.methodSet = pureMethodName
        elif len(parameters) == 0:
            self.accessorMethodCount+=1
        elif len(parameters)== 1:
            if parameters[0] == "self":
                self.accessorMethodCount+=1
            else:
                self.mutatorMethodCount+=1
        else:
            self.mutatorMethodCount+=1

    def submitFile(self,theFile):
        if theFile[0].split(".")[-1]=="py":
            codeChange = theFile[2]
            a = analyzePyCodeChange(theFile[1],codeChange)
            perubahan = [theFile[0],[a.savedClass,a.savedMethods,a.savedImport]]
            self.pyChange[theFile[1]].append(perubahan);
        elif theFile[0].split(".")[-1]=="html":
            self.htmlChange[theFile[1]].append(theFile[0])
        elif theFile[0].split(".")[-1]=="css":
            self.cssChange[theFile[1]].append(theFile[0])
        elif theFile[0].split(".")[-1]=="js":
            self.jsChange[theFile[1]].append(theFile[0])
        elif theFile[0].split(".")[-1]=="conf":
            self.confChange[theFile[1]].append(theFile[0])
        elif theFile[0].split(".")[-1]=="xml":
            self.xmlChange[theFile[1]].append(theFile[0])
        else:
            self.miscFiles += 1
