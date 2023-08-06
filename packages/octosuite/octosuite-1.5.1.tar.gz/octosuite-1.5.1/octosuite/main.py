'''
            octosuite Advanced Github OSINT Framework
                     Copyright (C) 2022  Richard Mwewa

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
'''


import os
import logging
import requests
import platform
import subprocess
from pprint import pprint
from datetime import datetime
from octosuite import colors,banner
      
        
def run():
    # Define attributes and dictionaries
    # Path attribute
    path_attrs = ['size','type','path','sha','html_url']
    # Path attribute dictionary
    path_attr_dict = {'size': 'Size (bytes)',
                                             'type': 'Type',
                                             'path': 'Path',
                                             'sha': 'SHA',
                                             'html_url': 'URL'}
                                             
    # Organization attributes
    org_attrs = ['avatar_url','login','id','node_id','email','description','blog','location','followers','following','twitter_username','public_gists','public_repos','type','is_verified','has_organization_projects','has_repository_projects','created_at','updated_at']
    # Organization attribute dictionary
    org_attr_dict = {'avatar_url': 'Profile Photo',
                                           'login': 'Username',
                                           'id': 'ID#',
                                           'node_id': 'Node ID',
                                           'email': 'Email',
                                           'description': 'About',
                                           'location': 'Location',
                                           'blog': 'Blog',
                                           'followers': 'Followers',
                                           'following': 'Following',
                                           'twitter_username': 'Twitter Handle',
                                           'public_gists': 'Gists (public)',
                                           'public_repos': 'Repositories (public)',
                                           'type': 'Account type',
                                           'is_verified': 'Is verified?',
                                           'has_organization_projects': 'Has organization projects?',
                                           'has_repository_projects': 'Has repository projects?',
                                           'created_at': 'Created at',
                                           'updated_at': 'Updated at'}
                                           
    # Repository attributes
    repo_attrs = ['id','description','forks','allow_forking','fork','stargazers_count','watchers','license','default_branch','visibility','language','open_issues','topics','homepage','clone_url','ssh_url','private','archived','has_downloads','has_issues','has_pages','has_projects','has_wiki','pushed_at','created_at','updated_at']
    # Repository attribute dictionary
    repo_attr_dict = {'id': 'ID#',
                                              'description': 'About',
                                              'forks': 'Forks',
                                              'allow_forking': 'Is forkable?',
                                              'fork': 'Is fork?',
                                              'stargazers_count': 'Stars',
                                              'watchers': 'Watchers',
                                              'license': 'License',
                                              'default_branch': 'Branch',
                                              'visibility': 'Visibility',
                                              'language': 'Language(s)',
                                              'open_issues': 'Open issues',
                                              'topics': 'Topics',
                                              'homepage': 'Homepage',
                                              'clone_url': 'Clone URL',
                                              'ssh_url': 'SSH URL',
                                              'private': 'Is private?',
                                              'archived': 'Is archived?',
                                              'is_template': 'Is template?',
                                              'has_wiki': 'Has wiki?',
                                              'has_pages': 'Has pages?',
                                              'has_projects': 'Has projects?',
                                              'has_issues': 'Has issues?',
                                              'has_downloads': 'Has downloads?',
                                              'pushed_at': 'Pushed at',
                                              'created_at': 'Created at',
                                              'updated_at': 'Updated at'}
                                              
    # Profile attributes
    profile_attrs = ['avatar_url','login','id','node_id','bio','blog','location','followers','following','twitter_username','public_gists','public_repos','company','hireable','site_admin','created_at','updated_at']
    # Profile attribute dictionary                                      
    profile_attr_dict = {'avatar_url': 'Profile Photo',
                                             'login': 'Username',
                                             'id': 'ID#',
                                             'node_id': 'Node ID',
                                             'bio': 'Bio',
                                             'blog': 'Blog',
                                             'location': 'Location',
                                             'followers': 'Followers',
                                             'following': 'Following',
                                             'twitter_username': 'Twitter Handle',
                                             'public_gists': 'Gists (public)',
                                             'public_repos': 'Repositories (public)',
                                             'company': 'Organization',
                                             'hireable': 'Is hireable?',
                                             'site_admin': 'Is site admin?',
                                             'created_at': 'Joined at',
                                             'updated_at': 'Updated at'}
                                             
    # User attributes                                    
    user_attrs = ['avatar_url','id','node_id','gravatar_id','site_admin','type','html_url']
    # User attribute dictionary
    user_attr_dict = {'avatar_url': 'Profile Photo',
                                             'id': 'ID#',
                                             'node_id': 'Node ID',
                                             'gravatar_id': 'Gravatar ID',
                                             'site_admin': 'Is site admin?',
                                             'type': 'Account type',
                                             'html_url': 'URL'}
                                         
    # Topic atrributes                                 
    topic_attrs = ['score','curated','featured','display_name','created_by','created_at','updated_at']
    # Topic attribute dictionary
    topic_attr_dict = {'score': 'Score',
                                               'curated': 'Curated',
                                               'featured': 'Featured',
                                               'display_name': 'Display Name',
                                               'created_by': 'Created by',
                                               'created_at': 'Created at',
                                               'updated_at': 'Updated at'}
        
    # Gists attributes                                       
    gists_attrs = ['node_id','description','comments','files','git_push_url','public','truncated','updated_at']
    # Gists attribute dictionary
    gists_attr_dict = {'node_id': 'Node ID',
                                              'description': 'About',
                                              'comments': 'Comments',
                                              'files': 'Files',
                                              'git_push_url': 'Git Push URL',
                                              'public': 'Is public?',
                                              'truncated': 'Is truncated?',
                                              'updated_at': 'Updated at'}
                                              
    # Issue attributes                                      
    issue_attrs = ['id','node_id','score','state','number','comments','milestone','assignee','assignees','labels','locked','draft','closed_at','body']
    # Issue attribute dict
    issue_attr_dict = {'id': 'ID#',
                                               'node_id': 'Node ID',
                                               'score': 'Score',
                                               'state': 'State',
                                               'closed_at': 'Closed at',
                                               'number': 'Number',
                                               'comments': 'Comments',
                                               'milestone': 'Milestone',
                                               'assignee': 'Assignee',
                                               'assignees': 'Assignees',
                                               'labels': 'Labels',
                                               'draft': 'Is draft?',
                                               'locked': 'Is locked?',
                                               'created_at': 'Created at',
                                               'body': 'Body'}
                                               
    # Author dictionary
    author_dict = {'Alias': 'rly0nheart',
                                         'Country': 'Zambia, Africa',
                                         'About.me': 'https://about.me/rly0nheart'}
                                         
                                         
                                         
    logging.info(f'Started new session on {platform.node()}:{os.getlogin()}')
    while True:
        if platform.system() == 'Windows':
            subprocess.run(['cls'])
        else:
            subprocess.run(['clear'],shell=False)
            
        print(banner.banner)
        command = input(f'''{colors.white}┌──({colors.red}{os.getlogin()}{colors.white}@{colors.red}octosuite{colors.white})-[{colors.green}{os.getcwd()}{colors.white}]\n└╼[{colors.green}:~{colors.white}]{colors.reset} ''')
        if command == 'orginfo':
            org_info(org_attrs, org_attr_dict)
        elif command == 'userinfo':
            user_profile(profile_attrs, profile_attr_dict)
        elif command == 'repoinfo':
            repo_info(repo_attrs, repo_attr_dict)
        elif command == 'pathcontents':
            path_contents(path_attrs, path_attr_dict)
        elif command == 'orgrepos':
            org_repos(org_attrs, org_attr_dict)
        elif command == 'userrepos':
            user_repos(repo_attrs, repo_attr_dict)
        elif command == 'usergists':
            user_gists(gists_attrs, gists_attr_dict)
        elif command == 'userfollowers':
            followers(user_attrs, user_attr_dict)
        elif command == 'userfollowing':
            following()
        elif command == 'usersearch':
            user_search(user_attrs, user_attr_dict)
        elif command == 'reposearch':
            repo_search(repo_attrs, repo_attr_dict)
        elif command == 'topicsearch':
            topic_search(topic_attrs, topic_attr_dict)
        elif command == 'issuesearch':
            issue_search(issue_attrs, issue_attr_dict)
        elif command == 'commitsearch':
            commits_search()
        elif command == 'changelog':
            print(changelog())
        elif command == 'author':
            author(author_dict)
        elif command == 'ilinso':
        	easter_egg()
        elif command == 'help':
            print(help())
        elif command == 'exit':
            logging.info('Session terminated with \'exit\' command')
            exit(f'\n{colors.white}[{colors.red}-{colors.white}] Session terminated with \'exit\' command{colors.reset}')
        else:
            print(f'\n{colors.white}[{colors.red}!{colors.white}] Command not found: ‘{command}’{colors.reset}')
            logging.warning(f'command not found: ‘{command}’')
                   
        input(f'\n{colors.white}[{colors.green}?{colors.white}] Press any key to continue{colors.reset} ')
            
            
