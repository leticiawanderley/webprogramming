$(function(){

	$('#user').blur(function(){
		$.ajax({
			type: 'POST',
			url: '/social/checkusersignup/',
			data : {
				'user' : $('#user').val(),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: checkuseranswer,
			dataType: 'html'
		});
	});

});

function checkuseranswer(data, textStatus, jqHXR)
{
	$('#info').html(data);
}

$("a").removeAttr('href');

$(function(){
	$('.request_friendship').click(function(event){
		$.ajax({
			type: 'POST',
			url: '/social/members/',
			data : {
				'add' : $(this).attr('id'),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: reloadLists,
			dataType: 'html'
		});
	});
});

$(function(){
	$('.accept_request').click(function(event){
		$.ajax({
			type: 'POST',
			url: '/social/members/',
			data : {
				'accept' : $(this).attr('id'),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: reloadLists,
			dataType: 'html'
		});
	});
});

$(function(){
	$('.deny_request').click(function(event){
		$.ajax({
			type: 'POST',
			url: '/social/members/',
			data : {
				'deny' : $(this).attr('id'),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: reloadLists,
			dataType: 'html'
		});
	});
});

$(function(){
	$('.cancel_request').click(function(event){
		$.ajax({
			type: 'POST',
			url: '/social/members/',
			data : {
				'cancel' : $(this).attr('id'),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: reloadLists,
			dataType: 'html'
		});
	});
});

$(function(){
	$('.unfriend_members').click(function(event){
		$.ajax({
			type: 'POST',
			url: '/social/members/',
			data : {
				'remove' : $(this).attr('id'),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: reloadLists,
			dataType: 'html'
		});
	});
});

$(function(){
	$('.unfriend').click(function(event){
		$.ajax({
			type: 'POST',
			url: '/social/friends/',
			data : {
				'remove' : $(this).attr('id'),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: reloadLists,
			dataType: 'html'
		});
	});
});

function reloadLists(data, textStatus, jqHXR)
{
	$("#content").html(data);
}
