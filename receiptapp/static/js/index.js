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
