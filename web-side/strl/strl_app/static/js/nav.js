function resetPages(){
	$('#home_page').removeClass('active')
	$('#editor_page').removeClass('active')
	$('#sign_in_page').removeClass('active')
	$('#sign_up_page').removeClass('active')
	$('#worlds_page').removeClass('active')
}

function activePage(name){
	resetPages()
	$('#'+name).addClass('active')
}