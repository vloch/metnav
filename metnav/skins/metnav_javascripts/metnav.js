$(document).ready(function(){
    $('p.goToTop').click(function(event){
        event.preventDefault();
        $('html,body').animate({scrollTop:$('[name="haut"]').offset().top}, 550);
    });
	
	$("ul.submenu a").hover(function() {
                $(this).parents("li").addClass("highlight");
        }, function() {
                $(this).parents("li").removeClass("highlight");
        });
	
});