def org_info(org_attrs, org_attr_dict):
    organization = input(f'{colors.white}@{colors.green}Organization {colors.white}>>{colors.reset} ')
    api = f'https://api.github.com/orgs/{organization}'
    response = requests.get(api)
    if response.status_code != 200:
    	print(f'\n{colors.white}[{colors.red}-{colors.white}] Organization @{organization} {colors.red}Not Found{colors.reset}')
    else:
    	response = response.json()
    	print(f"\n{colors.white}{response['name']}{colors.reset}")
    	for attr in org_attrs:
    		print(f'{colors.white}├─ {org_attr_dict[attr]}: {colors.green}{response[attr]}{colors.reset}')
    
                        
# Fetching user information        
def user_profile(profile_attrs, profile_attr_dict):
    username = input(f'{colors.white}@{colors.green}Username{colors.white} >> {colors.reset}')
    api = f'https://api.github.com/users/{username}'
    response = requests.get(api)
    if response.status_code != 200:
    	print(f'\n{colors.white}[{colors.red}-{colors.white}] User @{username} {colors.red}Not Found{colors.reset}')
    else:
    	response = response.json()
    	print(f"\n{colors.white}{response['name']}{colors.reset}")
    	for attr in profile_attrs:
    		print(f'{colors.white}├─ {profile_attr_dict[attr]}: {colors.green}{response[attr]}{colors.reset}')

        	        	
