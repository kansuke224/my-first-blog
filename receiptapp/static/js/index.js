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

$('#ajax-add-post').on('submit', e => {
    // デフォルトのイベントをキャンセルし、ページ遷移しないように!
    e.preventDefault();

	var task_id = 0;

    $.ajax({
        'url': '{% url "add" %}',
        'type': 'POST',
        'data': {
            "input_a": $("#input_a").value(),
			"input_b": $("#input_b").value()
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
		        'url': '{% url "worker_result" %}',
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
