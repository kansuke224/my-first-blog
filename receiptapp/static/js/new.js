// グローバル変数定義
// html文書がロードされた瞬間に実行される

var spinner = document.getElementById('loading');

// オンロードイベント
// <body>に指定された各エレメントが表示され準備が整ったら実行される
// jQueryの書き方
$(function (){
 	spinner.classList.add('loaded');

    $('#ajax-analyse').on('change', 'input[type="file"]', function(e) {
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

    spinner.classList.remove('loaded');

    // $("<p>", {class: "p_load", text: "画像解析中です、しばらくお待ちください・・・"}).appendTo("#load");
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
        console.log("worker_analyse 終了");
		console.log(response);
		// console.log(typeof response);
        task_id = response.task_id;

		console.log(task_id);

		var spanedSec = 0;
        var analyse_result;

		id = setInterval(function () {
	        spanedSec = spanedSec + 3;
			console.log(spanedSec + "秒");

	        if (spanedSec >= 30) {
                console.log("worker_resultにajaxトライ");
				$.ajax({
			        'url': 'https://healthreceiptapp.herokuapp.com/api/worker_result/',
			        'type': 'POST',
					'dataType':'json',
			        'data': {
			            'task_id': task_id,
			        },
			        'dataType': 'json'
			    }).done( response2 => {
					if(response2.result != 0) {
                        console.log("成功!")
                        $("#h3-select").removeClass('h3-select-before');
                        $("#h3-select").addClass('h3-select-after');
						//console.log(response2.result);
						//console.log(response2);
						analyse_result = JSON.parse(response2.result);
                        //console.log("1");
                        //console.log(analyse_result[0]);
                        //console.log("2");
                        //console.log(analyse_result[0][0]);
                        //console.log("3");
                        //console.log(analyse_result[0][0][0]);
                        var search_list = analyse_result;
                        // var count = analyse_result[1];
                        // food_select を作る処理
                        console.log(search_list);
                        for (var i in search_list) {
                            // 各食べ物リストについての処理
                            /*
                            [
                                []
                            ]
                            */
                            info_list = search_list[i][0];
                            var count = search_list[i][1];
                            // len = info_list.length;
                            console.log(info_list);
                            console.log(count);
                            if (count = 0) {
                                continue;
                            }
                            var ftag = $("<div>", {class: "food mb-5"}).appendTo("#result_fs");
                            $("<p>", {class: "p1", text: `候補が${count}個あります`}).appendTo(ftag);
                            $("<p2>", {class: "p1", text: "選択してください"}).appendTo(ftag);

                            var ftbl = $("<table>", {class: "table"}).appendTo(ftag);
                            for (var j in info_list) {
                                info = info_list[j];
                                var ftr = $("<tr>").appendTo(ftbl);
                                $("<td>", {text: info[0]}).appendTo(ftr);

                                var ftd1 = $("<td>").appendTo(ftr);
                                var fs = $("<select>", {class: "custom-select", name: i + "." + j}).appendTo(ftd1);
                                for (var k = 1; k<=10; k++) {
                                    $("<option>", {value: k, text: k + "00g"}).appendTo(fs);
                                }

                                var ftd2 = $("<td>", {class: "text-center"}).appendTo(ftr);
                                if (j == 1) {
                                    var fch = $("<input>", {
                                        type: "checkbox",
                                        name: "food",
                                        value: info[0] + "," + info[1] + "," + info[2] + "," + info[3] + "," + info[4] + "," + info[5] + "," + i + "." + j
                                    }).appendTo(ftd2);
                                    fch.checked = true;
                                } else {
                                    $("<input>", {
                                        type: "checkbox",
                                        name: "food",
                                        value: info[0] + "," + info[1] + "," + info[2] + "," + info[3] + "," + info[4] + "," + info[5] + "," + i + "." + j
                                    }).appendTo(ftd2);
                                }
                            }
                            $("<input>", {
                                type: "hidden",
                                name: i,
                                value: count
                            }).appendTo("#result_fs");
                        }
                        $("<input>", {
                            type: "submit",
                            class: "btn btn-info mb-5",
                            value: "食事内容決定"
                        }).appendTo("#result_fs");
                        spinner.classList.add('loaded');
						clearInterval(id);
					}
			    });
	        }
	    }, 3000);
    });

});