# Fetching repository information   	
def repo_info(repo_attrs, repo_attr_dict):
    username = input(f'{colors.white}@{colors.green}Owner-username{colors.white} >> {colors.reset}')
    repo_name = input(f'{colors.white}%{colors.green}reponame{colors.white} >> {colors.reset}')
    api = f'https://api.github.com/repos/{username}/{repo_name}'
    response = requests.get(api)
    if response.status_code != 200:
    	print(f'\n{colors.white}[{colors.red}-{colors.white}] Repository %{repo_name} {colors.red}Not Found{colors.reset}')
    else:
    	response = response.json()
    	print(f"\n{colors.white}{response['full_name']}{colors.reset}")
    	for attr in repo_attrs:
    	    print(f"{colors.white}├─ {repo_attr_dict[attr]}: {colors.green}{response[attr]}{colors.reset}")
        
    
# Get path contents        
def path_contents(path_attrs, path_attr_dict):
    username = input(f'{colors.white}@{colors.green}Owner-username{colors.white} >> {colors.reset}')
    repo_name = input(f'{colors.white}%{colors.green}reponame{colors.white} >> {colors.reset}')
    path_name = input(f'{colors.white}/path/name >>{colors.reset} ')
    api = f'https://api.github.com/repos/{username}/{repo_name}/contents/{path_name}'
    response = requests.get(api)
    if response.status_code != 200:
        print(f'\n{colors.white}[{colors.red}-{colors.white}] Information {colors.red}Not Found{colors.reset}')
    else:
    	response = response.json()
    	for item in response:
    	    print(f"\n{colors.white}{item['name']}{colors.reset}")
    	    for attr in path_attrs:
    	    	print(f'{colors.white}├─ {path_attr_dict[attr]}: {colors.green}{item[attr]}{colors.reset}')
        	
   
# Fetching organozation repositories        
def org_repos(repo_attrs, repo_attr_dict):
    organization = input(f'{colors.white}@{colors.green}Organization{colors.white} >> {colors.reset}')
    api = f'https://api.github.com/orgs/{organization}/repos?per_page=100'
    response = requests.get(api)
    if response.status_code != 200:
        print(f'\n{colors.white}[{colors.red}-{colors.white}] Organization @{organization} {colors.red}Not Found{colors.reset}')
    else:
        response = response.json()
        for repo in response:
        	print(f"\n{colors.white}{repo['full_name']}{colors.reset}")
        	for attr in repo_attrs:
        		print(f"{colors.white}├─ {repo_attr_dict[attr]}: {colors.green}{repo[attr]}{colors.reset}")
        	print('\n')
     
   
# Fetching user repositories        
def user_repos(repo_attrs, repo_attr_dict):
    username = input(f'{colors.white}@{colors.green}Username{colors.white} >> {colors.reset}')
    api = f'https://api.github.com/users/{username}/repos?per_page=100'
    response = requests.get(api)
    if response.status_code != 200:
    	print(f'\n{colors.white}[{colors.red}-{colors.white}] User @{username} {colors.red}Not Found{colors.reset}')
    else:
    	response = response.json()
    	for repo in response:
    		print(f"\n{colors.white}{repo['full_name']}{colors.reset}")
    		for attr in repo_attrs:
    			print(f"{colors.white}├─ {repo_attr_dict[attr]}: {colors.green}{repo[attr]}{colors.reset}")
    		print('\n')        	    
    	
    	   	       	    
