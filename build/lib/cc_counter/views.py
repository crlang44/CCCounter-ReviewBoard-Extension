from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader
from django.db import models

import logging
import codecs

from reviewboard.reviews.views import _find_review_request, _query_for_diff, get_patched_file, raw_diff
from reviewboard.diffviewer.diffutils import convert_to_unicode, get_original_file

from cc_counter.ccreader import analyze_file, get_comparison_data
from cc_counter.cccomparer import track_diff_ccchanges

import os
import operator

HOMEFOLDER = os.getenv('HOME')


def cc_list(request, template_name = 'cc_counter/datagrid.html'):
    return CCGrid(request).render_to_response(template_name)

def _download_analysis(analyze_function, request, review_request_id, revision,
                        filediff_id, local_site=None, modified=True):
    """Generates file analysis given by analyze_function on the specified file.

    This will download the file as a string, write it to a temporary file 
    in the homefolder, run the analysis, delete the temporary file, and 
    output the filename and data_analysis
    """
    
    logging.debug("Analyze_function" + analyze_function.__name__)

    review_request, response = \
        _find_review_request(request, review_request_id, local_site)

    if not review_request:
        return response

    draft = review_request.get_draft(request.user)
    diffset = _query_for_diff(review_request, request.user, revision, draft)
    filediff = get_object_or_404(diffset.files, pk=filediff_id)
    encoding_list = diffset.repository.get_encoding_list()

    # Get a file either from the cache or the SCM, applying the parent diff if it exists.
    # SCM exceptions are passed back to the caller.
    working_file = get_original_file(filediff, request, encoding_list)

    if modified:
        working_file = get_patched_file(working_file, filediff, request)

    working_file = convert_to_unicode(working_file, encoding_list)[1]   
    logging.debug("Encoding List: %s", encoding_list)
    logging.debug("Source File: " + filediff.source_file)
    
    temp_file_name = "cctempfile_" + filediff.source_file.replace("/","_")
    logging.debug("temp_file_name: " + temp_file_name)
    source_file = os.path.join(HOMEFOLDER, temp_file_name)
    
    #with open (source_file, "r") as myfile:
    #    logging.debug("String: " + myfile.read().replace('\n', ''))
      
    logging.debug("File contents" + working_file)
    #temp_file = open(source_file, 'w')
    #temp_file = codecs.open(source_file, encoding='utf-8')
    #temp_file.write(working_file.encode('utf-8'))
    temp_file = codecs.open(source_file, 'w', encoding='utf-8')
    temp_file.write(working_file)
    
    temp_file.close()
 
    data_analysis = analyze_function(source_file)
    os.remove(source_file)
      
    if not data_analysis:
        data_analysis = None


    return filediff.source_file, data_analysis 


def _download_comparison_data(request, review_request_id, revision,
                        filediff_id, modified=True, local_site=None):
    """Generates the Cyclometric complexity of a specified file.
    """

    return _download_analysis(get_comparison_data, request, review_request_id, 
        revision, filediff_id, local_site, modified) 

def download_ccdata(request, review_request_id, revision,
                        filediff_id):
    """Generates the Cyclometric complexity of a specified file as view.

    Calls on _download_analysis and simply packages the outputs into a view
    """

    source_file, ccdata = _download_analysis(analyze_file, request, 
        review_request_id, revision, filediff_id)

    if not ccdata:
        ccdata = "Incompatable file type" 

    template = loader.get_template('cc_counter/download_ccdata.html')
    context = RequestContext(request, {
        'ccdata' : ccdata,
        'source_file' : source_file,
    })

    return HttpResponse(template.render(context))

def _reviewrequest_recent_cc(request, review_request_id, modified=True, revision_offset=0,
                                local_site=None):

    review_request, response = \
        _find_review_request(request, review_request_id, local_site)


    logging.debug("review_request: " + str(review_request))
    
    if not review_request:
        return response

    draft = review_request.get_draft(request.user)
    diffset = _query_for_diff(review_request, request.user, None, draft)
    revision = diffset.revision

    if revision - revision_offset < 0:        
        return "No such revision"
    elif revision - revision_offset == 0:
        pass #We are simply getting revision 0: the initial code.
    else:
        revision -=  revision_offset
        diffset = _query_for_diff(review_request, request.user, revision, draft)

    filediff_ids = [ffile.pk for ffile in diffset.files.all()] 

    reviewrequest_ccdata = dict()
    for filediff_id in filediff_ids:
        filename, comparison_data = _download_comparison_data(request, review_request_id, revision, filediff_id, modified)
        logging.debug("filediff_id: " + str(filediff_id))
        logging.debug("filename: " + str(filename))
        logging.debug("comparison_data: " + str(comparison_data))
	reviewrequest_ccdata[filename] = comparison_data
        
    return reviewrequest_ccdata


def reviewrequest_recent_cc(request, review_request_id, revision_offset=1):
    """The generic view of the Cyclometric complexity counter
    """
    """"To be finished"""
    reviewrequest_ccdata = _reviewrequest_recent_cc(request, review_request_id, True)
    prev_reviewrequest_ccdata = _reviewrequest_recent_cc(request, review_request_id, False, revision_offset=1)
    logging.debug("reviewrequest_ccdata: ", str(reviewrequest_ccdata))
    logging.debug("prev_reviewrequest_ccdata: ", str(prev_reviewrequest_ccdata))
    diff_changes = track_diff_ccchanges(reviewrequest_ccdata, prev_reviewrequest_ccdata)

    compatable_files = []
    incompatable_files = []

    for diff_change in diff_changes:
        if diff_change['ccchanges'] == None:
            incompatable_files += [diff_change]
        else:
            compatable_files += [diff_change]

    processed_comp_files = []
    unchanged_cc_files = []

    functions_to_order = list()

    for compatible_file in compatable_files:
        changed_cc_functions = list()
        has_changed = False

        for function_instances in compatible_file['ccchanges']:
            for instance in function_instances:
                if instance[2] == instance[3]:
                    pass
                else:
                    functions_to_order.append((compatible_file['filename'],) + instance)
                    changed_cc_functions.append(instance)
                    has_changed = True

        processed_file =[{
            'filename': compatible_file['filename'],
            'ccchanges': changed_cc_functions
        }]
        if has_changed:
            processed_comp_files += processed_file
        else:
            unchanged_cc_files += processed_file

    logging.debug("functions_to_order unsorted: %s", functions_to_order)
    functions_to_order.sort(key=operator.itemgetter(4), reverse=True)
    logging.debug("functions_to_order sorted: %s", functions_to_order)

    template = loader.get_template('cc_counter/reviewrequest_recent_cc.html')
    context = RequestContext(request, {
        'incompatable_files': incompatable_files,
        'compatable_files': processed_comp_files,
        'unchanged_files': unchanged_cc_files,
        'ordered_functions': functions_to_order,
    })

    http_response = HttpResponse(template.render(context))

    return http_response
