import sys, inspect
from django.db import models
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render as djangorender
from tracking.models import Visitor

def find_request():
    """
    Find the request object and return it. For use when we dont have a propper
    request object to go to. Will contain all the usual stuff.
    
    """
    f = sys._getframe()
    while f:
        request = f.f_locals.get('request')
        if isinstance(request, HttpRequest):
            break
        f = f.f_back
    return request

def set_base_template(request, base):
    if base == 'touch':
        request.session['base_template'] = 'touch_base.html'
    else:
        request.session['base_template'] = 'desktop_base.html'

    try:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    except:
        return HttpResponseRedirect(request.META['PATH_INFO'])

def get_base_template(request):
    try:
        return request.session['base_template']
    except:
        request.session['base_template'] = 'desktop_base.html'
        return request.session['base_template']

def render(request, *args):
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])

    template = args[0]

    try:
        vars = args[1]
    except:
        vars = {}
        
    try:
        app_name = vars['app_name']
    except:
        app_name = mod.__name__.split('.')[1]
    
    vars['app_name'] = app_name
    vars['base_template'] = get_base_template(request)
    
    users = Visitor.objects.active()
    seen = set()
    seen_add = seen.add
    vars['active_users'] = [ x for x in users if x.user not in seen and not seen_add(x.user)]
    
    request.session['app_name'] = vars['app_name']
    
    return djangorender(request, template, vars)


def create_datepicker(form):
    formfield = form.formfield()
    if isinstance(form, models.DateField):
        formfield.widget.attrs.update({'class':'datePicker', 'readonly':'true'})
    return formfield

def validate_internal_tags(request, tags):

    tags_array = []
    
    for tag in tags:
        is_upper = tag.isupper()
        is_staff = request.user.is_staff
        
        if is_upper and is_staff:
            tags_array.append( tag.upper() )
        else:
            tags_array.append( tag.lower() )
            
    return tags_array




from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils.cache import add_never_cache_headers
from django.utils import simplejson

def get_datatables_records(request, querySet, columnIndexNameMap, jsonTemplatePath = None, *args):
        """
        Usage: 
                querySet: query set to draw data from.
                columnIndexNameMap: field names in order to be displayed.
                jsonTemplatePath: optional template file to generate custom json from.  If not provided it will generate the data directly from the model.

        """
        
        cols = int(request.GET.get('iColumns',0)) # Get the number of columns
        iDisplayLength =  min(int(request.GET.get('iDisplayLength',10)),100)     #Safety measure. If someone messes with iDisplayLength manually, we clip it to the max value of 100.
        startRecord = int(request.GET.get('iDisplayStart',0)) # Where the data starts from (page)
        endRecord = startRecord + iDisplayLength  # where the data ends (end of page)
        
        # Pass sColumns
        keys = columnIndexNameMap.keys()
        keys.sort()
        colitems = [columnIndexNameMap[key] for key in keys]
        sColumns = ",".join(map(str,colitems))
        
        # Ordering data
        iSortingCols =  int(request.GET.get('iSortingCols',0))
        asortingCols = []
                
        if iSortingCols:
                for sortedColIndex in range(0, iSortingCols):
                        sortedColID = int(request.GET.get('iSortCol_'+str(sortedColIndex),0))
                        if request.GET.get('bSortable_{0}'.format(sortedColID), 'false')  == 'true':  # make sure the column is sortable first
                                sortedColName = columnIndexNameMap[sortedColID]
                                sortingDirection = request.GET.get('sSortDir_'+str(sortedColIndex), 'asc')
                                if sortingDirection == 'desc':
                                        sortedColName = '-'+sortedColName
                                asortingCols.append(sortedColName) 
                querySet = querySet.order_by(*asortingCols)

        # Determine which columns are searchable
        searchableColumns = []
        for col in range(0,cols):
                if request.GET.get('bSearchable_{0}'.format(col), False) == 'true': searchableColumns.append(columnIndexNameMap[col])

        # Apply filtering by value sent by user
        customSearch = request.GET.get('sSearch', '').encode('utf-8');
        if customSearch != '':
                outputQ = None
                first = True
                for searchableColumn in searchableColumns:
                        kwargz = {searchableColumn+"__icontains" : customSearch}
                        outputQ = outputQ | Q(**kwargz) if outputQ else Q(**kwargz)             
                querySet = querySet.filter(outputQ)

        # Individual column search 
        outputQ = None
        for col in range(0,cols):
                if request.GET.get('sSearch_{0}'.format(col), False) > '' and request.GET.get('bSearchable_{0}'.format(col), False) == 'true':
                        kwargz = {columnIndexNameMap[col]+"__icontains" : request.GET['sSearch_{0}'.format(col)]}
                        outputQ = outputQ & Q(**kwargz) if outputQ else Q(**kwargz)
        if outputQ: querySet = querySet.filter(outputQ)
                
        iTotalRecords = iTotalDisplayRecords = querySet.count() #count how many records match the final criteria
        querySet = querySet[startRecord:endRecord] #get the slice
        sEcho = int(request.GET.get('sEcho',0)) # required echo response
        
        if jsonTemplatePath:
                jstonString = render_to_string(jsonTemplatePath, locals()) #prepare the JSON with the response, consider using : from django.template.defaultfilters import escapejs
                response = HttpResponse(jstonString, mimetype="application/javascript")
        else:
                aaData = [ entry.aaData() for entry in querySet ]
                '''
                aaData = []
                a = querySet.values() 
                for row in a:
                        rowkeys = row.keys()
                        rowvalues = row.values()
                        rowlist = []
                        for col in range(0,len(colitems)):
                                for idx, val in enumerate(rowkeys):
                                        if val == colitems[col]:
                                                rowlist.append(unicode(rowvalues[idx]))
                        aaData.append(rowlist)
                '''
                response_dict = {}
                response_dict.update({'aaData':aaData})
                response_dict.update({'sEcho': sEcho, 'iTotalRecords': iTotalRecords, 'iTotalDisplayRecords':iTotalDisplayRecords, 'sColumns':sColumns})
                response =  HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
        #prevent from caching datatables result
        add_never_cache_headers(response)
        return response