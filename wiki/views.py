from flask import render_template, redirect, request

from wiki import app, models
from wiki.models import ValidationError, get_page


@app.route('/')
def home():
    return redirect('/HomePage')


@app.route('/<pagetitle>/edit', methods=['GET', 'POST'])
def wikipageedit(pagetitle):
    data = {
            "pagetitle": pagetitle
            }

    if(request.method == 'POST'):
        data['content'] = request.form['content']

    else:
        page = get_page(pagetitle)
        if(page != []):
            data["page"] = page

    return render_template('wikipage.edit.html', data=data)


@app.route('/<pagetitle>/save', methods=['POST'])
def wikipagesave(pagetitle):
    if(request.method == 'POST'):
        try:
            page = get_page(pagetitle)
            if(page is not None):
                page.content = request.form['content']
            else:
                page = models.WikiPage(request.form['content'])
            page.save()
            return redirect('/' + page.title)
        except ValidationError as e:
            # Here set field Error and make a POST request to /edit
            return "ValidationError: " + e.message, 500


@app.route('/<pagetitle>')
def wikipageredirect(pagetitle):
    return redirect('/%s/' % pagetitle)


@app.route('/<pagetitle>/')
def wikipageview(pagetitle):
    page = get_page(pagetitle)
    data = {
            "pagetitle": pagetitle
            }
    if(page != None):
        data["page"] = page

    return render_template('wikipage.view.html', data=data)
