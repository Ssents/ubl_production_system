


// If production type is Work order, enable editing the woek order number
var production_type = document.getElementById('productionTypeValidation');
var order = production_type.options[production_type.selectedIndex].value;

if (order != "WO"){
	document.getElementById('orderNumberValidation').disabled = true;
};

// on change actually
production_type.onchange = function(){
	var order = production_type.options[production_type.selectedIndex].value;
	console.log(order);
	if (order == "WO"){
		document.getElementById('orderNumberValidation').disabled = false;
	}
	else {
		document.getElementById('orderNumberValidation').disabled = true;
	}

};



	
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
var csrftoken = getCookie('csrftoken');
var activeItem = null;

// http://127.0.0.1:8000/api/v1/orders

// ADDING ORDER DETAILS
function add_order(){
	var wrapper = document.getElementById('production-details-section')
}
