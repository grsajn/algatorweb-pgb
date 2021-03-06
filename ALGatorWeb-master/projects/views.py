# PROBLEMS
import codecs
import os
from pprint import pprint

from django.core.files import File
from django.template.defaulttags import register
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.http import HttpResponse
from os import system
from vision import views
from django.contrib.auth.decorators import login_required,permission_required,user_passes_test

from Classes.FolderScraper import FolderScraper  # scrapes different JSON files and puts them together in objects.
from Classes.GlobalConfig import GlobalConfig
import json


@login_required
def projects(request):
    print()

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
        algdescription=request.POST.get('algdescription')
        algsdescription=request.POST.get('algsdescription')

        if not check_if_project_exists(pname):
            system("java algator.Admin -ca " + pname + " " + aname)
            proj_conf = return_proj_conf_file(pname)
            alg_conf = return_alg_conf_file(pname,aname)
            proj_description_file = open(proj_conf, 'r').read()
            alg_description_file = open(alg_conf, 'r').read()
            proj_json_description = json.loads(proj_description_file)
            alg_json_description = json.loads(alg_description_file)
            proj_json_description["Project"]["Author"]=request.user.username
            alg_json_description["Algorithm"]["Author"]=request.user.username
            proj_json_description["Project"]["Description"]=pdescription
            alg_json_description["Algorithm"]["Description"]=algdescription
            with open(proj_conf, "w") as jsonFile:
                jsonFile.write(json.dumps(proj_json_description))
            with open(alg_conf, "w") as jsonFile:
                jsonFile.write(json.dumps(alg_json_description))
            return redirect('/projects/pdetails?project=' + pname)
#        try:
#            projectConfig = views.get_project_config(pname)
#            projects.append(projectConfig["Name"])
#        except:
#            pass


    return render_to_response(
        'newproject.html',
        context_instance=RequestContext(request)
    )

def return_proj_conf_file(project):
    data_root = GlobalConfig().data_root_path
    return "{0}/PROJ-{1}/proj/{1}.atp".format(data_root, project)

def return_alg_conf_file(proj, alg):
    data_root = GlobalConfig().data_root_path
    print("{0}/PROJ-{1}/algs/ALG-{2}/{2}.atal".format(data_root,proj, alg))
    return "{0}/PROJ-{1}/algs/ALG-{2}/{2}.atal".format(data_root,proj, alg)

def check_if_project_exists(proj):
    data_root = GlobalConfig().data_root_path
    if os.path.exists("{0}/PROJ-{1}".format(data_root,proj)):
        return True
    return False

def check_if_algorithm_exists(proj,alg):
    data_root = GlobalConfig().data_root_path
    if os.path.exists("{0}/PROJ-{1}/algs/ALG-{2}".format(data_root,proj,alg)):
        return True
    return False

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
    pprint(project.html_desc)
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
    data_root = GlobalConfig().data_root_path

    detailed_algorithm_description = codecs.open("{0}/PROJ-{1}/doc/{2}.html".format(data_root, project.name, algorithm.name),'r').read()
    return render_to_response(
        'adetails.html',
        {
            'algorithm': algorithm,
            'project' : project,
            'detailed_algorithm_description': detailed_algorithm_description,

        }
        , context_instance=RequestContext(request)
    )


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
