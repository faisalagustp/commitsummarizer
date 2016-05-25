import urllib.request, json, pprint
from cosum.models import Commit, Files

class Importer:
    name = ""
    project = ""

    def __init__(self,name,project):
        self.name = name
        self.project = project

    def crawl_git(self):
        #crawl dari repository, simpen per baris ke database
        isi = ""
        response = urllib.request.urlopen("https://api.github.com/repos/"+self.name+"/"+self.project+"/commits?per_page=100&client_id=8ca1f7d85e6aee485391&client_secret=cccbfee89add2b5154eee95c909c1694428c2cdf").read()
        json_response = json.loads(response.decode('utf-8'))
        for commits in json_response:
            isi += commits["comments_url"]
            commitnya = Commit.objects.create(nama_project = self.name +"/"+self.project, hashnya = commits["sha"],commiter=commits["commit"]["committer"]["name"],message=commits["commit"]["message"])

            urlFiles = commits["url"] + "?client_id=8ca1f7d85e6aee485391&client_secret=cccbfee89add2b5154eee95c909c1694428c2cdf"
            responseFiles = urllib.request.urlopen(urlFiles).read()
            json_files = json.loads(responseFiles.decode('utf-8'))
            for files in json_files["files"]:
                filename = files["filename"]
                status = files["status"]

                perubahan = ""
                try:
                    perubahan = files["patch"]
                except Exception as e:
                    perubahan = ""

                filenya = Files.objects.create(commit = commitnya, filename=filename, status=status, perubahan=perubahan)

        return isi
