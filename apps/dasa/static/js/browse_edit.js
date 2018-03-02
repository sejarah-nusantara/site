// http://www.punteney.com/writes/django-inpage-edit-object-link/
function django_admin_links_div() {
    // Update these variables for your site
    var admin_url = '/admin/';
    var div_title = 'Admin';
    var div_style = 'position: fixed; top: 0; right: 0; border: solid #008999 1px; padding: 3px 5px 3px 5px; text-align: center; color: #000; background: #EEDEBC; font-size: 11px;';
    // end variables to update
    if(typeof ActiveXObject != 'undefined') {
       var x = new ActiveXObject('Microsoft.XMLHTTP');
    }
    else if(typeof XMLHttpRequest != 'undefined') {
       var x = new XMLHttpRequest();
    }
    else {
       return;
    }
    x.open('GET', location.href, false);
    x.send(null);
    try {
       var type = x.getResponseHeader('x-object-type');
       var id = x.getResponseHeader('x-object-id');
    }
    catch(e) {
       return;
    }
    var div = document.createElement('div');
    div.style.cssText = div_style;
    div.innerHTML = '<b><a href="'+admin_url+'">'+div_title+'</a></b><br /><a href="'+admin_url + type.split('.').join('/') + '/' + id + '/">Edit this page'+'</a> &nbsp; <a href="'+admin_url+'logout/">Log Out</a>';
    document.body.appendChild(div);
}
django_admin_links_div();