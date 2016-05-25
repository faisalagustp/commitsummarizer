from django.shortcuts import render
from django.http import HttpResponse
from importer import Importer
from analyzeChange import analyzeChange
from analyzePyCodeChange import analyzePyCodeChange
from cosum.models import Commit, Files


# Create your views here.
def home_page(request):
    commits = Commit.objects.values('nama_project').distinct()
    return render(request, 'home.html',{'commits':commits})

def import_page(request):
    kode = "sukses"
    try:
        if request.method == 'POST':
           # create an object and save to database
           name = request.POST['username']
           project = request.POST['project']
           importer = Importer(name,project)
           name = importer.crawl_git()
    except Exception as e:
        kode = str(e)

    return HttpResponse(kode)

def commit_page(request):
    project = request.GET['project']
    commits = Commit.objects.filter(nama_project=project)

    #melakukan looping untuk setiap commit
    for commit in commits:
        if "" == "":
            files = Files.objects.filter(commit_id=commit.id)
            c = analyzeChange()
            commit.jumlahFile = len(files)
            for berkas in files:
                c.submitFile([berkas.filename,berkas.status,berkas.perubahan])

            c.analyzePyChange()
            c.calculateCommitStereotype()

            commit.generated_comment = c.generateCommitMessage("brief")

    return render(request, 'commit.html',{'project':project, 'commits':commits})

def detail_page(request,commit_id):
    files = Files.objects.filter(commit_id=commit_id)
    commit = Commit.objects.get(id=commit_id)

    c = analyzeChange()
    for berkas in files:
        c.submitFile([berkas.filename,berkas.status,berkas.perubahan])

    c.analyzePyChange()
    c.calculateCommitStereotype()

    commit.generated_comment = c.generateCommitMessage("all")
    commit.generated_tfidf = c.generateCommitMessage("tfidf")
    commit.generated_tfidfmessage = c.generateCommitMessage("tfidfmessage",commit.message)
    commit.save()


    return render(request, 'detail.html',{'files':files, 'commit':commit})
