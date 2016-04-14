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

$(document).on('click', '.request_friendship', function(){
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
})

$(document).on('click', '.cancel_request', function(){
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
})

$(document).on('click','.accept_request', function() {
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

$(document).on('click','.deny_request', function() {
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

$(document).on('click','.unfriend_members', function() {
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

$(document).on('click','.unfriend', function() {
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

function reloadLists(data, textStatus, jqHXR)
{
	$("#content").html(data);
}

