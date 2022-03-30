from pybtex.style.formatting.unsrt import Style
from formatting.apa import APAStyle
from labels.apa import LabelStyle as APALabelStyle
from pybtex.plugin import register_plugin
from pybtex.style.template import names, sentence

class MyAPALabelStyle(APALabelStyle):
    def format_label(self, entry):
        return APALabelStyle.format_label(self, entry)

class MyAPAStyle(Style):
    default_label_style = 'myapa'

def setup(app):
    register_plugin('pybtex.style.labels', 'myapa', MyAPALabelStyle)
    register_plugin('pybtex.style.formatting', 'myapastyle', MyAPAStyle)