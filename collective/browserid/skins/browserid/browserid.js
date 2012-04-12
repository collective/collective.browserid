(function($){
	"use strict";
	
	function gotAssertion(assertion) {
	    if (assertion !== null) {
	        $(".browserid-login input[name=__ac_browserid_assertion]").val(assertion);
	        $(".browserid-login form").submit();
	    }
	}
	
	$(function() {
		// onload
		$('.browserid-login button').click(function() {
			navigator.id.get(gotAssertion);
			return false;
		});
	});
	
	// prevent FOUC
	$('head').append($('<style type="text/css">.browserid-login{display: block;}</style>'));
}(jQuery));