# Fetching user's gists
def user_gists(gists_attrs, gists_attr_dict):
    username = input(f'{colors.white}@{colors.green}Username{colors.white} >> {colors.reset}')
    api = f'https://api.github.com/users/{username}/gists'
    response = requests.get(api).json()
    if response == []:
    	print(f'{colors.white}[{colors.red}-{colors.white}]User @{username} does not have any active gists.{colors.reset}')
    else:
        for item in response:
        	print(f"\n{colors.white}{item['id']}{colors.reset}")
        	for attr in gists_attrs:
        		print(f"{colors.white}├─ {gists_attr_dict[attr]}: {colors.green}{item[attr]}{colors.reset}")
        	print('\n')    	
    
    	    	    
# Fetching user's followera'    	    
def followers(user_attrs, user_attr_dict):
    username = input(f'{colors.white}@{colors.green}Username{colors.white} >> {colors.reset}')
    api = f'https://api.github.com/users/{username}/followers?per_page=100'
    response = requests.get(api).json()
    if response == []:
    	print(f'\n{colors.white}[{colors.red}-{colors.white}]User @{username} does not have followers.{colors.reset}')
    else:
        for item in response:
        	print(f"\n{colors.white}@{item['login']}{colors.reset}")
        	for attr in user_attrs:
        		print(f"{colors.white}├─ {user_attr_dict[attr]}: {colors.green}{item[attr]}{colors.reset}")
        	print('\n')
    
                    
# Checking whether or not user[A] follows user[B]            
def following():
    user_a = input(f'{colors.white}@{colors.green}User[A]{colors.white} >> {colors.reset}')
    user_b = input(f'{colors.white}@{colors.green}User[B]{colors.white} >> {colors.reset}')
    api = f'https://api.github.com/users/{user_a}/following/{user_b}'
    response = requests.get(api)
    if response.status_code == 204:
    	print(f'{colors.white}[{colors.green}+{colors.white}] @{user_a} follows @{user_b}.{colors.reset}')
    else:
    	print(f'{colors.white}[{colors.red}-{colors.white}] @{user_a} does not follow @{user_b}.{colors.reset}')             

    	           	    
# User search    	    
def user_search(user_attrs, user_attr_dict):
    query = input(f'{colors.white}#{colors.green}Query{colors.white} >> {colors.reset}')
    api = f'https://api.github.com/search/users?q={query}&per_page=100'
    response = requests.get(api).json()
    for item in response['items']:
    	print(f"\n{colors.white}@{item['login']}{colors.reset}")
    	for attr in user_attrs:
    		print(f"{colors.white}├─ {user_attr_dict[attr]}: {colors.green}{item[attr]}{colors.reset}")
    	print('\n')
		
       		
# Repository search
def repo_search(repo_attrs, repo_attr_dict):
    query = input(f'{colors.white}#{colors.green}Query{colors.white} >> {colors.reset}')
    api = f'https://api.github.com/search/repositories?q={query}&per_page=100'
    response = requests.get(api).json()
    for item in response['items']:
        print(f"\n{colors.white}{item['full_name']}{colors.reset}")
        for attr in repo_attrs:
            print(f"{colors.white}├─ {repo_attr_dict[attr]}: {colors.green}{item[attr]}{colors.reset}")
        print('\n')
    
    
# Topics search
def topic_search(topic_attrs, topic_attr_dict):
    query = input(f'{colors.white}#{colors.green}Query{colors.white} >> {colors.reset}')
    api = f'https://api.github.com/search/topics?q={query}&per_page=100'
    response = requests.get(api).json()
    for item in response['items']:
        print(f"\n{colors.white}{item['name']}{colors.reset}")
        for attr in topic_attrs:
            print(f"{colors.white}├─ {topic_attr_dict[attr]}: {colors.green}{item[attr]}{colors.reset}")
        print('\n')
    
    
# Issue search
def issue_search(issue_attrs, issue_attr_dict):
    query = input(f'{colors.white}#{colors.green}Query{colors.white} >> {colors.reset}')
    api = f'https://api.github.com/search/issues?q={query}&per_page=100'
    response = requests.get(api).json()
    for item in response['items']:
        print(f"\n{colors.white}{item['title']}{colors.reset}")
        for attr in issue_attrs:
            print(f"{colors.white}├─ {issue_attr_dict[attr]}: {colors.green}{item[attr]}{colors.reset}")
        print('\n')

    
