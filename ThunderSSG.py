# Gemaakt door Bers Goudantov 1ITAI
# style.css en de template files paginas en ook de tekst voor de html files werden gemaakt door middel van ChatGPT 3.5 
import os
from pathlib import Path
import yaml
import markdown
import webbrowser
from jinja2 import Environment, FileSystemLoader

TEMPLATE_FILE = "Template.html" # initiatie van de variabele TEMPLATE_FILE met als gegvens de naam van de template html bestand
TEMPLATE_DIR = os.path.join(os.path.abspath("."), "Templates") # geeft het pad van de Template directory
ABS_TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, TEMPLATE_FILE) # geeft het absolute pad van de Template.html weer
lijstVanPagesLink = [] # slaagt op alle links van elke pages bij
lijstVanPostsLink = [] # slaagt op alle tags van elke posts bij
lijstVanPagesTitels = [] # slaagt op alle titels van elke aangemaakte pages bij
lijstVanPostsTitels = [] # slaagt op alle titels van elke aangemaakte posts bij
tagList = [] # slaagt op alle tags van elke posts/pages bij
Categories = [] # slaagt op de categories van elke posts bij
paginaPadHome = os.path.abspath('homepage.html') # verwijst naar de lokale pad voor de homepage.html
paginaPadNavigatie = os.path.abspath('Navigation.html') # verwijst naar de lokale pad voor de Navigation.html
paginaPadAbout = os.path.abspath('about.html') # verwijst naar de lokale pad voor de about.html
paginaPadContact = os.path.abspath('contact.html') # verwijst naar de lokale pad voor de contact.html
paginaPadServices = os.path.abspath('services.html') # verwijst naar de lokale pad voor de services.html
paginaPadTerms = os.path.abspath('terms.html') # verwijst naar de lokale pad voor de terms.html
paginaPadStyle = os.path.abspath('Templates/style.css') # verwijst naar de lokale pad voor de style.css

"""Genereert de pages paginas aan"""   
def Genereer_blog_page():
    markdown_dir_Pages = './pages/'
    output_dir = Path('./_site/pages/')
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template(TEMPLATE_FILE)

    md = markdown.Markdown(extensions=['full_yaml_metadata'])

    for page in os.listdir(markdown_dir_Pages):
        with open(os.path.join(markdown_dir_Pages, page), 'r') as f:
            content = f.read()

        split = content.rfind("---") + 3
        yaml_front_matter = content[:split]
        markdown_content = content[split:]
        data = yaml.safe_load(yaml_front_matter.replace("---", ""))
        if isinstance(data, dict):
            
            tags = ', '.join(data.get("tags", []))
            if not isinstance(tags, str):
                tags = ', '.join(tags)

            author = data.get("author", [])
            if not isinstance(author, str):
                author = ', '.join(author)
            
            title = data.get("title", [])
            if not isinstance(title, str):
                title = ', '.join(title)
            
            date = data.get("date", [])
            if not isinstance(date, str):
                date = ', '.join(date)
            html_content = md.convert(markdown_content)

            output = template.render(data=data, content=html_content, tags=tags, category="geen", title=title, author=author, date=date, style=paginaPadStyle, linkHome=paginaPadHome, linkNavigatie=paginaPadNavigatie, linkAbout=paginaPadAbout, linkContact=paginaPadContact, linkServices=paginaPadServices, linkTermsOfService=paginaPadTerms)

            output_path = output_dir / f'{page[:-3]}.html'
            with open(output_path, 'w') as f:
                f.write(output)
            lijstVanPagesTitels.append(data.get("title"))
            lijstVanPagesLink.append(str(output_path))
            tagList.append(tags)
        else:
            print(f"Invalid YAML front matter for {page}")
 
     
