// グローバル変数定義
// html文書がロードされた瞬間に実行される


// オンロードイベント
// <body>に指定された各エレメントが表示され準備が整ったら実行される
// jQueryの書き方
$(function (){
	var today = new Date();
	var year = today.getFullYear();
	var month = today.getMonth() + 1;
	$("."+year+"."+month).css("display","block");
})

function beforeMonth(year, month) {
	$("."+year+"."+month).css("display","none");
	if (month == 1) {
		$("."+(year-1)+".12").css("display","block");
	}
	$("."+year+"."+(month-1)).css("display","block");
}

function afterMonth(year, month) {
	$("."+year+"."+month).css("display","none");
	if (month == 12) {
		$("."+(year+1)+".1").css("display","block");
	}
	$("."+year+"."+(month+1)).css("display","block");
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$('#ajax-add-post').on('submit', e => {
	console.log("submitevenv");
    // デフォルトのイベントをキャンセルし、ページ遷移しないように!
    e.preventDefault();

	var task_id = 0;

    $.ajax({
        'url': 'https://healthreceiptapp.herokuapp.com/api/worker_add/',
        'type': 'POST',
        'data': {
            "input_a": $("#input_a").val(),
			"input_b": $("#input_b").val()
        },
        'dataType': 'json'
    }).done( response => {
        task_id = response.task_id;
    });

	var spanedSec = 0;

	setInterval(function () {
        spanedSec++;
		console.log(spanedSec + "秒");

        if (spanedSec >= 30) {
			$.ajax({
		        'url': 'https://healthreceiptapp.herokuapp.com/api/worker_result/',
		        'type': 'POST',
		        'data': {
		            'task_id': task_id,  // 記事タイトル
		        },
		        'dataType': 'json'
		    }).done( response => {
		        $("#result-text").text() = response.result;
		    });
        }
    }, 1000);

});
