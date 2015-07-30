from __future__ import unicode_literals

from djblets.extensions.hooks import TemplateHook, URLHook

from reviewboard.extensions.base import Extension
from reviewboard.urls import review_request_url_names, diffviewer_url_names

from cc_counter.urls import urlpatterns

import logging

class CCCounter(Extension):
	"""Links up CC Counter extension into CCCounter's framework
	"""
	metadata = {
		'Name': 'CCCounter'
	}

	css_bundles = {
		'default': {
			'source_filenames': [
				'css/cccounter.css',
				'css/jquery.dataTables.css',
			]
		},
	}

	js_bundles = {
		'default': {
			'source_filenames': [
				'js/jquery.dataTables.js',
			]
		},
	}

	has_admin_site = False
	def __init__(self, *args, **kwargs):
		logging.warning("I'm really init")
		super(CCCounter, self).__init__(*args, **kwargs)
		URLHook(self, urlpatterns)
		TemplateHook(self, "base-after-content", "cc_counter/reviewrequest_cc.html",
				apply_to=diffviewer_url_names)