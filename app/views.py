"""Summary

Attributes:
    script_args (dict): Description
"""
import os
from app import app
from flask import render_template, request, jsonify, url_for, flash, redirect, send_from_directory
import json
import jinja2
import pdfkit
import pyqrcode

# DEBUG
import time


script_args = {}


@app.route('/', methods=['GET', 'POST'])
def page_index():
    """Summary.

    Returns:
        TYPE: Description
    """
    page_args = script_args.copy()

    # AJAX Action Occurs.
    if request.method == 'POST' and 'action' in request.get_json():
        return process_ajax_action(request, page_args=page_args)
    return render_template('./index.html', **page_args)


@app.route('/rendered/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = app.config['APP_DIR']
    return send_from_directory(directory='', filename=filename)


@app.route('/download/<path:path>')
def send_js(path):
    return send_from_directory(app.config['STATIC_DIR'], path)


def process_ajax_action(request, **kwargs):
    """AJAX Action Occurs. Process the specific action & return JSON response.

    Args:
        request (TYPE): Description
        **kwargs (TYPE): Description
    """
    print(request.get_json()['action'])

    if 'page_args' in kwargs:
        # Values common to the specific page.
        page_args = kwargs['page_args']

    # Actions
    # ==========================================================================
    if request.get_json()['action'] == "init":
        '''init.
        '''
        contents_html = render_html_from_action('init', {})
        return json.dumps({'status': 'OK', "init": contents_html})

    if request.get_json()['action'] == "render":
        '''render.
        '''
        contents_html = render_html_from_action('render', {})   #   UI -> render.jinja

        # Jinja Env for render layouts of barcodes
        render_layouts_templates = os.path.join(app.config['TEMPLATES_DIR'], 'render_layouts')
        template_dirs = [x[0] for x in os.walk(render_layouts_templates)]
        jinja_env = create_jinja2_env(template_dirs=template_dirs)

        # Create rendered qrcodes
        qrcodes = []

        for i in range(30):
            t = time.time()

            qrcode = {}
            qr_time = pyqrcode.create(t)
            qr_code_name = str(t) + '.svg' 
            qr_time.svg(qr_code_name, scale=4)
            print(qr_time.terminal(quiet_zone=1))

            qrcode['name'] = qr_code_name
            qrcode['id'] = t
            qrcode['label'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
            qrcodes.append(qrcode) # throw this sucker into a template
        rendered_html = os.path.join(os.getcwd(),
                                             "tmp.html")
        with open(rendered_html, "w+") as f:
            f.write(
                jinja_env.get_template("layout1.jinja").render(
                    {"qrcodes":qrcodes}))


        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
        }
        pdfkit.from_file(rendered_html, 'qrcodes.storage.from-file.pdf', options=options)
        # pdfkit.from_url('http://192.168.1.148:5000/', 'qrcodes.storage.pdf')
        
        rendered = jinja_env.get_template("layout1.jinja").render({"qrcodes":qrcodes})

        return json.dumps({'status': 'OK', "render": contents_html, "rendered-html": rendered})

    # No action found
    return json.dumps({'status': 'OK',
                       'message':
                       'No action for ' + request.get_json()['action']})


def render_html_from_action(action, data):
    """Render HTML For an Action.

    Args:
        action (String): name of the action (for the template file name).
        data (List): Data passed to the template.

    Returns:
        String: Rendered HTML.
    """
    action_templates = os.path.join(app.config['TEMPLATES_DIR'], 'actions')
    template_dirs = [x[0] for x in os.walk(action_templates)]
    jinja_env = create_jinja2_env(template_dirs=template_dirs)
    # app.logger.info(data)
    return jinja_env.get_template("%s.jinja" % action).render(data=data)


def create_jinja2_env(**kwargs):
    """A jinja2 Environment with templates loaded.

    Args:
        **kwargs (TYPE): Description
    """
    print("JINJA2 ENV CREATED")
    if "template_dirs" in kwargs:
        print("TEMPLATE DIRS: " + str(kwargs["template_dirs"]))
        template_loader = jinja2.FileSystemLoader(kwargs["template_dirs"])
    template_env = jinja2.Environment(loader=template_loader)
    return template_env
