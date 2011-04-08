function popup(mylink, windowname) {
    if (! window.focus)return true;
    var href;
    if (typeof(mylink) == 'string')
	href=mylink;
    else
	href=mylink.href;
    window.open(href, windowname, 'width=400,height=200,scrollbars=no,status=no,location=no');
    return false;
}

$(document).ready(function() {
	$(".module").delegate("#id_org", "change", function() {
		//var row = $(this).attr("id").split('id_org')[1].split("-user")[0];
		var org_id = $(this).val();
		var data = {"org_id":org_id};
		
		$.getJSON("http://localhost:8080/app/admin/json/org/", data, function(data) {
			$("#id_groupadmin_set-" + 0 + "-user").find('option').remove().end();
			var NONE_SELECT = "---------";
			//$("#id_groupadmin_set-" + 0 + "-user").append("<option></option>").attr("value", "").text(NONE_SELECT);
			//if (data.length > 0) {
			$.each(data, function (index, value) {
				alert(index);
				key = data[index].pk;
				name = data[index].fields['name_text'];
				$("#id_groupadmin_set-0-user").
				    append("<option></option>").attr("value", key).text(name);
			    });
			//}
		    });
	    });
    });