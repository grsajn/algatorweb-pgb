# PROBLEMS

from django.template.defaulttags import register
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse
from os import system
from vision import views

from Classes.FolderScraper import FolderScraper  # scrapes different JSON files and puts them together in objects.

@login_required
def projects(request):

    scraper = FolderScraper()

    return render_to_response(
        'index.html',
        {
            'projects_list': scraper.projects_list,
        }
        , context_instance=RequestContext(request)
    )

@login_required
def newproject(request):
    if (request.POST.get('mybtn')):
        pname=request.POST.get('pname')
        pdescription=request.POST.get('pdescription')
        sdescription=request.POST.get('sdescription')
        aname=request.POST.get('aname')
        alg = str(aname) if aname else 'Testing algorihtm'
        print(alg)
        print(pname)
        system("java algator.Admin -ca " + pname + " " + alg)
#        try:
#            projectConfig = views.get_project_config(pname)
#            projects.append(projectConfig["Name"])
#        except:
#            pass


    return render_to_response(
        'newproject.html',
        context_instance=RequestContext(request)
    )

@login_required
def pdetails(request):
    
    projectName = request.GET.get('project', '')
    
    scraper = FolderScraper()
    project = None
    for proj in scraper.projects_list:
        if proj.name == projectName:
          project = proj
    if project == None:
        return HttpResponse('projectName=' + projectName)

    return render_to_response(
        'pdetails.html',
        {
            'project': project,
            'projects_list': scraper.projects_list,

        }
        , context_instance=RequestContext(request)
    )

# technical details about the project
@login_required
def tdetails(request):
    
    projectName = request.GET.get('project', '')
    
    scraper = FolderScraper()
    project = None
    for proj in scraper.projects_list:
        if proj.name == projectName:
          project = proj
    if project == None:
        return HttpResponse('projectName=' + projectName)

    return render_to_response(
        'tdetails.html',
        {
            'project': project,
        }
        , context_instance=RequestContext(request)
    )

# technical details about the project
@login_required
def results(request):
    
    projectName = request.GET.get('project', '')
    
    scraper = FolderScraper()
    project = None
    for proj in scraper.projects_list:
        if proj.name == projectName:
          project = proj
    if project == None:
        return HttpResponse('projectName=' + projectName)

    return render_to_response(
        'results.html',
        {
            'project': project,
        }
        , context_instance=RequestContext(request)
    )

    
@login_required
def adetails(request):
    
    projectName   = request.GET.get('project', '')
    algorithmName = request.GET.get('algorithm', '')
    
    scraper = FolderScraper()
    
    project = None
    for proj in scraper.projects_list:
        if proj.name == projectName:
          project = proj
    if project == None:
        return HttpResponse('Unknown project: "' + projectName + '"')
    
    algorithm = None
    for alg in project.algorithms:
        if alg.name == algorithmName:
          algorithm = alg 
    if algorithm == None:
        return HttpResponse('Unknown algorithm: "' + projectName + '/' + algorithmName + '"')
    

    return render_to_response(
        'adetails.html',
        {
            'algorithm': algorithm,
            'project' : project,

        }
        , context_instance=RequestContext(request)
    )


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)