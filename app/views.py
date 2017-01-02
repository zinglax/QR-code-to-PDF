import os
from app import app
from flask import render_template, request, jsonify, url_for, flash, redirect
import json
import jinja2


script_args = {}


@app.route('/', methods=['GET', 'POST'])
def page_index():
    page_args = script_args.copy()

    # AJAX Action Occurs.
    if request.method == 'POST' and 'action' in request.get_json():
        return process_ajax_action(request, page_args=page_args)
    return render_template('./index.html', **page_args)


def process_ajax_action(request, **kwargs):
    """AJAX Action Occurs. Process the specific action & return JSON response.
    """

    print(request.get_json()['action'])

    if 'page_args' in kwargs:
        # Values common to the specific page.
        page_args = kwargs['page_args']


    # Actions
    # ==========================================================================
    if request.get_json()['action'] == "init":
        '''init
        '''        

        contents_html = render_html_from_action('init', {})
        return json.dumps({'status': 'OK', "init": contents_html})


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
    """A jinja2 Environment with templates loaded."""
    print("JINJA2 ENV CREATED")
    if "template_dirs" in kwargs:
        print("TEMPLATE DIRS: " + str(kwargs["template_dirs"]))
        template_loader = jinja2.FileSystemLoader(kwargs["template_dirs"])
    template_env = jinja2.Environment(loader=template_loader)
    return template_env
