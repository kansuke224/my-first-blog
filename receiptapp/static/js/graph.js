// グローバル変数定義
// html文書がロードされた瞬間に実行される


// オンロードイベント
// <body>に指定された各エレメントが表示され準備が整ったら実行される
// jQueryの書き方
$(function (){

})

function change_seibun(chart) {
	var value = $("#seibun").value();
}

function addData(chart, data) {
	chart.data.datasets.forEach((dataset) => {
		dataset.data.push(data);
	});
	chart.update();
}

function removeData(chart) {
	chart.data.datasets.forEach((dataset) => {
		dataset.data.pop();
	});
	chart.update();
}

function updatelabel(chart, label) {
	chart.data.datasets.forEach((dataset) => {
		dataset.label = label;
	})
	chart.update();
}

function updateText(chart, text) {
	chart.options.title.text = text;
	chart.update();
}
