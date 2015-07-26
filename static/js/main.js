

$(window).load(function() {
	var path = $('#path').load(function)
   	switch(path)
   	{
   		case ""
		$('.sec').css('background','red');
   	}
}); 

$("#btn_submit").click(function(){
	console.log("submit");
	$("#target").submit();
})