# Commits search
def commits_search():
    query = input(f'{colors.white}#{colors.green}Query{colors.white} >> {colors.reset}')
    api = f'https://api.github.com/search/commits?q={query}&per_page=100'
    response = requests.get(api).json()
    n=0
    for item in response['items']:
    	n+=1
    	print(f'{colors.white}{n}.{colors.reset}')
    	pprint(item['commit'])
    	print('\n')
    	
    	
def easter_egg():
    print(f'\n{colors.white}[{colors.green}*{colors.white}] Downloading. Please wait...{colors.reset}')
    file = requests.get('https://drive.google.com/uc?export=download&id=1IRu4kWSuNpYWH8hZkqQ8mLnv4sSDu-GN')
    with open('EasterEgg.zip','wb') as f:
        f.write(file.content)
        		        
    exit(f'{colors.white}[{colors.green}+{colors.white}] Downloaded (EasterEgg.zip).\n{colors.white}[{colors.green}!{colors.white}] The password is: {colors.green}horus{colors.white}\n[{colors.green}!{colors.white}] Happy hunting! :).{colors.reset}')
    	    	
    	
# Show changelog
def changelog():
    # lol yes the changelog is hard coded
    changelog_text = '''
    v1.5.1-beta CHANGELOG:
    
• First pypi package release
• Termux users will now have to manually create the .logs folder
• Changed logs date/time format
• Removed 1 internal dependency
• There's an easter egg somewhere in here ;) (use the command 'ilinso')
'''
    return changelog_text
    	
    	
# Author info   
def author(author_dict):
    print(f'\n{colors.white}Richard Mwewa (Ritchie){colors.reset}')
    for key,value in author_dict.items():
    	print(f'{colors.white}├─ {key}: {colors.green}{value}{colors.reset}')
    	
    	
def help():
	help = f'''
	
help:

   {colors.white}Command                  Descritption
   ------------             ---------------------------------------------------------
   {colors.green}orginfo{colors.white}           -->    Get target organization info{colors.reset}
   {colors.green}userinfo{colors.white}          -->    Get target user profile info{colors.reset}
   {colors.green}repoinfo{colors.white}          -->    Get target repository info{colors.reset}
   {colors.green}pathcontents{colors.white}      -->    Get contents of a specified path from a target repository{colors.reset}
   {colors.green}orgrepos{colors.white}          -->    Get a list of repositories owned by a target organization{colors.reset}
   {colors.green}userrepos{colors.white}         -->    Get a list of repositories owned by a target user{colors.reset}
   {colors.green}usergists{colors.white}         -->    Get a list of gists owned by a target user{colors.reset}
   {colors.green}userfollowers{colors.white}     -->    Get a list of the target's followers{colors.reset}
   {colors.green}userfollowing{colors.white}     -->    Check whether or not User[A] follows User[B]{colors.reset}
   {colors.green}usersearch{colors.white}        -->    Search user(s){colors.reset}
   {colors.green}reposearch{colors.white}        -->    Search repositor[y][ies]{colors.reset}
   {colors.green}topicsearch{colors.white}       -->    Search topic(s){colors.reset}
   {colors.green}issuesearch{colors.white}       -->    Search issue(s){colors.reset}
   {colors.green}commitsearch{colors.white}      -->    Search commit(s){colors.reset}
   {colors.green}changelog{colors.white}         -->    Show changelog{colors.reset}
   {colors.green}author{colors.white}            -->    Show author info{colors.reset}
   {colors.green}help{colors.white}              -->    Show usage/help{colors.reset}
   {colors.green}exit{colors.white}              -->    Exit session{colors.reset}
   {colors.white}------------             ---------------------------------------------------------{colors.reset}
   {colors.white}Run '{colors.green}pip install --upgrade octosuite{colors.white}' to update.{colors.reset}
   '''
	return help


if os.path.exists('.logs'):
	pass
	
else:
	# Creating the .logs directory
	if platform.system() == "Windows":
		subprocess.run(['mkdir','.logs'])
	else:
		subprocess.run(['sudo','mkdir','.logs'],shell=False)
		
# Set to automatically monitor and log network and user activity into the .logs folder
logging.basicConfig(filename=f'.logs/{datetime.now()}.log',format='%(asctime)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',level=logging.DEBUG)