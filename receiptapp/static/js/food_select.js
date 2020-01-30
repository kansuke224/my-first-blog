// グローバル変数定義
// html文書がロードされた瞬間に実行される


// オンロードイベント
// <body>に指定された各エレメントが表示され準備が整ったら実行される
// jQueryの書き方
$(function (){
	const spinner = document.getElementById('loading');
 	spinner.classList.add('loaded');
})
