"""
Utility function to support application.
"""


def get_html_string(filepath):
    with open(filepath, 'r') as f:
        contents = f.read()

    contents = contents.replace(
        '''{% if title %}
        <title>{{ title }}</title>
    {% else %}
        <title>IPC</title>
    {% endif %}
    <!-- insert dash head -->''',
        '{%metas%}<title>{%title%}</title>{%favicon%}{%css%}'
    )
    contents = contents.replace(
        '''{% block content %}{% endblock %}
    <!-- insert dash footer -->''',
        '{%app_entry%}<footer>{%config%}{%scripts%}{%renderer%}</footer>'
    )
    return contents
