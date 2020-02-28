// グローバル変数定義
// html文書がロードされた瞬間に実行される

var spinner = document.getElementById('loading');

// オンロードイベント
// <body>に指定された各エレメントが表示され準備が整ったら実行される
// jQueryの書き方
$(function (){
 	spinner.classList.add('loaded');

    $('#receiptform').on('change', 'input[type="file"]', function(e) {
    var file = e.target.files[0],
        reader = new FileReader(),
        $preview = $(".preview");
        t = this;

    // 画像ファイル以外の場合は何もしない
    if(file.type.indexOf("image") < 0){
      return false;
    }

    // ファイル読み込みが完了した際のイベント登録
    reader.onload = (function(file) {
      return function(e) {
        //既存のプレビューを削除
        $preview.empty();
        // .prevewの領域の中にロードした画像を表示するimageタグを追加
        $preview.append($('<img>').attr({
                  src: e.target.result,
                  width: "500px",
                  class: "preview",
                  title: file.name
              }));
      };
    })(file);

    reader.readAsDataURL(file);
  });
})

function loadstart() {
	spinner.classList.remove('loaded');
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


$('#ajax-analyse').on('submit', e => {
	console.log("submitevenv");
    // デフォルトのイベントをキャンセルし、ページ遷移しないように!
    e.preventDefault();

    var formdata = new FormData($('#ajax-analyse').get(0));
	var task_id = 0;

    $.ajax({
        'url': 'https://healthreceiptapp.herokuapp.com/api/worker_analyse/',
        'type': 'POST',
		'dataType':'json',
        'data': formdata,
        'cache'       : false,
        'contentType' : false,
        'processData' : false,
        'dataType': 'json'
    }).done( response => {
		console.log(response);
		console.log(typeof response);
        task_id = response.task_id;

		console.log(task_id)

		var spanedSec = 0;

		id = setInterval(function () {
	        spanedSec++;
			console.log(spanedSec + "秒");

	        if (spanedSec >= 15) {
				$.ajax({
			        'url': 'https://healthreceiptapp.herokuapp.com/api/worker_result/',
			        'type': 'POST',
					'dataType':'json',
			        'data': {
			            'task_id': task_id,  // 記事タイトル
			        },
			        'dataType': 'json'
			    }).done( response2 => {
					if(response2.result != 0) {
						console.log(response2.result);
						console.log(response2);
						$("#result-text").text(response2.result);
						clearInterval(id);
					}
			    });
	        }
	    }, 1000);
    });

});