"""Genereert een blog post paginas aan"""           
def Genereer_blog_post():
    markdown_dir_Posts = './posts/Technologie/'
    output_dir = Path('./_site/posts/')
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template(TEMPLATE_FILE)

    md = markdown.Markdown(extensions=['full_yaml_metadata'])

    for page in os.listdir(markdown_dir_Posts):
        with open(os.path.join(markdown_dir_Posts, page), 'r') as f:
            content = f.read()

        split = content.rfind("---") + 3
        yaml_front_matter = content[:split]
        markdown_content = content[split:]
        data = yaml.safe_load(yaml_front_matter.replace("---", ""))
        if isinstance(data, dict):
            
            tags = ', '.join(data.get("tags", []))
            if not isinstance(tags, str):
                tags = ', '.join(tags)
            
            author = data.get("author", [])
            if not isinstance(author, str):
                author = ', '.join(author)
            
            title = data.get("title", [])
            if not isinstance(title, str):
                title = ', '.join(title)
            
            date = data.get("date", [])
            if not isinstance(date, str):
                date = ', '.join(date)
            
            category = data.get("category", [])
            if not isinstance(category, str):
                category = ', '.join(category)
            html_content = md.convert(markdown_content)

            output = template.render(data=data, content=html_content, tags=tags, category=category, title=title, author=author, date=date, style=paginaPadStyle, linkHome=paginaPadHome, linkNavigatie=paginaPadNavigatie, linkAbout=paginaPadAbout, linkContact=paginaPadContact, linkServices=paginaPadServices, linkTermsOfService=paginaPadTerms)

            output_path = output_dir / f'{page[:-3]}.html'
            with open(output_path, 'w') as f:
                f.write(output)
            lijstVanPostsTitels.append(data["title"])
            lijstVanPostsLink.append(str(output_path))
            tagList.append(tags)
            Categories.append(category)
        else:
            print(f"Invalid YAML front matter for {page}")


"""Injecteert een javascript code bij het nieuwe aangemaakte navigatie pagina, hulp javascript cursus en ChatGPT"""
def Create_Script():
    js_code = '''
document.addEventListener("DOMContentLoaded", function() {
  var pages = {{pagesList}}
  var posts = {{postsList}}
  var namePages = {{pageNames}}
  var namePosts = {{postNames}}
  var TagsList = {{TagsList}}
  var CategoryList = {{CategoryList}}
  
   for (var i = 0; i < pages.length; i++) {
    pages[i] = pages[i].replace('\\\\', '/');
    var link = document.createElement("a");
    link.href = pages[i];
    link.appendChild(document.createTextNode(namePages[i]));

    var li = document.createElement("li");
    li.appendChild(link);

    var pagesUl = document.getElementById("pages");
    pagesUl.appendChild(li);
  }

  for (var i = 0; i < posts.length; i++) {
    posts[i] = posts[i].replace('\\\\', '/');
    var link = document.createElement("a");
    link.href = posts[i];
    link.appendChild(document.createTextNode(namePosts[i]));

    var li = document.createElement("li");
    li.appendChild(link);

    var postsUl = document.getElementById("posts");
    postsUl.appendChild(li);
  }
  
  for (var i = 0; i < pages.length; i++) {
                        pages[i] = pages[i].replace('\\\\', '/');
                        var link = document.createElement("a");
                        link.href = pages[i];
                        link.appendChild(document.createTextNode(TagsList[i]));

                        var li = document.createElement("li");
                        li.appendChild(link);

                        var pagesUl = document.getElementById("Tags");
                        pagesUl.appendChild(li);
                    }

                    for (var i = 0; i < posts.length; i++) {
                        posts[i] = posts[i].replace('\\\\', '/');
                        var link = document.createElement("a");
                        link.href = posts[i];
                        link.appendChild(document.createTextNode(CategoryList[i]));

                        var li = document.createElement("li");
                        li.appendChild(link);

                        var postsUl = document.getElementById("Category");
                        postsUl.appendChild(li);
                    }
  
});
    '''
    env = Environment(loader=FileSystemLoader("Templates"))
    template = env.get_template("Navigation_Template.html")
    output = template.render(include_js=js_code)

    with open('Navigation.html', 'w') as f:
        f.write(output)    


"""Voegt links en tags toe van de pagina en de post"""
def Add_links():
    env = Environment(loader=FileSystemLoader(""))
    template = env.get_template("Navigation.html")
    output = template.render(pagesList=lijstVanPagesLink, postsList=lijstVanPostsLink, pageNames = lijstVanPagesTitels, postNames =lijstVanPostsTitels, TagsList=tagList, CategoryList=Categories)

    with open('Navigation.html', 'w') as f:
        f.write(output)


"""Run de programma main"""
def main():
    lijstVanPagesTitels.clear()
    lijstVanPostsTitels.clear()
    lijstVanPagesLink.clear()
    lijstVanPostsLink.clear()
    tagList.clear()
    Categories.clear()
    input("Druk op enter om de SSG te starten: ")
    Create_Script()
    Genereer_blog_page()
    Genereer_blog_post()
    Add_links()
    webbrowser.open("file://" + paginaPadHome)

if __name__ == '__main__':
    main()