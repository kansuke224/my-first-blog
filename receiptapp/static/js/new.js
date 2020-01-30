// グローバル変数定義
// html文書がロードされた瞬間に実行される

var spinner = document.getElementById('loading');

// オンロードイベント
// <body>に指定された各エレメントが表示され準備が整ったら実行される
// jQueryの書き方
$(function (){
 	spinner.classList.add('loaded');
})

function loadstart() {
	spinner.classList.remove('loaded');
}
